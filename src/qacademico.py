from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml

def openPage(driver):
    print('Open Qacademico..', end=' ')
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
    print('OK')

    return driver.page_source.count('Nota:')

def updatePage(driver):
    driver.refresh()
    if(driver.current_url != 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071'):
        driver = openQacademico(driver)
    return driver.page_source.count('Nota:')
