# Web Scraping - Qacademico
Receive notifications directly on your smartphone about your grades on Qacademico.

## Requirements

### Install chromium - chromedriver
```
sudo apt install chromium-chromedriver
```

### Install virtualenv via pip:
```
pip install virtualenv
```

### Test your installation:
```
virtualenv --version
```

### Create the virtualenv for the project:
```
cd WebScraping_Qacademico/
virtualenv .env -p python3 --no-site-packages
```

### Activate the virtualenv:
```
. .env/bin/activate
```

### Intall the requirements:
```
pip3 install -r resources/requirements.txt
```

## Running

### Register your Android Smartphone on notify.run:
```
notify-run register
```

### Put your credentials on resources/credentials.yml, following the example:
```
credentials:
  username: xxxx
  password: xxxx
```

### Run the code:
```
python3 src/init.py
```

### At the end, deactivate the virtualenv:
```
deactivate
```
