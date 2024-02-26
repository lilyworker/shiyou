import argparse
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

# parse args
praser = argparse.ArgumentParser()
praser.add_argument('date', type=str)
praser.add_argument('code', type=str)
args = praser.parse_args()


def get_pj_name():
    # get source of target site
    url = 'https://www.11meigui.com/tools/currency'
    content = requests.get(url).text

    # find pj name corresponding to the code
    soup = BeautifulSoup(content, 'html.parser')
    pj_name = list(soup.find('td',string=args.code+' ').previous_siblings)[5].text
    return pj_name[:-1]

def get_price():
    # set basic options to avoid anti-spider
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    options.add_argument(f"user_agent={user_agent}")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")
    chrome = webdriver.Chrome()
    chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                        "source": """
                            Object.defineProperty(navigator, 'webdriver',{
                                get: () => undefined
                            })"""
    })

    # get source of target site
    chrome.get('https://www.boc.cn/sourcedb/whpj/')

    # input information for searching
    start_date_input = WebDriverWait(chrome, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[2]/div/input')))
    start_date_input.send_keys(args.date)
    end_date_input = WebDriverWait(chrome, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input')))
    end_date_input.send_keys(args.date)
    pj_select = Select(WebDriverWait(chrome, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="pjname"]'))))
    pj_select.select_by_value(get_pj_name())

    # click search
    search_bt = WebDriverWait(chrome, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input')))
    search_bt.click()
    chrome.switch_to.window(chrome.window_handles[-1])

    # find target price and write it to 'result.txt'
    price = WebDriverWait(chrome, 10).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[4]/table/tbody/tr[2]/td[4]')))
    with open('result.txt', 'w') as f:
        f.write(price.text)

if __name__ == '__main__':
    get_price()

