"""Real isolated Edge checks. --media adds playback after both encodes finish."""
import json,argparse,traceback
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'.qa';OUT.mkdir(exist_ok=True)
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8185/');p.add_argument('--media',action='store_true');a=p.parse_args();checks=[];errors=[]
def checked(name):checks.append(name);print('PASS',name,flush=True)
with sync_playwright() as tool:
 browser=tool.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
 context=browser.new_context(viewport={'width':1440,'height':1000});page=context.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
 try:
  page.goto(a.url,wait_until='networkidle');assert page.locator('.metric strong').all_text_contents()==['7','2','0.8','7 / 0'];checked('hand-calculated golden metrics')
  page.screenshot(path=str(OUT/'desktop.png'),full_page=True)
  page.locator('#next').click();assert 'VH' in page.locator('#trace-copy').inner_text();page.locator('#prev').click();assert 'HV' in page.locator('#trace-copy').inner_text();checked('candidate stepping uses engine trace')
  cap=page.locator('#capacity');cap.fill('0');cap.dispatch_event('change');assert cap.get_attribute('aria-invalid')=='true';assert page.locator('.metric strong').first.inner_text()=='7';page.locator('#reset').click();assert cap.get_attribute('aria-invalid') is None;checked('invalid capacity preserves last valid state and reset recovers')
  pin=page.locator('#demand-grid [data-pin="A"]');pin.focus();page.keyboard.press('ArrowRight');assert page.locator('input[data-id="A"][data-axis="x"]').input_value()=='4.5';assert page.locator('.metric strong').first.inner_text()=='6';checked('keyboard pin movement changes computed demand')
  page.locator('#language').select_option('en');assert page.locator('html').get_attribute('lang')=='en';assert page.locator('input[data-id="A"][data-axis="x"]').input_value()=='4.5';assert 'Move a pin' in page.locator('#lab h2').inner_text();checked('English interface retains experimental state')
  page.locator('#reset').click();pin=page.locator('#demand-grid [data-pin="A"] circle');pin.scroll_into_view_if_needed();b=pin.bounding_box();scale=page.locator('#demand-grid svg').evaluate('(s)=>s.getScreenCTM().a');page.mouse.move(b['x']+b['width']/2,b['y']+b['height']/2);page.mouse.down();page.mouse.move(b['x']+b['width']/2+72*scale,b['y']+b['height']/2,steps=10);page.mouse.up();assert page.locator('input[data-id="A"][data-axis="x"]').input_value()=='4.5';checked('pointer coordinates respect actual SVG transform')
  page.locator('#preset').select_option('same');assert page.locator('.metric strong').first.inner_text()=='1';page.locator('#mode').select_option('upstream');assert page.locator('.metric strong').first.inner_text()=='2';page.locator('#preset').select_option('teacher');assert page.locator('.metric strong').first.inner_text()=='12';checked('same-cell, compatibility and pinned teacher presets compute live')
  page.locator('#questions form').first.locator('input').fill('7');page.locator('#questions form').first.locator('button').click();assert '1 / 6' in page.locator('#progress').inner_text();page.reload(wait_until='networkidle');assert '1 / 6' in page.locator('#progress').inner_text();page.locator('#clear-progress').click();checked('only correct submitted answers persist and clear')
  for width in [375,390,768,1440]:
   page.set_viewport_size({'width':width,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'Horizontal overflow {width}'
   if width==390:
    page.screenshot(path=str(OUT/'mobile.png'),full_page=True)
    assert page.locator('#chapters').is_visible(),'Film chapter navigation disappears on mobile'
  checked('mobile layout and chapter navigation remain available')
  if a.media:
   page.goto(a.url+'?lang=en',wait_until='networkidle');page.wait_for_function('document.querySelector("#lesson-video").dataset.language==="en"');v=page.locator('#lesson-video');assert v.evaluate('(v)=>v.videoWidth')==1920;assert abs(v.evaluate('(v)=>v.duration')-303.667)<.2;page.locator('#chapters button').nth(2).click();page.wait_for_timeout(500);assert v.evaluate('(v)=>v.currentTime')>30
   page.locator('#video-speed').select_option('1.5');page.locator('#caption-mode').select_option('off');page.locator('#language').select_option('zh');page.wait_for_function('document.querySelector("#lesson-video").dataset.language==="zh"');assert v.evaluate('(v)=>v.playbackRate')==1.5;assert v.evaluate('(v)=>[...v.textTracks].every(t=>t.mode!=="showing")');checked('real video metadata, seek, voice/UI switch and preferences')
  page.goto(a.url+'reading/?lang=en',wait_until='networkidle');assert page.locator('[data-reading-lang="en"]').is_visible();assert not page.locator('[data-reading-lang="zh"]').is_visible();assert 'def estimate' in page.locator('#code-reference').inner_text();assert len(page.locator('#code-data').inner_text())>1000;checked('complete notes and source are readable online')
  page.goto(a.url+'python/?lang=en',wait_until='networkidle');page.wait_for_function('!document.querySelector("#run").disabled',timeout=60000);assert 'BBox' not in page.locator('body').inner_text();page.locator('#run').click();page.wait_for_function('document.querySelector("#status").textContent.includes("Finished")');assert 'total: 7' in page.locator('#output').inner_text();checked('real CPython reference execution')
  page.locator('#code').fill('raise RuntimeError("intentional-probe")');page.locator('#run').click();page.wait_for_function('document.querySelector("#errors").textContent.includes("intentional-probe")');checked('real Python exceptions are visible')
  page.locator('#code').fill('while True: pass');page.locator('#run').click();page.wait_for_function('document.querySelector("#errors").textContent.includes("exceeded 5 seconds")',timeout=15000);page.wait_for_function('!document.querySelector("#run").disabled',timeout=60000);page.locator('#code').fill('print("recovered")');page.locator('#run').click();page.wait_for_function('document.querySelector("#output").textContent.includes("recovered")');checked('Python timeout terminates Worker and recovers')
  page.wait_for_function('!document.querySelector("#run").disabled');page.locator('#code').fill('while True: pass');page.locator('#run').click();page.wait_for_timeout(300);page.locator('#stop').click();page.wait_for_function('!document.querySelector("#run").disabled',timeout=60000);assert 'stopped' in page.locator('#errors').inner_text().lower();assert page.locator('#code').input_value()=='while True: pass';page.locator('#code').fill('print("after-stop")');page.locator('#run').click();page.wait_for_function('document.querySelector("#output").textContent.includes("after-stop")');checked('manual Stop preserves code and restores a usable interpreter')
  page.wait_for_function('!document.querySelector("#run").disabled');page.locator('#live').check();page.locator('#code').fill('print("live-recalculation")');page.wait_for_function('document.querySelector("#output").textContent.includes("live-recalculation")');checked('live mode executes edited code after debounce')
  blocked=browser.new_context();blocked.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw Error('denied')}})");q=blocked.new_page();q.goto(a.url,wait_until='networkidle');assert q.locator('.metric strong').first.inner_text()=='7';assert '不可用' in q.locator('#storage-status').inner_text();blocked.close();checked('disabled storage retains full lesson functionality')
  assert not errors,errors
  result={'status':'passed','checks':checks,'browser':'Microsoft Edge headless, isolated context','base':a.url,'media_playback_checked':a.media,'errors':errors}
 except Exception as exc:
  page.screenshot(path=str(OUT/'failure.png'),full_page=True);result={'status':'failed','checks':checks,'failure':str(exc),'traceback':traceback.format_exc(),'errors':errors};raise
 finally:
  (ROOT/'docs/qa/browser.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');browser.close()
