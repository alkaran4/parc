from selenium import webdriver
import re
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




def date_converter(var):

    month_dict = {'янв': '01',
                  'фев': '02',
                  'мар': '03',
                  'апр': '04',
                  'мая': '05',
                  'июн': '06',
                  'июл': '07',
                  'авг': '08',
                  'сен': '09',
                  'окт': '10',
                  'ноя': '11',
                  'дек': '12'}

    if re.match(r'\d\d:\d\d', var):
        return date.today()
    elif re.match(r"\d+ \w+", var):
        lst = var.split(' ')
        return f'{date.today().year}-{month_dict[lst[1]]}-{lst[0]}'
    else:
        return var


def log_in():
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\Арина\Desktop\Саша\GB\2я четверть\Сбор данных из сети\chromedriver.exe')

    driver.get('https://account.mail.ru/login')
    driver.implicitly_wait(10)

    input_user_name = driver.find_element(By.XPATH, '//input[@name="username"]')
    input_user_name.send_keys('gb_students_787@mail.ru')
    input_user_name.send_keys(Keys.ENTER)

    input_user_name = driver.find_element(By.XPATH, '//input[@name="password"]')
    input_user_name.send_keys('Gfhjkmlkzcneltynjd001#')
    input_user_name.send_keys(Keys.ENTER)

    return driver


def letters_scrapper():
    letters = log_in().find_elements(By.XPATH, '//a[contains(@class, "llc")]')
    letter_list = []

    for letter in letters:
        dict = {}
        dict['sender'] = letter.find_element(By.XPATH, './/div[contains(@class, "llc__item_correspondent")]//span').get_attribute('title')
        dict['topic'] = letter.find_element(By.XPATH, './/span[contains(@class, "ll-sj__normal")]').text
        date_lett = letter.find_element(By.XPATH, './/div[contains(@class, "llc__item_date")]').text
        dict['date'] = date_converter(date_lett)
        letter_list.append(dict)

    return letter_list


letters_scrapper()

driver.quit()