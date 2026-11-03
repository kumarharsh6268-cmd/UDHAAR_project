# Render SVG files to PNG via Chromium. usage: render.py out_dir file1.svg file2.svg ...
import sys, asyncio, pathlib
from playwright.async_api import async_playwright
SCALE=1.1
async def main(out, files):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':1080,'height':1920}, device_scale_factor=SCALE)
        for f in files:
            svg=pathlib.Path(f).read_text()
            html=f"<html><body style='margin:0;background:#000'>{svg}</body></html>"
            await pg.set_content(html); await pg.wait_for_timeout(50)
            o=pathlib.Path(out)/(pathlib.Path(f).stem+'.png')
            await pg.screenshot(path=str(o), clip={'x':0,'y':0,'width':1080,'height':1920})
            print('rendered',o,flush=True)
        await b.close()
asyncio.run(main(sys.argv[1], sys.argv[2:]))
