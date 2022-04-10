# -------------------------------------------------------------------------------------------------------------------
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import os
os.environ['WDM_LOG_LEVEL'] = '0'
ua = UserAgent(verify_ssl=False)
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={ua}')
options.add_argument('--window-size=960,540')
options.add_argument('--incognito')
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True)
driver.set_window_position(0, 0, windowHandle='current')
# -------------------------------------------------------------------------------------------------------------------



data = []
total = ''

driver.get('https://simpleicons.org')
soup = BeautifulSoup(driver.page_source, 'html.parser')

for i in soup.find('p', {'class': 'header__description'}).get_text().strip():
    if i.isdigit():
        total = total + i
total = int(total)

for index, tag in enumerate(soup.find_all('h2', {'class': 'grid-item__title'})):
    data.append(tag.get_text())
    payload = f'{data[index]}' + ' '*(40-len(data[index])) + f'{index+1}/{total}' + ' '*(10-len(str(f'{index+1}/{total}'))) + ' completed' + ' '*(2) + '|' + ' '*(2) + f'{round((index/(total-1)*100), 10)}%' + ' '*(15-len(str(round((index/(total-1)*100), 10)))) + ' done'
    print(payload)

with open('names.txt', 'w') as file:
    for i in data:
        i.replace(' ', '-')
        driver.get(f'https://img.shields.io/static/v1?style=for-the-badge&logo={i}&label=&message=­&color=0d1116')









# file.write(f'![](https://img.shields.io/static/v1?style=for-the-badge&logo={i}&label=&message=­&color=0d1116)\n')

