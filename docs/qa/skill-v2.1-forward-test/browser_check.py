import os
from pathlib import Path
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parent
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get("EDGE_PATH") or None,headless=True)
    page=browser.new_page(viewport={"width":900,"height":850})
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto((root/"index.html").as_uri()+"?lang=en")
    val=lambda id:page.locator("#"+id).input_value()
    tab=lambda id:page.locator("#"+id)
    assert tab("title").inner_text()=="Mini Placement"
    tab("A").focus()
    page.keyboard.press("ArrowRight")
    assert (val("Ax"),val("Ay"))==("2.45","1.02")
    assert "A 2" in tab("result").inner_text()
    page.keyboard.press("ArrowLeft")
    assert (val("Ax"),val("Ay"))==("2.35","1.02")
    assert tab("A").evaluate("(e)=>e===document.activeElement")
    tab("A").scroll_into_view_if_needed()
    bounds=tab("A").bounding_box()
    # The SVG transform excludes the focus stroke included in the bounding box.
    x,y=bounds["x"]+bounds["width"]/2,bounds["y"]+bounds["height"]/2
    page.mouse.move(x,y); page.mouse.down()
    scale=tab("board").evaluate("(e)=>e.getScreenCTM().a")
    page.mouse.move(x+50*scale*.53,y,steps=5)
    assert (val("Ax"),val("Ay"))==("2.85","1.02"), (val("Ax"),val("Ay"), bounds, x,y)
    page.mouse.move(x,y)
    page.mouse.up()
    assert (val("Ax"),val("Ay"))==("2.35","1.02")
    tab("Ax").fill("oops");tab("By").fill("9")
    assert "Ax" in tab("feedback").inner_text() and "By" in tab("feedback").inner_text()
    tab("lang").click()
    assert "有限小数" in tab("feedback").inner_text() and val("Ax")=="oops"
    tab("By").fill("0")
    assert tab("By").get_attribute("aria-invalid")=="false" and "By" not in tab("feedback").inner_text()
    tab("reset").click()
    assert val("Ax")=="2.35" and tab("Ax").get_attribute("aria-invalid")=="false" and not tab("feedback").inner_text()
    for k,v in dict(Ax="1",Ay="0",Bx="1.9999999995",By="0").items():tab(k).fill(v)
    assert "0.000000001" in tab("result").inner_text()
    tab("answer").fill(".25");tab("answer").press("Enter")
    assert "再试" in tab("quiz").inner_text()
    tab("answer").fill(".50");tab("answer").press("Enter")
    assert "正确" in tab("quiz").inner_text() and tab("answer").evaluate("(e)=>e===document.activeElement")
    page.keyboard.press("Tab")
    assert tab("submit").evaluate("(e)=>e===document.activeElement")
    tab("lang").click()
    assert "Correct" in tab("quiz").inner_text()
    page.set_viewport_size({"width":360,"height":740})
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    tab("reading").click()
    assert page.locator("pre").inner_text()==(root/"reference.py").read_text()
    assert not errors,errors
    print("Edge",browser.version,"keyboard, drag, validation, translation, quiz, mobile width, reference OK")
    browser.close()
