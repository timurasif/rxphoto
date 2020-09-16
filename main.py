from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import csv
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome(r'C:\Users\Lenovo\Downloads\chromedriver_win32\chromedriver')
driver.maximize_window()

url = 'https://app.rxphoto.com/#/login'
driver.get(url)

# Enter credentials and hit submit
username = driver.find_element_by_xpath('//input[@id="login_username"]')
username.clear()
username.send_keys('mkelleher')
time.sleep(1)

password = driver.find_element_by_xpath('//input[@id="login_password"]')
password.clear()
password.send_keys('password')
time.sleep(2)

submit = driver.find_element_by_xpath('//form[@name="loginForm"]/div[@class="uk-margin-medium-top"]/button')
submit.click()
time.sleep(250)


clients = WebDriverWait(driver, 50).until(EC.presence_of_all_elements_located((By.XPATH, '//tr/td[@class="mat-cell cdk-column-name mat-column-name ng-star-inserted"]/div/a')))
clients_hrefs = []
for client in clients:
    clients_hrefs.append(client.get_attribute('href'))

with open('Client Info.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Client Id', 'DOB', 'Last visit', 'Images', 'PDFs', 'Notes'])

for href in clients_hrefs:
    driver.get(href)
    time.sleep(30)
    name = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//div[@class="patient-info-details"]/div[@class="title ng-binding"]')))
    name = name.text

    info = driver.find_elements_by_xpath('//div[@class="subtitle ng-binding"]')
    info_list = []
    for element in info:
        info_list.append(element.text)

    for info in info_list:
        id = info_list[1]
        id = id.replace('Client ID: ', '')
        dob = info_list[2]
        last_visit = info_list[3]

    print('Name: ' + name)
    print('Client ID: ' + id)
    print('DOB: ' + dob)
    print('Last visit: ' + last_visit)



    # info = driver.find_elements_by_xpath('//div[@class="patient-info-details"]/div[@class="title"]')
    # for element in info:
    #     if 'DOB' in element.text:
    #         dob = element.find_element_by_xpath('./following-sibling::div[@class="subtitle ng-binding"]')
    #         dob = dob.text
    #         print('DOB: ' + dob)

    images = driver.find_elements_by_xpath('//figure[@class="gallery_item uk-overlay uk-overlay-hover ng-scope"]/a/img')
    img_srcs = ''
    if images:
        for img in images:
            img_srcs = img_srcs + img.get_attribute('src')
            img_srcs = img_srcs + '\n'

    time.sleep(3)

    document = driver.find_element_by_xpath('//button[@class="md-btn md-btn-small md-btn-primary md-btn-wave signed-docs position-relative waves-effect waves-button"]/span')
    doc_links = ''
    text = document.text
    if text:
        document = driver.find_element_by_xpath('//button[@class="md-btn md-btn-small md-btn-primary md-btn-wave signed-docs position-relative waves-effect waves-button"]')
        hover = ActionChains(driver).move_to_element(document)
        hover.perform()

        docs = driver.find_elements_by_xpath('//li[@ng-repeat="form in forms track by $index"]')

        for doc in docs:
            hover = ActionChains(driver).move_to_element(document)
            hover.perform()
            doc.click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[1])
            doc_links = doc_links + driver.current_url
            doc_links = doc_links + '\n'
            driver.close()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(5)

    notes = driver.find_element_by_xpath('//button[@class ="md-btn md-btn-small md-btn-primary md-btn-wave position-relative waves-effect waves-button"]')
    notes.click()
    notes_text = ''
    time.sleep(1)
    msgs = driver.find_elements_by_xpath('//ul[@class ="chat_message"]/li/p')
    if msgs:
        for msg in msgs:
            notes_text = notes_text + msg.text
            notes_text = notes_text + '\n'
            time.sleep(2)

    with open('Client Info.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, id, dob, last_visit, img_srcs, doc_links, notes_text])

    time.sleep(10)