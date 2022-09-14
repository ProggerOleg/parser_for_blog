import random
import sqlite3
import requests
from slugify import slugify
from bs4 import BeautifulSoup


months = {'січня': '1', 'лютого': '2', 'березня': '3', 'квітня': '4', 'травня': '5', 'червня': '6',
          'липня': '7', 'серпня': '8', 'вересня': '9', 'жовтня': '10', 'листопада': '11', 'грудня': '12'}


url = 'https://ua.korrespondent.net/'


def get_data(url_of_site):
    headers = {
    "accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif,"
              " image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3; q = 0.9",
    'accept - encoding': 'gzip, deflate, br',
    'accept - language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache - control': "max - age = 0",
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.79 Safari/537.36',
    }
    r = requests.get(url_of_site, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    articles_cards = soup.find_all('div', class_='article')
    for aricle in articles_cards:
        article_url = aricle.find("a").get("href")
        req = requests.get(article_url, headers=headers)
        soup1 = BeautifulSoup(req.text, 'lxml')
        try:
            title = soup1.find('h1', class_='post-item__title').text
            author_and_time = soup1.find('div', class_='post-item__info').text
            img_src = soup1.find('img', class_='post-item__big-photo-img').get('src')
            content = soup1.find('div', class_='post-item__text').text
            content = str(content).replace('\n', ' ')
            description = '. '.join(content.split('.')[:2])
            time_create = (author_and_time.split(',')[1]).split()
            time_create = (time_create[2] + '-' + months[time_create[1]] + '-' + time_create[0])
            author = ''.join(author_and_time.split(',')[:1])
            post_url = slugify(str(title)[:15])
            insert_db(title, description, content, img_src, time_create, random.randrange(1, 3), post_url)
        except Exception:
            print('Упс, не смог обработать пост по данной ссылке: ' + article_url)


def insert_db(title, description, content, image, time_create, author, post_url):
    connection = sqlite3.connect('/home/oleg/PycharmProjects/pythonProject/blog/db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("""
            INSERT INTO blog_app_post(title, h1, description, content, image, time_create, author_id, url) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (title, title, description, content,
                                                 image, time_create, author, post_url))
    connection.commit()


def main():
    get_data(url)


if __name__ == '__main__':
    main()
