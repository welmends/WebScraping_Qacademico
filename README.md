# Web Scraping

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
cd WebScraping\
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
