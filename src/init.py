from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notify_run import Notify
import time
import datetime
import qacademico

if __name__ == '__main__':
    # Create some object instances
    notify = Notify()
    option = Options()
    option.set_headless(True)
    driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver', options=option)

    # Open Page
    lastValue = qacademico.openPage(driver)
    trigger = datetime.datetime.now()
    trigger_seconds = 15*60 # 15 minutes

    # Service is running in loop..
    while True:
        # Update Page
        value = qacademico.updatePage(driver)
        now = datetime.datetime.now()
        strDate = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        strNota = strDate + ' - NOTA NO ACADEMICO'
        strAlive = strDate + ' - NOTAS POSTADAS: ' + str(value)

        # Notify if exists a new grade
        if(lastValue != value):
            trigger = datetime.datetime.now()
            print(strNota)
            for i in range(2):
                notify.send(strNota)
            lastValue=value

        # Notify if trigger is activated
        if(abs(now-trigger).total_seconds()>trigger_seconds):
            print(strAlive)
            if(now.hour>=7 and now.hour<=23):
                for i in range(2):
                    notify.send(strAlive)
            trigger = datetime.datetime.now()

        # Sleep
        time.sleep(5)
