from flask import Flask, request, render_template
from playwright.async_api import async_playwright
import asyncio
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        try:
            asyncio.run(submit_form(form_data))
            return "Submitted!"
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')


async def submit_form(form_data):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = await browser.new_page()
        await page.goto("https://fakeformtesting.netlify.app/")
        await page.fill("input[name='username']", form_data.get('name', ''))
        await page.fill("input[name='email']", form_data.get('email', ''))
        await page.fill("input[name='password']", "fliptestpass")
        await page.get_by_role("button", name="submit").click()
        await page.wait_for_load_state("networkidle")
        await browser.close()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)