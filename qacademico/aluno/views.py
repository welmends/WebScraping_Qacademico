# Create your views here.
from django.shortcuts import render
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import time
import json
import re

# Checks Methods
def checkBody(request):
    try:
        body_pass = json.loads(request.body.decode('utf-8'))
    except KeyError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
        return False
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
        return False
    else:
        return True
def checkKey(request, key):
    try:
        body_pass = json.loads(request.body.decode('utf-8'))[key]
    except KeyError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
        return False
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        print('Decoding JSON has failed')
        return False
    else:
        return True

# Scrap Selenium Webdriver
def search_one_string(object_string, start_string, end_string):
    strart_idx = object_string.find(start_string)
    end_idx = object_string.find(end_string)
    
    return object_string[strart_idx:end_idx]
def search_one_string_by_start(object_string, start_string, end_string):
    strart_idx = object_string.find(start_string)
    current_string = object_string[strart_idx+len(start_string):]
    end_idx = current_string.find(end_string)
    return current_string[0:end_idx]
def search_string(object_string, start_string, end_string):
    vec = []
    objects = [i.start() for i in re.finditer(start_string, object_string)] 
    start_len = len(start_string)
    for obj in objects:
        index = object_string[obj+start_len:].find(end_string)
        sub_str = object_string[obj+start_len:obj+start_len+index]
        vec.append(sub_str)
        #sub_str = sub_str.replace(" ","")
        #print( float(sub_str) )
    return vec
def getCountGrades(driver):
    grades = driver.page_source.count('Nota:')

    # Get class name and professor
    strart_cadeiras = "<td class=\"conteudoTexto\">"
    end_cadeiras = "</td>"
    cadeiras  = search_string(str(driver.page_source),strart_cadeiras,end_cadeiras)
    cadeiras_filter = []
    professor_filter = []
    string_n = chr(92) + 'n'
    for cadeira in cadeiras:
        cadeiras_filter.append(cadeira.split("-")[2].split(")")[0]+")")
        professor_filter.append(cadeira.split("-")[3].split("            ")[0][:-1])

    vec_search_nota = []
    for index in range(len(cadeiras_filter)):
        if index == len(cadeiras_filter) - 1:
            vec_search_nota.append( search_one_string(str(driver.page_source), cadeiras_filter[index], "</body></html>" ) )
        else:
            vec_search_nota.append( search_one_string(str(driver.page_source),cadeiras_filter[index],cadeiras_filter[index+1]) )
        
    vector_num_aulas_previstas = []
    for search_nota in vec_search_nota:
        current_str = search_one_string_by_start(search_nota, "aulas previsto</td>", "</td>")
        index_find = current_str.find(">")
        vector_num_aulas_previstas.append( current_str[index_find+1:] )
    
    vector_num_aulas_restantes = []
    for search_nota in vec_search_nota:
        current_str = search_one_string_by_start(search_nota, "<td>Aulas restantes (com base nas aulas previstas)</td>", "</td>")
        index_find = current_str.find(">")
        vector_num_aulas_restantes.append( current_str[index_find+1:] )
    
    vector_num_faltas = []
    for search_nota in vec_search_nota:
        current_str = search_one_string_by_start(search_nota, "<td>Faltas</td>", "</td>")
        index_find = current_str.find(">")
        vector_num_faltas.append( current_str[index_find+1:] )
    
    vector_split_notas = []
    for search_nota in vec_search_nota:
        # buscar por todas as ocorrências de "<td>Nota:" em search_nota 
        res_list = [i for i in range(len(search_nota)) if search_nota.startswith("<td>Nota:", i)] 
        vec_list = []
        for idx in range(len(res_list)):
            if idx < len(res_list) - 1:
                temp = search_nota[res_list[idx]:res_list[idx+1]].replace("<td>Nota: ","")
                index_temp = temp.find("<")
                vec_list.append(temp[:index_temp])
            else:
                temp = search_nota[res_list[idx]:].replace("<td>Nota: ","")
                index_temp = temp.find("<")
                vec_list.append(temp[:index_temp])
        vector_split_notas.append(vec_list)

    # for index_c in range(len(vector_split_notas)):
    #     print("notas:", vector_split_notas[index_c])
    #     print("cadeiras", cadeiras_filter[index_c])
    #     print("professor: ", professor_filter[index_c])
    #     print("aulas_previstas: ", vector_num_aulas_previstas[index_c])
    #     print("aulas_restantes: ", vector_num_aulas_restantes[index_c])
    #     print("num_faltas: ", vector_num_faltas[index_c])
    #     print("\n\n")
    
    return vector_split_notas, cadeiras_filter, professor_filter, vector_num_aulas_previstas, vector_num_aulas_restantes, vector_num_faltas
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

    gradesStr = '___NOTAS___\n'
    for grade in grades:
        for i in grade:
            if(i==grade[0]):
                gradesStr += i + ':\n'
            else:
                gradesStr+= '     ' + i + '\n'

    return gradesStr
def get_Grades(driver, input_login, input_pass):
    # Get into qacademico 'alunos login' page
    print('Open Qacademico..', end=' ')
    driver.get('https://qacademico.ifce.edu.br/qacademico/alunos')

    # Find elements of login and senha
    username = driver.find_element_by_id('txtLogin')
    password = driver.find_element_by_id('txtSenha')
    # Login with credentials
    username.send_keys(input_login)
    password.send_keys(input_pass)

    # Click to login into account
    loginBtn = driver.find_element_by_id("btnOk")
    loginBtn.click()

    # Get into qacademico 'diarios' page
    driver.get('https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071')

    # Return grades
    return getCountGrades(driver)
def updatePage(driver):
    # Refresh
    driver.refresh()

    # If the page was closed, open the page again
    if(driver.current_url != 'https://qacademico.ifce.edu.br/qacademico/index.asp?t=2071'):
        # Return grades
        return openPage(driver)
    else:
        # Return grades
        return getCountGrades(driver)

class alunos(APIView):

    def post(self, request):
        if checkBody(request) == False or checkKey(request, 'LOGIN') == False or checkKey(request, 'PASS') == False:
            out_json = {'error_message': 'Falta o body da requisição ou o body está errado'}
            return Response(out_json, status=status.HTTP_400_BAD_REQUEST)
        
        # load input post json body data
        body = json.loads(request.body.decode('utf-8'))
        login = body['LOGIN']
        password = body['PASS']
        
        # run scrap
        option = Options()
        option.set_headless(True)
        driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', options=option)
        time.sleep(1) # Let the user actually see something!
        
        vector_split_notas, cadeiras_filter, professor_filter, vector_num_aulas_previstas, vector_num_aulas_restantes, vector_num_faltas = get_Grades(driver, login, password)
        driver.quit()     

        out_json = []
        for index_c in range(len(vector_split_notas)):
            current_json = {
                "grades": vector_split_notas[index_c],
                "subject": cadeiras_filter[index_c],
                "professor": professor_filter[index_c],
                "scheduledclasses": vector_num_aulas_previstas[index_c],
                "remainingclasses": vector_num_aulas_restantes[index_c],
                "absences": vector_num_faltas[index_c]
            }
            out_json.append(current_json)
        return Response(out_json, status=status.HTTP_200_OK) 




