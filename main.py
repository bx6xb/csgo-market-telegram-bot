import requests
from bs4 import BeautifulSoup as bs
import json
import time
import telebot
import sys

sys.stdout.reconfigure(encoding='utf-8')

token = '6175052325:AAGMSqpOwaBuPZvRnGAG7Ix9NoqdiWpXb6Y'

url = 'https://steamcommunity.com/market/'
url_search = 'search?q='
url_page = '#p1_default_desc/'

bot = telebot.TeleBot(token)

def load():
    with open('data.json', 'r', encoding='utf-8') as file:
        src = json.load(file)
        file.close()
    return src 


def save():
    global data
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.close()


def make_request(message):
    item = message.text.strip().replace(' ', '+')
    link = url + url_search + item
    req = requests.get(link)

    with open(f'index.html', 'w', encoding='utf-8') as file:
        file.write(req.text)
        file.close()

    with open(f'index.html', 'r', encoding='utf-8') as file:
        src = file.read()
        file.close()

    soup = bs(src, 'lxml')
    item_name = soup.find_all('span', class_='market_listing_item_name')
    item_buy_price = soup.find_all(class_='normal_price')
    item_sale_price = soup.find_all(class_='sale_price')
    item_link = soup.find_all(class_='market_listing_row_link')
    item_price = []

    for price in range(len(item_buy_price)):
        if price % 2 == 1:
            item_price.append(item_buy_price[price])

    if len(item_name) > 0:
        text = '-----ZenOw-----\n'
        for i in range(len(item_name)):
            text += f'{item_name[i].text} --> Buy: {item_price[i].text} Sale: {item_sale_price[i].text}\n{item_link[i].get("href")}\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'No items with that name(')


data = load()


@bot.message_handler(commands=['start', 'help'])
def start(message):
    
    bot.send_message(
        message.chat.id, 'Hi! This bot can track prices for the items on the Steam market place. Just write name of the item in English to start tracking it.')


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    make_request(message)


bot.polling()