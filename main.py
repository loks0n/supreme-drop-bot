import time, sys, requests, hashlib
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver

#User payment data
PAYMENT_NAME = "John Smith"
PAYMENT_EMAIL = "johnsmith@gmail.com"
PAYMENT_PHONE = "0712345789"
PAYMENT_ADDR1 = "10 Church Street"
PAYMENT_ADDR2 = "Southwell"
PAYMENT_ADDR3 = ""
PAYMENT_ZIP = "NG146NU"
PAYMENT_CITY = "Nottingham"
PAYMENT_COUNTRY = "GB"
PAYMENT_TYPE = "visa"
PAYMENT_NUMBER = "3451860275849104"
PAYMENT_EXP_MONTH = "02"
PAYMENT_EXP_YEAR = "2017"
PAYMENT_CVV = "999"

#Product list: name, category, color, size, 
products = [["Leather Work","jackets","Silver","Medium"],]

#Supreme site data
mainUrl = 'http://www.supremenewyork.com/shop/all/'
baseUrl = 'http://supremenewyork.com'
checkoutUrl = 'https://www.supremenewyork.com/checkout'
browser = Browser('chrome')

def main():
        product_search()
        checkout()

def product_search():
        #For each product in product list
        for product in products:
                #Search category for product
                print("Searching for "+str(product))
                req = requests.get(mainUrl + product[1]).text
                print(req)
                soup = BeautifulSoup(req, 'html.parser')
                for div in soup.find_all('div', 'turbolink_scroller'):
                        name_flag = False
                        for a in div.find_all('a', href=True, text=True):
                                if product[0] in a.text:
                                        name_flag = True
                                if name_flag and product[2] in a.text:
                                        #If found: add to cart
                                        productUrl = baseUrl + a['href']
                                        browser.visit(productUrl)
                                        try:
                                                browser.find_option_by_text(product[3]).first.click()
                                        except:
                                                print('Error whilst adding '+product[0]+' to cart.')
                                        browser.find_by_name('commit').click()
                                        time.sleep(0.1)

def checkout():
        #Fill payment data
        browser.visit(checkoutUrl)
        browser.fill('order[billing_name]', PAYMENT_NAME)
        browser.fill('order[email]', PAYMENT_EMAIL)
        browser.fill('order[tel]', PAYMENT_PHONE)
        browser.fill('order[billing_address]', PAYMENT_ADDR1)
        browser.fill('order[billing_address_2]', PAYMENT_ADDR2)
        browser.fill('order[billing_address_3]', PAYMENT_ADDR3)
        browser.fill('order[billing_zip]', PAYMENT_ZIP)
        browser.fill('order[billing_city]', PAYMENT_CITY)
        browser.select('order[billing_country]', PAYMENT_COUNTRY)
        browser.select('credit_card[type]', PAYMENT_TYPE)
        browser.fill('credit_card[cnb]', PAYMENT_NUMBER)
        browser.select('credit_card[month]', PAYMENT_EXP_MONTH)
        browser.select('credit_card[year]', PAYMENT_EXP_YEAR)
        try:
                browser.fill('credit_card[vval]', PAYMENT_CVV)
        except:
                browser.fill('credit_card[ovv]', PAYMENT_CVV)
        browser.find_by_css('.iCheck-helper')[1].click()
        browser.find_by_name('commit').click()
        
if __name__=="__main__":
        main()










