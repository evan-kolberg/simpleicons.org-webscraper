from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import os

os.environ['WDM_LOG_LEVEL'] = '0'    # prevents webdriver manager from printing, it is quite annoying tbh

ua = UserAgent(verify_ssl=False)

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')    # helps go undetected
options.add_argument(f'--user-agent={ua}')
options.add_argument('--window-size=960,540')
options.add_argument('--incognito')    # doesn't save cookies after session
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

# adds extra protection against getting detected
stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True)

driver.set_window_position(0, 0, windowHandle='current')

data = []
total = ''

driver.get('https://simpleicons.org')
soup = BeautifulSoup(driver.page_source, 'html.parser')

for i in soup.find('p', {'class': 'header__description'}).get_text().strip():
    if i.isdigit():
        total = total + i
total = int(total)

print(f'\n{total} icon names to grab!')
print('Okay! I am going to iterate through all of them and export the data to a file. This data will work with .md file types!\n')

for i in range(total):
    data.append(soup.find('li', {'order-alpha': i}).get_text())
    payload = f'{data[i]}' + ' '*(50-len(data[i])) + f'{i+1}/{total}' + ' '*(10-len(str(f'{i+1}/{total}'))) + ' completed' + ' '*(2) + '|' + ' '*(2) + f'{round((i/(total-1)*100), 10)}%' + ' '*(15-len(str(round((i/(total-1)*100), 10)))) + ' done'
    print(payload)

