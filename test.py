from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_data():
    url = 'https://www.nseindia.com/option-chain'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(url, headers=headers)
    print(page)
    with open('templates/test.html', 'w') as f:
        f.write(page.text)


@app.route('/')
def home():
    get_data()
    return render_template('test.html')

if __name__ == "__main__":
    app.run(debug=True)
