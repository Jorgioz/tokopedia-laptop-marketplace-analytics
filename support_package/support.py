from bs4 import BeautifulSoup
from bs4.element import NavigableString
import datetime
import os

path = os.getcwd()
folder_name = "product_urls"

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

def get_url_txt(url, keyword, search_position):
    if not os.path.isdir(path + "\\" + folder_name):
        os.makedirs(path + "\\" + folder_name)

    if " " in keyword:
        file_path = os.path.join(path, folder_name, f"{keyword[:6]}_{keyword[7:]}_urls.txt")
    else:
        file_path = os.path.join(path, folder_name, f"{keyword}_urls.txt")

    with open(file_path, "a", encoding="utf-8-sig") as file_url:
        file_url.write(f"{url},{keyword},{search_position}\n")

def get_product_url(product_url:list, keyword):
    if " " in keyword:
        file_path = os.path.join(path, folder_name, f"{keyword[:6]}_{keyword[7:]}_urls.txt")
    else:
        file_path = os.path.join(path, folder_name, f"{keyword}_urls.txt")

    if os.path.isfile(file_path):
        print(f"file {file_path} is found")
        with open(file_path, "r", encoding="utf-8-sig") as file:
            for line in file:
                data = line.strip().split(",")
                product_url.append(data)