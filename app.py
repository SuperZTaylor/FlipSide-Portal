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
                browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
                page = browser.new_page()
                page.goto("https://fakeformtesting.netlify.app/")
                page.fill("input[name='username']", "fliptest")
                page.fill("input[name='email']", "fliptest@email.com")
                page.fill("input[name='password']", "fliptestpass")
                page.get_by_role("button", name="Submit:").click()
                page.wait_for_load_state("networkidle")   # <-- ensures submission completes
                browser.close()
                
            return "Submitted!"
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('index.html')




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)