from flask import Flask, request, render_template
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        try:
            with sync_playwright() as p:
                #browser = p.chromium.launch(headless=False)
                browser = p.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                page = browser.new_page()
                page.goto("https://fakeformtesting.netlify.app/")
                page.get_by_role('textbox', name='Username:').fill('fliptest')
                page.get_by_role('textbox', name='Email:').fill('fliptest@email.com')
                page.get_by_role('textbox', name='Password:').fill('fliptestpass')
                page.get_by_role('button', name='Submit:').click()
                browser.close()
            return "Submitted!"
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)