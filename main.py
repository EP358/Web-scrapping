import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

HOST = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page="
ARTICLES = "&hhtmFrom=vacancy_search_list"


def get_headers():
    return Headers(browser="firefox", os="win").generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text


def parse_link(page):
    html = get_text(f"{HOST}{page}{ARTICLES}")
    soup = BeautifulSoup(html, features="html5lib")
    articles = soup.find_all("a", class_="serp-item__title")
    links = []
    for article in articles:
        link = article['href']
        links.append(link)
    return links
        
def parse_page():
    links_list = []
    for page in range(0, 5):
        print(f'Обработка {page + 1} страницы...')
        links = parse_link(page)
        for link in links:
            html = get_text(f"{link}")
            soup = BeautifulSoup(html, features="html5lib")
            description = soup.find(class_="g-user-content")
            description = str(description)
            if 'Flask' in description:
                links_list.append(link)
            elif 'flask' in description:
                links_list.append(link)
            elif 'Django' in description:
                links_list.append(link)
            elif 'django' in description:
                links_list.append(link)
    return links_list
       
def parse_info():
    parse_info_dict = []
    links = parse_page()
    for link in links:
        html = get_text(f"{link}")
        soup = BeautifulSoup(html, features="html5lib")
        salary = soup.find(class_="bloko-header-section-2 bloko-header-section-2_lite").text.replace('\u2009', '').replace('\xa0', '').replace('\u202f', '')
        if salary is None:
            return
        company = soup.find(attrs={'data-qa': 'bloko-header-2'}).text.replace('\xa0', ' ')
        if company is None:
            return
        city = soup.find(attrs={'data-qa': 'vacancy-view-location'})
        if city is None:
            city = soup.find(attrs={'data-qa': 'vacancy-view-raw-address'})
        parse_dict = {
        "link": link,
        "salary": salary,
        "company": company,
        "city": city.text.split(',')[0]
        }
        parse_info_dict.append(parse_dict)
    


    with open('test.json', 'w', encoding="utf-8") as f:
        json.dump(parse_info_dict, f, ensure_ascii=False, indent=4)
    
    print('Обработка успешно закончена!')

if __name__ == "__main__":
    parse_info()
    