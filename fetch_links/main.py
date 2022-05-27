# for wait
import time
# import and start chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
# import models to be used by user
from models import modelsList
# to get links
from linkSave import findSave

# get auc.autodealsjapan
driver.get('http://auc.autodealsjapan.com/')

# params initialized
wait = WebDriverWait(driver, 10)

# username and password for the login
username = '#'
password = '#'

# login script
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(password)
loginScript = 'doLoad_login()'
driver.execute_script(loginScript)
wait.until(lambda driver: driver.current_url == 'http://auc.autodealsjapan.com/_home')
driver.get('http://auc.autodealsjapan.com/st?classic')

# Takes which models to scrap and load it
i = 0
while i < len(modelsList):
    print(f"Use {i} for {modelsList[i][1]}")
    i += 1

choice = int(input("Enter the number agaisnt model to scrap: "))
driver.execute_script(modelsList[choice][0])

# get the total pages
pageNum = 0
if WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".navi1"))):
    pages = driver.find_elements_by_class_name('navi1')
    for page in pages:
        temp = int(page.get_attribute('innerText'))
        if temp > pageNum:
            pageNum = temp


# get the link
def getLinks(driver):
    time.sleep(3)
    html = driver.find_element_by_id('aj_out_poisk').get_attribute('innerHTML')
    if (not (html.find('<div class="aj_nothing">nothing found</div>') == -1)):
        pass
    elif (not (html.find('aj_loading') == -1)):
        time.sleep(3)
        getLinks(driver)
    else:
        findSave(html)

i = 1
while i <= pageNum:
    getLinks(driver)
    i += 1
    driver.execute_script('page_num = '+ str(i) +';var form_id = "poisk";try {second_row_event(page_num);} catch (e) {}if (page_num == -1 || page_num == -2) {docId(form_id).sort_ord.value = "";page_num = 1;}docId(form_id).page.value = page_num;doLoad(form_id);')
    time.sleep(3)

print('Finished ----- Please Quit')
