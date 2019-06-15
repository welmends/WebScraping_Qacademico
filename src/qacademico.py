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

def getCountGrades(driver):
    grades = driver.page_source.count('Nota:')
    return grades

def getGrades(driver):
    elementsCourse = driver.find_elements_by_tag_name('strong')
    elementsAllContent = driver.find_elements_by_class_name('conteudoTexto')
    grades = []
    enablerList = False
    enabler = False
    selector = 0

    for e_course in elementsCourse:
        for e_all in elementsAllContent:
            if(e_all.text.count('-')==3):
                if(e_course.text == e_all.text):
                    str_txt = e_all.text
                    begin = str_txt.find( '-',str_txt.find( '-' )+1 )+2
                    end = str_txt.find('-', begin)-1
                    #print(str_txt)
                    grades.append([str_txt[begin:end]])
                    enablerList = True
                else:
                    enablerList = False
            else:
                if(enablerList):
                    if(e_all.text[:2] == 'N1'):
                        selector = 1
                        enabler = True
                    elif(e_all.text[:2] == 'N2'):
                        selector = 2
                        enabler = True
                    elif(enabler):
                        if(selector==1):
                            idx = e_all.text.find('Nota:')
                            if(idx==-1):
                                enabler = False
                            else:
                                #print('N1: ', e_all.text[idx:idx+10])
                                grades[len(grades)-1].append('N1: ' + e_all.text[idx:idx+10])
                        elif(selector==2):
                            idx = e_all.text.find('Nota:')
                            if(idx==-1):
                                enabler = False
                            else:
                                #print('N2: ', e_all.text[idx:idx+10])
                                grades[len(grades)-1].append('N1: ' + e_all.text[idx:idx+10])

    gradesStr = ''
    for grade in grades:
        for i in grade:
            if(i==grade[0]):
                gradesStr += i + ':\n'
            else:
                gradesStr+= '     ' + i + '\n'
        gradesStr+='\n'
        
    return gradesStr

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

    # Return grades
    return getCountGrades(driver)

def updatePage(driver):
    # Refresh
    driver.refresh()

    # If the page was closed, open the page again
    if(driver.current_url != 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071'):
        driver = openQacademico(driver)

    # Return grades
    return getCountGrades(driver)
