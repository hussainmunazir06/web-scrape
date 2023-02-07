from bs4 import BeautifulSoup
from selenium import webdriver
import csv

from datetime import datetime

# method to generate the url
def get_url(search_url='bags'):
    url = f"https://www.amazon.in/s?k={search_url}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    url += "&page{}"                    # for the number of pages
    return url

def take_data(item):
    """ will take a record of data"""
    a_tag = item.h2.a                   # helps to give the product name and url
    
    # Product Url
    product_url = "https://amazon.com"+a_tag.get('href')

    # Product Name
    product_name = a_tag.text.strip()

    try:
        # Product Price
        price = item.find('span', 'a-price')
        product_price = price.find('span', 'a-price-whole').text 
    except ArithmeticError:
        return

    try:
        # Rating
        rating = item.i.text 

        # Number of reviews
        reviews = item.find('span', 'a-size-base').text 
    except AttributeError:
        rating = ""
        reviews = ""

    result = (product_url, product_name, product_price, rating, reviews)
    return result


# starting the main method 



driver = webdriver.Chrome()
url = get_url("bags")
result = []

for page in range(1, 21):
    driver.get(url.format(page))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    record = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in record:
        temp_result = take_data(item)
        if temp_result:
            result.append(temp_result)
    
driver.close()

# save all the record to the csv file 
timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
filename = timestr + '.csv'
with open(filename, 'w', newline="", encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of reviews'])
    writer.writerows(result)
