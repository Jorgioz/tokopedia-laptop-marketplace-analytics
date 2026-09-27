import time
from bs4 import BeautifulSoup
import random
import csv

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from support_package import support

options = webdriver.ChromeOptions()
# options.add_argument("--disable-background-timer-throttling")
options.add_argument("--disable-backgrounding-occluded-windows")
# options.add_argument("--disable-renderer-backgrounding")
driver = uc.Chrome(options=options, version_main=153)        # version_main is Chrome Version
driver.maximize_window()

wait = WebDriverWait(driver, 20)

keywords = [
    "laptop", "laptop terbaik", "laptop terbaru",
    "laptop gaming", "laptop kerja", "laptop mahasiswa", "laptop kantor", "laptop editing", "laptop programming",
    "laptop asus", "laptop lenovo", "laptop acer", "laptop hp", "laptop dell", "laptop msi", "laptop axioo", "laptop advan", "macbook"
]

headers = [
    "product_name", "category_name", "keyword", "condition", "current_price", "original_price", "discount_percentage", "rating", "review_count", "sold_count", "search_position", "scraped_date",
    "seller_name", "seller_rating", "seller_location", "store_type", "product_url"
]

keyword_not_exist = []

def check_if_exist(xpath, timeout = 20):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except TimeoutException:
        return False

def click_more(keyword):
    scroll = 1
    more = 1

    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-testid='btnSRPShopTab']")))
        logo_toko = driver.find_element(By.XPATH, "//button[@data-testid='btnSRPShopTab']")
        driver.execute_script("arguments[0].click()", logo_toko)
        time.sleep(random.uniform(3.0, 5.0))
        
        logo_produk = driver.find_element(By.XPATH, "//button[@data-testid='btnSRPProductTab']")
        driver.execute_script("arguments[0].click()", logo_produk)
        time.sleep(random.uniform(3.0, 5.0))

        while True:
            time.sleep(random.uniform(1.0, 2.0))
            wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='css-5wh65g']")))
            print(f"Scroll {scroll} Keyword: {keyword}")

            for i in range(5):
                driver.execute_script("window.scrollBy(0,1000)")
                time.sleep(random.uniform(0.5, 1.0))
                print("Data:", len(driver.find_elements(By.XPATH, "//div[@class='css-5wh65g']")))
                # print(i)
                # driver.execute_script("window.scrollBy(0,1000)")
                # time.sleep(random.uniform(0.3, 0.5))
                # driver.execute_script("window.scrollBy(0,1000)")

            xpath = "//span[contains(text(), 'Muat Lebih Banyak')]"

            if check_if_exist(xpath):
                button = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click()", button)
                time.sleep(random.uniform(1.5, 2.0))
                print(f"click more {more}")
                more+=1
            elif more >= 1:       # The amount of scrolling performed
                break
            elif scroll >= 20:
                break

            scroll+=1
        print("Total data:", len(driver.find_elements(By.XPATH, "//div[@class='css-5wh65g']")))
    except Exception as e:
            print(f"Timeout to Click More Keyword {keyword}")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error: {e}")
            # traceback.print_exc()
            keyword_not_exist.append(keyword)


def get_data_url(product_url, result:list, search_position, keyword, total_data):
    print(f"Data {total_data}")
    print(f"{keyword} Link {search_position}") 
    print(f"link: {product_url}")

    try:
        driver.get(product_url)
        time.sleep(random.uniform(1.5, 2.0))
    
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-15hp1ih pad-bottom']")))
        soup = BeautifulSoup(driver.page_source, "lxml")

        # Get Dataset
        product_name = support.find_data(soup, "div", {"class":"css-1nylpq2"}, "product_name")
        category_name = support.find_category_name(soup, "a", {"class":"css-1oriv31-unf-heading e1qvo2ff7"})
        condition = support.find_data(soup, "li", {"class":"css-1i6xy22"}, "condition")[9:]
        current_price = support.find_data(soup, "div", {"class":"price"}, "current_price")
        original_price = support.find_data(soup, "div", {"class":"original-price"}, "original_price")
        discount_percentage = support.find_data(soup, "div", {"class":"css-1c4ggdd"}, "discount_percentage")
        rating = support.find_data(soup, "span", {"data-testid":"lblPDPDetailProductRatingNumber"}, "rating")
        review_count = support.find_data(soup, "span", {"data-testid":"lblPDPDetailProductRatingCounter"}, "review_count")
        sold_count = support.find_data(soup, "div", {"class":"css-70qvj9"}, "sold_count")
        seller_name = support.find_data(soup, "div", {"class":"css-1sl4zpk"}, "seller_name")
        seller_rating = support.find_data(soup, "p", {"class":"css-1dpfpja-unf-heading e1qvo2ff8"}, "seller_rating")
        seller_location = support.find_data(soup, "h2", {"class":"css-793nib-unf-heading e1qvo2ff2"}, "seller_location")
        store_type = support.find_data_attribute(soup, "img", {"class":"css-ebxddb"}, "alt", "store_type")

        time.sleep(random.uniform(1.0, 1.5))

        value = [
            product_name, category_name, keyword, condition, current_price, original_price, discount_percentage, rating, review_count, sold_count, search_position, support.scraped_date(),
            seller_name, seller_rating, seller_location, store_type, product_url
        ]

        result.append(dict(zip(headers, value)))

    except Exception as e:
        print(f"Timeout to get data {total_data}, keyword {keyword}")
        # print(f"Error Type: {type(e).__name__}")
        # print(f"Error: {e}")
        # traceback.print_exc()

    print(f"succesfully retrieved all data in link {search_position}\n")


def main():
    print("===== STARTING SCRAPING THE DATA =====")
    product_url = []
    for keyword in keywords:
        if " " in keyword:
            # url = f"https://www.tokopedia.com/search?st=&q=laptop&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
            url = f"https://www.tokopedia.com/search?st=&q=laptop%20{keyword[7:]}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
        else:
            # url = f"https://www.tokopedia.com/search?st=&q=laptop%20{keyword[7:]}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
            url = f"https://www.tokopedia.com/search?st=&q={keyword}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource="
        # url = "https://www.tokopedia.com/"
        driver.get(url)
        time.sleep(random.uniform(3.0, 5.0))

        click_more(keyword)

        # time.sleep(10)
        time.sleep(random.uniform(2.0, 3.0))
        soup = BeautifulSoup(driver.page_source, "lxml")     
        elements = soup.find_all("div", class_="css-5wh65g")
        # all_elements = soup.find_all("div", class_="css-jza1fo")
        # print(f"Total data: {len(all_elements)}")
        
        search_position = 0
        for element in elements:
            if element.find("a", class_="Ui5-B4CDAk4Cv-cjLm4o0g== XeGJAOdlJaxl4+UD3zEJLg=="):
                search_position+=1
                url = element.find("a", class_="Ui5-B4CDAk4Cv-cjLm4o0g== XeGJAOdlJaxl4+UD3zEJLg==")["href"]
                product_url.append([url, keyword, search_position])

                support.get_url_txt(keyword, url)

        print(f"Successfully retrieved all data in keyword {keyword}")
        print(f"Total url in keyword {keyword} : {search_position}")
        
        time.sleep(random.uniform(3.0, 5.0))

    total_data = 1
    results = []
    for data_url in product_url:
        get_data_url(data_url[0], results, data_url[2], data_url[1], total_data)
        total_data+=1
    
    with open("tokopedia_raw_dataset.csv", 'w', encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, headers)
        writer.writeheader()
        writer.writerows(results)
        # Back to home
        # tokopedia_logo = driver.find_element(By.XPATH, "//a[@data-testid='icnHeaderIcon'] | //a[@class='css-isbo03 e1cyykyf0']")
        # driver.execute_script("arguments[0].click()", tokopedia_logo)
        # time.sleep(2)

    # driver.save_screenshot("Home.png")
    

if __name__ == "__main__":
    try:
        keyword_not_exist = []
        main()
    finally:
        print("===== Finished scraping the data =====\n")
        if len(keyword_not_exist) > 0:
            print("There are several keywords that failed to scrape. Please retry scraping the following keywords:\n")
            for keyword in keyword_not_exist:
                print(keyword)
        else:
            print("All data has been scraped")
        driver.quit()