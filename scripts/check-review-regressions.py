"""Observe initial loading, consecutive keyboard use and raw-unit semantics."""
from pathlib import Path
import argparse,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--version',default='after');a=p.parse_args();result={}
with sync_playwright() as tool:
 b=tool.chromium.launch(executable_path='/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',headless=True)
 c=b.new_context(viewport={'width':1440,'height':1000});page=c.new_page();requests=[];page.on('request',lambda r:requests.append(r.url))
 page.goto('http://127.0.0.1:8185/?lang=en',wait_until='networkidle');page.wait_for_timeout(1000)
 result['initial_english_has_no_mp4_request']=not any('.mp4' in u for u in requests);result['initial_ready_state']=page.locator('#lesson-video').evaluate('(v)=>v.readyState')
 x=page.locator('input[data-id="A"][data-axis="x"]');x.fill('2.5');x.press('Tab');result['tab_moves_to_next_coordinate']=page.locator('input[data-id="A"][data-axis="y"]').evaluate('(e)=>e===document.activeElement')
 cell=page.locator('#demand-grid [data-cell="1,1"]');cell.focus();cell.press('Enter');result['selected_cell_keeps_keyboard_focus']=page.locator('#demand-grid [data-cell="1,1"]').evaluate('(e)=>e===document.activeElement')
 cap=page.locator('#capacity');cap.fill('0.4375');cap.dispatch_event('change');result['exact_capacity_is_accepted']=cap.get_attribute('aria-invalid') is None and 'C=0.4375' in page.locator('#inspect').inner_text();cap.fill('0.5');cap.dispatch_event('change');result['valid_capacity_clears_prior_error']=page.locator('#input-status').inner_text()==''
 page.locator('#reset').click();page.locator('#rudy-unit').select_option('raw');result['raw_rudy_metric']=page.locator('.metric strong').last.inner_text();result['raw_rudy_suppresses_hotspots']='—' in result['raw_rudy_metric'];result['raw_rudy_has_no_capacity_outline']=page.locator('#rudy-grid rect').evaluate_all('(els)=>els.every(e=>e.getAttribute("stroke")!=="#dfbd78")')
 page.locator('#mode').select_option('upstream');page.locator('[data-load="same"]').click();result['guided_same_cell_selects_promised_convention']=page.locator('#mode').input_value()=='path' and page.locator('.metric strong').first.inner_text()=='1'
 b.close()
result['status']='passed' if all(result[k] for k in ['initial_english_has_no_mp4_request','tab_moves_to_next_coordinate','selected_cell_keeps_keyboard_focus','exact_capacity_is_accepted','valid_capacity_clears_prior_error','raw_rudy_suppresses_hotspots','raw_rudy_has_no_capacity_outline','guided_same_cell_selects_promised_convention']) else 'failed'
(ROOT/f'docs/qa/review-{a.version}.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['status']=='passed'
