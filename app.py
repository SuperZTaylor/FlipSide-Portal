from flask import *
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
async def home():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("https://www.genesislh.com/pages/contact")
            await page.get_by_role("textbox", name="Name").fill("b")
            await page.get_by_role("textbox", name="Email").fill("b")
            await page.get_by_role("textbox", name="Message").fill("b")
            await page.pause()
            await browser.close()
        return "Submitted!"
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))