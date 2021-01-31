from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
import sys
import time
sys.path.append(".")
from sermon import Sermon

def getSermons(page, lastSermon):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(executable_path='C:/chromedriver.exe', options=options)
    URL = "https://accentral.apostolicchristian.org/sermons#page-{0}"
    browser.get(URL.format(page))
    print("--------------request made------------------")
    #line below  will set webdriver to wait infinitely
    #wait = WebDriverWait(browser, float("inf"))
    if page != 1:
        wait = WebDriverWait(browser, 1800)
        #wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sermon_row")))
        wait.until_not(EC.visibility_of_element_located((By.ID, "loadingAnimation"))) 
        wait.until(lambda x: False if lastSermon in browser.page_source else True)
    else: 
        wait = WebDriverWait(browser, 1800)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sermon_row")))      
    print("--------------the wait is over------------------")
    #TESTING------------------------------------------------
    f = open("page{}.html".format(page), "w+")
    f.write(browser.page_source)
    f.close()
    #TESTING END--------------------------------------------
    #browser.execute_script("document.getElementById('pages').value = 'Sermon';")
    #print("--------------javascript ran------------------")
    rawHtml = browser.page_source
    browser.close()
    htmlSoup = BeautifulSoup(rawHtml, "html.parser")
    results = htmlSoup.find(id="sermonContainers")
    sermon_elems = None
    sermon_elems = results.find_all("div", class_="sermon_row")
    lastSermon = sermon_elems[0]
    for sermon_elem in sermon_elems:
        dateAndType_elem = sermon_elem.find("div", class_="sermon_name allcaps letterspacing1").text
        minister_elem = sermon_elem.find("div", class_="sermon_author allcaps letterspacing1").text
        congregation_elem = sermon_elem.find("div", class_="float_left user_descriptions row_congregation_id").text
        passages_elem = sermon_elem.find("div", class_="float_left user_descriptions row_passages_id").text
        title_elem = sermon_elem.find("div", class_="float_left user_descriptions row_title_id").text
        keywords_elem = sermon_elem.find("div", class_="float_left user_descriptions row_keywords_id").text
        if None in (sermon_elem, minister_elem, congregation_elem):
            continue

        if minister_elem[3:7] == "Bro ":
            formattedMinister = minister_elem.lstrip("By Bro")
        elif minister_elem[3:7] == "Bro.":
            formattedMinister = minister_elem.lstrip("By Bro.")
        else:
            formattedMinister = minister_elem.lstrip("By")
        s = Sermon(dateAndType_elem[0:10], dateAndType_elem[13:], 
                        formattedMinister, congregation_elem.split(':')[1], passages_elem.split(':')[1].replace(" \u2022", ","), 
                        title_elem.split(':')[1], keywords_elem.split(':')[1])
        
        data = [s.date, s.type, s.minister, s.congregation, s.passages, s.title, s.keywords]
        sheet.append(data)
    #TESTING------------------------------------------------
    if page ==2:
        workbook.save(filename='accentral.xlsx')
    #TESTING END--------------------------------------------
    print("page {} proccessing complete".format(page))
    return str(lastSermon)

pages = 2761

workbook = openpyxl.load_workbook('accentral.xlsx')
sheet = workbook.active
lastSermon = ""

for page in range(1, pages+1):
    try:
       lastSermon = getSermons(page, lastSermon)
    except TimeoutException:
        print("page {} failed to load".format(page))
        break

workbook.save(filename='accentral.xlsx')