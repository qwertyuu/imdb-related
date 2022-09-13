from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import dotenv
import datetime
from quantulum3 import parser
import dateparser
from babel.dates import format_date
from selenium.webdriver.support.wait import WebDriverWait


def pretty(sentence):
    quantum = parser.parse(sentence)[0]
    return f"{quantum.value.real}{quantum.unit.symbols[0]}"


dotenv.load_dotenv()

FIREFOX_IP = os.getenv('FIREFOX_IP', 'localhost:4444')

options = webdriver.FirefoxOptions()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
driver = webdriver.Remote(
    command_executor=f'http://{FIREFOX_IP}/wd/hub',
    options=options,
)
exception = False
try:
    driver.get(f"https://mybell.bell.ca/Mobility/Usage?AcctNo=D117CBAE2881AF0F9A4E84E57D2ED008F499DAFD73AA6547479C64A026B72BEE81D5D453C1CDFEEE8C5B38C0E689558B0D369E002F74C59C95DD3B3DF4FF6D47&SubNo=27468019&INT=MOB_MyServices_TXT_flyout_Mass_031013_mb_MyUsage")

    user_field = WebDriverWait(driver, timeout=30).until(lambda d: driver.find_element(by=By.ID, value="USER"))
    user_field.send_keys(os.getenv('BELL_LOGIN'))
    pass_field = driver.find_element(by=By.ID, value="PASSWORD")
    pass_field.send_keys(os.getenv('BELL_PASSWORD'))
    login_button = driver.find_element(by=By.ID, value="labelLogin")
    login_button.click()
    WebDriverWait(driver, timeout=30).until(lambda d: driver.find_element(by=By.CSS_SELECTOR, value="h2.bellSlimSemibold"))
    driver.get(f"https://mybell.bell.ca/Mobility/Usage?AcctNo=D117CBAE2881AF0F9A4E84E57D2ED008F499DAFD73AA6547479C64A026B72BEE81D5D453C1CDFEEE8C5B38C0E689558B0D369E002F74C59C95DD3B3DF4FF6D47&SubNo=27468019&INT=MOB_MyServices_TXT_flyout_Mass_031013_mb_MyUsage")

    time.sleep(3)
    sm = driver.find_element(by=By.CSS_SELECTOR, value="g>.chart-label-center-sm")
    used = driver.find_element(by=By.CSS_SELECTOR, value="g>.chart-label-center-used")
    qtyused = driver.find_element(by=By.CSS_SELECTOR, value="g>.chart-label-center-blueLight-bold")
    days_passed_percent = driver.find_element(by=By.CSS_SELECTOR, value="g>.chart-label-bottom-txt")
    days_passed = driver.find_element(by=By.CSS_SELECTOR, value="g>.chart-label-bottom-num")
    bill_date_elem = driver.find_element(by=By.XPATH, value="//*[contains (text(), 'Bill date' )]")
    bill_date_elem_text = bill_date_elem.text
    donut = driver.find_element(by=By.CSS_SELECTOR, value=".donutGraphFull")
    donut_b64 = donut.screenshot_as_base64
    donut.screenshot("donut.png")

    print(bill_date_elem.text)
    sm_text = sm.text
    used_text = used.text
    qtyused_text = qtyused.text
    days_passed_percent_text = days_passed_percent.text
    days_passed_text = days_passed.text
    print(sm.text)
    print(used.text)
    print(qtyused.text)
    print(days_passed_percent.text)
    print(days_passed.text)

except Exception as e:
    exception = True
    driver.save_screenshot('fail.png')
    print(e)
finally:
    driver.quit()

if exception:
    exit(1)

MAILGUN_SERVER_NAME = os.getenv('MAILGUN_SERVER_NAME')

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')

recipient_list = os.getenv('BELL_RECIPIENTS').split('|')

with open('email.html') as f:
    html = f.read()

bill_date = bill_date_elem_text.replace("Bill date: ", "")
dt = dateparser.parse(bill_date)
today = datetime.datetime.now()
diff = dt - today
remaining_days = diff.days + 1

content = ''
content += f"<div>{pretty(sm_text)} restant / 4.0GB total</div>"
content += f"<div>{pretty(qtyused_text)} utilisé ({pretty(used_text)})</div>"
content += f"<div>{days_passed_text} ({pretty(days_passed_percent_text)}) jours passés</div>"
content += f"<div>Il reste {remaining_days} jours avant la facturation le {format_date(dt, locale='fr')}</div>"
preheader = f"Bell: {pretty(used_text)} données utilisées, {pretty(days_passed_percent_text)} du mois"

for email in recipient_list:
    print(f'sending email to {email}')
    r = requests.post(
        MAILGUN_SERVER_NAME + "/messages",
        auth=("api", MAILGUN_API_KEY),
        files=[("attachment", open('donut.png', mode='rb'))],
        data={"from": "Consommation BELL LTE <bell@bot.com>",
              "to": email,
              "o:campaign": "",  # optional, but it was cool (and creepy) to track opens and clicks.
              "subject": "Ta consommation de LTE",
              #"attachment": open('donut.png', mode='rb').read(),
              "text": 'oups',
              "html": html.replace('{{CONTENT}}', content).replace('{{PREHEADER}}', preheader)})
    print(r.status_code)
    print(r.content)
