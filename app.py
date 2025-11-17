from flask import Flask, request, render_template
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://www.genesislh.com/pages/contact")
            page.get_by_role("textbox", name="Name").fill("b")
            page.get_by_role("textbox", name="Email").fill("b")
            page.get_by_role("textbox", name="Message").fill("b")
            page.pause()  # Optional: pauses for manual inspection
            browser.close()
        return "Submitted!"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))