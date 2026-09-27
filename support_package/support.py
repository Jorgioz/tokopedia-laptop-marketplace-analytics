from bs4 import BeautifulSoup
from bs4.element import NavigableString
import datetime
import os

path = os.getcwd()
folder_name = "url_product"

def find_data(soup:BeautifulSoup, name:str, attrs:str, data = "data") -> NavigableString:
    if soup.find(name, attrs):
        print(f"succesfully retrieved the {data}")
        return soup.find(name, attrs).get_text(strip=True)
    else:
        print(f"{data} is not found")
        return f"Null"

def find_category_name(soup:BeautifulSoup, name:str, attrs:str) -> NavigableString:
    if len(soup.find_all(name, attrs)) > 3:
        print("succesfully retrieved the category_name")
        return soup.find_all(name, attrs)[3].get_text(strip=True)
    else:
        print("category name is not found")
        return f"Null"

def find_data_attribute(soup:BeautifulSoup, name:str, attrs:str, add_attribute:str, data = "data") -> NavigableString:
    if soup.find(name, attrs):
        print(f"succesfully retrieved the {data}")
        return soup.find(name, attrs).get(add_attribute)
    else:
        print(f"{data} is not found")
        return f"Null"

def scraped_date():
    return datetime.date.today().strftime("%d/%m/%Y")

def get_url_txt(keyword, url):
    if not os.path.isdir(path + "\\" + folder_name):
        os.makedirs(path + "\\" + folder_name)

    with open(f"{path}\\{folder_name}\\{keyword}_url.txt", "a", encoding="utf-8-sig") as file_url:
        file_url.write(f"{url}\n")
 