import os
import string
import sys

import requests
from bs4 import BeautifulSoup


def get_web_page_contents(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r.status_code == 200:
        return r.text
    else:
        print(f'The URL returned {r.status_code}!')

    return None


def delete_contents_dir(dir_name):
    for filename in os.listdir(dir_name):
        file_path = os.path.join(dir_name, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception:
            raise


def try_make_new_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    else:
        delete_contents_dir(dir_name)


def process_current_page(dir_name):
    try_make_new_dir(dir_name)

    articles = soup.findAll('article')

    for article in articles:
        article_type = article.findChildren("span", attrs={
            'class': 'c-meta__type'
        })
        if article_type:
            article_type = article_type[0].text
        if article_type != the_article_type:
            continue

        title = article.findChildren("a", attrs={
            'class': 'c-card__link u-link-inherit'
        }, recursive=True, href=True)
        if title:
            link = 'https://www.nature.com' + title[0]['href']
            title = title[0].text

            title_table = title.maketrans(" ", "_", string.punctuation)
            file_name = title.translate(title_table) + '.txt'

            with open(os.path.join(dir_name, file_name), 'w', encoding='utf-8') as out_file:
                article_contents = get_web_page_contents(link)
                soup2 = BeautifulSoup(article_contents, features="html.parser")
                body = soup2.findAll("div", attrs={
                    'class': 'c-article-body u-clearfix'
                })

                if body:
                    out_file.write(body[0].text)


try:
    num_pages = int(input())
    the_article_type = input()
    page_counter = 1
    dir_name = f'Page_{page_counter}'

    while True:
        if page_counter == 1:
            url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
            contents = get_web_page_contents(url)
            if contents is None:
                sys.exit(-1)

            soup = BeautifulSoup(contents, features="html.parser")

            process_current_page(dir_name)

            page_counter += 1
            dir_name = f'Page_{page_counter}'
        else:
            process_current_page(dir_name)

            next_children = soup.findAll('c - pagination__link',
                                         recursive = True, href = True)
            if next_children and next_children[0]:
                url = next_children[0]['href']
                contents = get_web_page_contents(url)
                if contents is None:
                    sys.exit(-1)

                soup = BeautifulSoup(contents, features="html.parser")

            page_counter += 1
            dir_name = f'Page_{page_counter}'
            if page_counter > num_pages:
                break
except IndexError:
    print('Invalid movie page!')
