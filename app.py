from flask import Flask, render_template, request
import requests, random
from bs4 import BeautifulSoup

app = Flask(__name__)


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0 Chrome/61.0.3396.99",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/16.16299 Chrome/67.0.3396.99",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3359.181 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Chrome/68.0.3396.99 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Safari/537.36",
    'Mozilla/80.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
]


def get_random_user_agent():
    return random.choice(user_agents)

def get_product_from_flipKart(item='mobiles'):
    url = f'https://www.flipkart.com/search?q={item}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    agent = get_random_user_agent()
    headers = {
            'user-agent': agent
        }
    page = requests.get(url, headers=headers)
    print(page)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


@app.route('/')
def home():
    search = request.args.get('search', 'mobiles')
    soup = get_product_from_flipKart(search)
    titles = soup.find_all(class_='KzDlHZ')
    if len(titles) != 0:
        discription = soup.find_all(class_='G4BRas')
        image = soup.find_all(class_='DByuf4')

    elif len(soup.find_all(class_='wjcEIp')) != 0:
        titles = soup.find_all(class_='wjcEIp')
        discription = soup.find_all(class_='NqpwHC')
        image = soup.find_all(class_='DByuf4')

    else:
        titles = soup.find_all(class_='syl9yP')
        if len(titles) == 0:
            dis = soup.find_all(class_='WKTcLC')
            titles = [d.text[:20] + '...' for d in dis]
        image = soup.find_all(class_='_53J4C-')
        discription = [d.text for d in soup.find_all(class_='WKTcLC')]

    images = [img['src'] for img in image]
    prices = soup.find_all(class_='Nx9bqj')
    product = dict(zip(titles, prices))
    products = dict(zip(titles, discription))
    product_img = dict(zip(titles, images))
    data = {
        'products': products,
        'product': product,
        'title': search,
        'product_img': product_img,
    }
    return render_template('index.html', **data)


if __name__ == "__main__":
    app.run(debug=True)
