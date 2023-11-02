#importing libraries
#To create dataframe
import pandas as pd
#To parse HTML
from bs4 import BeautifulSoup
#To access websites
import requests
#Always import when using BS4 in case i need to use it
import re
#Allow python to interact with website
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
#Strip Numbers from string
import nums_from_string
#Allow selenium time to wait
import time

#Setting up chrome options
chromeOptions = Options()
chromeOptions.headless = False

#Accessing website through selenium
s = Service(r"C:\Users\might\OneDrive\Documents\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chromeOptions)
driver.get("https://www.bbcgoodfood.com")
time.sleep(5)

#Switching iframe to click consent button
driver.switch_to.frame("sp_message_iframe_730595")
button = driver.find_element(by=By.XPATH, value=('//button[@title="AGREE"]'))
button.click()
time.sleep(2)

#Typing pie in search bar
searchbar = driver.find_element(By.ID, "branded-section-search-input")
searchbar.click()
searchbar.send_keys("pie")
searchbar.send_keys(Keys.RETURN)



#get current url
get_url = driver.current_url

#find number of pages
page = requests.get(get_url)
doc = BeautifulSoup(page.text, "html.parser")
find_string = doc.find_all("h2")
length = len(find_string)
pgnm = 1
while length <2:
    pgnm = pgnm+1
    pgnms = str(pgnm)
    pgnmss = pgnms.strip()
    url ="https://www.bbcgoodfood.com/search/recipes/page/"+pgnmss+"?q=pie&sort=-relevance"
    page = requests.get(url)
    doc = BeautifulSoup(page.text, "html.parser")
    find_string = doc.find_all("h2")
    length = len(find_string)
    if length == 2:
        print ("Total number of pages is" ,pgnm-1)
        break



#close offer iframe
time.sleep(20)
driver.switch_to.frame("offer_becc6ba7ac773010ccd5-0")
button = driver.find_element(by=By.XPATH, value=('//button[@class="pn-widget__link pn-widget__link--secondary unbutton"]'))
button.click()
time.sleep(2)




#set sort order to most popular
#Scroll so that sort box is clickable
driver.execute_script("window.scrollTo(0, 400)")
time.sleep(3)
dropdown = driver.find_element(by=By.ID, value =('sort-by'))
dropdown.click()
dropdown.send_keys("m")
dropdown.send_keys(Keys.RETURN)

#set a 4 star+ filter
button = driver.find_element(by=By.XPATH, value=('//button[@class="standard-button standard-button--secondary standard-button--fluid qa-edit-filters-button"]'))
button.click()
driver.execute_script("window.scrollTo(0, 400)")
time.sleep(1)
button = driver.find_element(by=By.CSS_SELECTOR, value=("[aria-label='Filter by Rating']"))
button.click()
time.sleep(3)
button = driver.find_elements(by=By.XPATH, value=("//label[@class='form-check-input__label body-copy-small']"))[3]
button.click()

#Grab current url and close selenium to save memory
currenturl = driver.current_url
currenturls = str(currenturl)
print (currenturls)
time.sleep(3)
driver.close()
time.sleep(3)

#creating lists
recipe_name =[]
linkk =[]
caloriesss=[]

#creating while loop
i=1
while i<=6:
    a = str(i)
    url = (currenturls)
    split = url.split("?")
    splitstr = str(split[0])
    splitstr2 = str(split[1])
    splitstrf = splitstr[:-1]
    new_url = (splitstrf+"/page/"+a+"?"+splitstr2)
    page = requests.get(new_url)
    doc = BeautifulSoup(page.text, "html.parser")
    recipes = doc.find_all("h4")
    for recipe in recipes:
#finding,concatenating and accessing link
        link = (recipe.find("a").get("href"))
        links = str(link)
        linka = ("https://www.bbcgoodfood.com"+links)
        pie = requests.get(linka)
        document = BeautifulSoup(pie.text, "html.parser")
#no data found for calories in pork pies therefore creating an if statement to show that there was no data found.
        if linka == "https://www.bbcgoodfood.com/recipes/raised-pork-pie":
#finding and cleaning title
            title = document.find("h1")
            titles = str(title)
            titler = titles.split('<h1 class="heading-1">')
            titled = str(titler)
            titleb = titled.split('</h1>')
            titlef = titleb[0]
            titleg = str(titlef)
            titleh =  titleg[6:]
            titlei = titleh.replace("&amp;", "&")
#finding and cleaning calories
            calories2 = "No data"
            recipe_name.append(titlei)
            linkk.append(linka)
            caloriesss.append(calories2)
        else:
#finding and cleaning title
            title = document.find("h1")
            titles = str(title)
            titler = titles.split('<h1 class="heading-1">')
            titled = str(titler)
            titleb = titled.split('</h1>')
            titlef = titleb[0]
            titleg = str(titlef)
            titleh =  titleg[6:]
            titlei = titleh.replace("&amp;", "&")
#finding and cleaning calories
            tbody = document.tbody
            trs = tbody.contents
            trs0 = (trs[0])
            trss = str(trs0)
            calories = (nums_from_string.get_nums(trss))
            caloriess = str(calories)
            calories1 = caloriess.replace("[", "")
            calories2 = calories1.replace("]", "")
            recipe_name.append(titlei)
            linkk.append(linka)
            caloriesss.append(calories2)
    i=i+1
#Create dataframe and write to excel
df = pd.DataFrame(list(zip(recipe_name, linkk, caloriesss)),columns =['Recipe', 'Link', 'Calories'])
df.to_excel('recipe.xlsx', index=False)





