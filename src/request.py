from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from notify_run import Notify
import time
import yaml
import datetime

def openQacademico(driver):
    driver.get('https://qacademico.ifce.edu.br/qacademico/alunos')

    username = driver.find_element_by_id('txtLogin')
    password = driver.find_element_by_id('txtSenha')

    with open("resources/credentials.yml", 'r') as stream:
        try:
            yamlData = yaml.safe_load(stream)
            username.send_keys(yamlData['credentials']['username'])
            password.send_keys(yamlData['credentials']['password'])
        except yaml.YAMLError as exc:
            print(exc)

    loginBtn = driver.find_element_by_id("btnOk")
    loginBtn.click()

    driver.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071')

    return driver

def updateQacademico(driver):
    driver.refresh()
    if(driver.current_url != 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071'):
        driver = openQacademico(driver)
    return driver.page_source.count('Nota:')

opt = Options()
opt.set_headless(True)
driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', options=opt)
notify = Notify()

openQacademico(driver)
lastValue = updateQacademico(driver)
aliveTrigger = 1
thresh_time  = 60*15 # 15 minutes

while True:
    value = updateQacademico(driver)
    strNota = 'NOTA NO ACADEMICO'
    strAlive = 'NOTAS POSTADAS: ' + str(value)

    if(lastValue != value):
        print(strNota)
        notify.send(strNota)
        lastValue=value
        aliveTrigger = 1

    if(aliveTrigger==thresh_time):
        print(strAlive)
        now = datetime.datetime.now()
        if(now.hour>7 and now.hour<23):
            notify.send(strAlive)
        aliveTrigger = 1

    aliveTrigger+=1
    time.sleep(1)
