#!/usr/bin/env python
import time, sys, requests, hashlib, pygubu, json, os
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
import tkinter as tk

#Supreme site data
mainUrl = 'http://www.supremenewyork.com/shop/all/'
baseUrl = 'http://supremenewyork.com'
checkoutUrl = 'https://www.supremenewyork.com/checkout'
start_time = time.time()

#os.path.join(os.path.dirname(os.path.realpath(__file__)),"chromedriver.exe")
class Container:
    pass

class Application:
    def __init__(self, master):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('bin\\gui.ui')
        self.mainwindow = builder.get_object('mainwindow', master)
        self.console = builder.get_object('console')
        self.productlist = builder.get_object('listbox_products')
        builder.connect_callbacks(self)
        self.container = Container()
        self.builder.import_variables(self.container)
        self.load_paymentdata()

    def add_productdata(self):
        self.productlist.insert(tk.END, [self.container.productname.get(),self.container.productcolour.get(),self.container.productsize.get(),self.container.productcategory.get()])

    def remove_productdata(self):
        index = int(self.productlist.curselection()[0])
        self.productlist.delete(index)

    def select_productdata(self, event):
        index = int(self.productlist.curselection()[0])
        value = self.productlist.get(index)
        self.container.productname.set(self.productlist.get(index)[0])
        self.container.productcolour.set(self.productlist.get(index)[1])
        self.container.productsize.set(self.productlist.get(index)[2])
        self.container.productcategory.set(self.productlist.get(index)[3])


    def load_paymentdata(self):
        self.console_print("Loading config.json")
        self.config = {}
        try:
            with open('bin\\config.json', 'r') as f:
                self.config = json.load(f)
            self.container.value_name.set(self.config['name'])
            self.container.value_email.set(self.config['email'])
            self.container.value_phone.set(self.config['phone'])
            self.container.value_addr1.set(self.config['addr1'])
            self.container.value_addr2.set(self.config['addr2'])
            self.container.value_addr3.set(self.config['addr3'])
            self.container.value_zip.set(self.config['zip'])
            self.container.value_city.set(self.config['city'])
            self.container.value_country.set(self.config['country'])
            self.container.value_cardtype.set(self.config['cardtype'])
            self.container.value_cardnumber.set(self.config['cardnumber'])
            self.container.value_cardexpmonth.set(self.config['cardexpmonth'])
            self.container.value_cardexpyear.set(self.config['cardexpyear'])
            self.container.value_cardcode.set(self.config['cardcode'])
            self.console_print("Loaded config.json")
        except:
            self.console_print("Failed to load config.json")
            self.update_paymentdata()

    def update_paymentdata(self):
        self.config.clear()
        self.config['name'] = self.container.value_name.get()
        self.config['email'] = self.container.value_email.get()
        self.config['phone'] = self.container.value_phone.get()
        self.config['addr1'] = self.container.value_addr1.get()
        self.config['addr2'] = self.container.value_addr2.get()
        self.config['addr3'] = self.container.value_addr3.get()
        self.config['zip'] = self.container.value_zip.get()
        self.config['city'] = self.container.value_city.get()
        self.config['country'] = self.container.value_country.get()
        self.config['cardtype'] = self.container.value_cardtype.get()
        self.config['cardnumber'] = self.container.value_cardnumber.get()
        self.config['cardexpmonth'] = self.container.value_cardexpmonth.get()
        self.config['cardexpyear'] = self.container.value_cardexpyear.get()
        self.config['cardcode'] = self.container.value_cardcode.get()
        with open('bin\\config.json', 'w') as f:
            json.dump(self.config, f)
        self.console_print("Updated config.json")

    def console_print(self, msg):
        self.console.configure(state="normal")
        self.console.insert(tk.END, msg+"\n")
        self.console.configure(state="disabled")

    def start_bot(self):
        self.console_print("Starting bot")
        self.browser = Browser("chrome")
        #self.browser.set_window_size(0, 0)
        self.console_print("Waiting for drop")
        #self.productlist.insert(tk.END, ['Work Jacket','Silver','Medium','jackets'])
        self.product_search()
        self.checkout()

    def product_search(self):
        #For each product in product list
        for product in self.productlist.get(0,self.productlist.size()):
                #Search category for product
                req = requests.get(mainUrl + product[3], verify=os.path.join(os.path.dirname(os.path.realpath(__file__)),"cacert.pem")).text
                soup = BeautifulSoup(req, 'html.parser')
                for div in soup.find_all('div', 'turbolink_scroller'):
                        name_flag = False
                        for a in div.find_all('a', href=True, text=True):
                                if product[0] in a.text:
                                        name_flag = True
                                if name_flag and product[1] in a.text:
                                        #If found: add to cart
                                        productUrl = baseUrl + a['href']
                                        self.browser.visit(productUrl)
                                        try:
                                                self.browser.find_option_by_text(product[2]).first.click()
                                        except:
                                                print('Error whilst adding '+product[0]+' to cart.')
                                        self.browser.find_by_name('commit').click()
                                        time.sleep(0.1)

    def checkout(self):
        #Fill payment data
        self.browser.visit(checkoutUrl)
        self.browser.fill('order[billing_name]', self.config['name'])
        self.browser.fill('order[email]', self.config['email'])
        self.browser.fill('order[tel]', self.config['phone'])
        self.browser.fill('order[billing_address]', self.config['addr1'])
        self.browser.fill('order[billing_address_2]', self.config['addr2'])
        self.browser.fill('order[billing_address_3]', self.config['addr3'])
        self.browser.fill('order[billing_zip]', self.config['zip'])
        self.browser.fill('order[billing_city]', self.config['city'])
        self.browser.select('order[billing_country]', self.config['country'])
        self.browser.select('credit_card[type]', self.config['cardtype'])
        self.browser.fill('credit_card[cnb]', self.config['cardnumber'])
        self.browser.select('credit_card[month]', self.config['cardexpmonth'])
        self.browser.select('credit_card[year]', self.config['cardexpyear'])
        try:
                self.browser.fill('credit_card[vval]', self.config['cardcode'])
        except:
                self.browser.fill('credit_card[ovv]', self.config['cardcode'])
        #Accept terms
        self.browser.find_by_css('.iCheck-helper')[1].click()
        #Checkout
        self.browser.find_by_name('commit').click()

def main():
    root = tk.Tk()
    app = Application(root)
    root.wm_title("Supreme Drop Bot")
    root.wm_resizable(0,0)
    root.wm_iconbitmap("bin\\favicon.ico")
    root.mainloop()

if __name__ == '__main__':
    main()
