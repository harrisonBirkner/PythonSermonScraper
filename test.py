import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from openpyxl import Workbook
import os
import sys
sys.path.append(".")
from sermon import Sermon

lastSermon = '<div class="sermon_row"><div class="float_left sermon_row_left_user"><div class="sermon_name allcaps letterspacing1">2021-01-17 - Sunday PM</div><div class="sermon_author allcaps letterspacing1">By Bro George Gal</div></div><div class="float_left player_wrap_user" id="jp_container_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90"><div id="jplayer_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90" style="width: 0px; height: 0px;"><img id="jp_poster_0" style="width: 0px; height: 0px; display: none;"/><audio id="jp_audio_0" preload="metadata" src="https://s3-us-west-2.amazonaws.com/acmobile/da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90.mp3"></audio></div><div class="player_play" id="play_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90"></div><div class="player_pause" id="pause_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90" style="display: none;"></div><div class="seek-bar-container"><div class="seek-bar-bg"><div class="seek-bar" id="seekbar_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90" style="width: 100%;"><div class="play-bar" id="playbar_da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90" style="width: 0%;"></div></div></div></div></div><div class="float_right"><div class="downloadbutton"><a download="da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90.mp3" href="https://s3-us-west-2.amazonaws.com/acmobile/da6cdcdf-bfd7-4f4b-9a92-90261ceb2c90.mp3"><span class="download_btn allcaps letterspacing1"><img src="/resources/images/download.png"/>Download</span></a></div></div><div class="clear_both"></div><div class="float_left user_descriptions row_congregation_id"><div class="sermon_description allcaps letterspacing1">Congregation:</div><div>Akron</div></div><div class="float_left user_descriptions row_passages_id"><div class="sermon_description allcaps letterspacing1">Passages:</div><div>Ezekiel 17 • James 2</div></div><div class="float_left user_descriptions row_title_id"><div class="sermon_description allcaps letterspacing1">Title:</div><div>N/A</div></div><div class="float_left user_descriptions row_keywords_id"><div class="sermon_description allcaps letterspacing1">Keywords:</div><div>N/A</div></div><div class="clear_both"></div></div>'
page = 2
options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(executable_path='C:/chromedriver.exe', options=options)
URL = "https://accentral.apostolicchristian.org/sermons#page-2"
browser.get(URL)
print("--------------request made------------------")
#line below  will set webdriver to wait infinitely
#wait = WebDriverWait(browser, float("inf"))
if page != 1:
    wait = WebDriverWait(browser, 1800)
    wait.until(lambda x: False if lastSermon in browser.page_source else True)
    print("in second wait") 
else: 
    wait = WebDriverWait(browser, 1800)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "sermon_row"))) 
        
print("--------------the wait is over------------------")