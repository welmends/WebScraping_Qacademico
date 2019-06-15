from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import yaml

def loginOnPage(username, password):
    # Read credentials from credentials.yml
    with open("resources/credentials.yml", 'r') as stream:
        try:
            # Send credentials through webdriver
            yamlData = yaml.safe_load(stream)
            username.send_keys(yamlData['credentials']['username'])
            password.send_keys(yamlData['credentials']['password'])
        except yaml.YAMLError as exc:
            print(exc)

def openPage(driver):
    # Get into qacademico 'alunos login' page
    print('Open Qacademico..', end=' ')
    driver.get('https://qacademico.ifce.edu.br/qacademico/alunos')

    # Find elements of login and senha
    username = driver.find_element_by_id('txtLogin')
    password = driver.find_element_by_id('txtSenha')

    # Login with credentials
    loginOnPage(username, password)

    # Click to login into account
    loginBtn = driver.find_element_by_id("btnOk")
    loginBtn.click()

    # Get into qacademico 'diarios' page
    driver.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071')
    print('OK')

    # Return how many grades has been posted
    return driver.page_source.count('Nota:')


def updatePage(driver):
    # Refresh
    driver.refresh()

    # If the page was closed, open the page again
    if(driver.current_url != 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071'):
        driver = openQacademico(driver)

    # Return how many grades has been posted
    return driver.page_source.count('Nota:')
