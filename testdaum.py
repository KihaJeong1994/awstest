#testdaum.py
from selenium.webdriver import Firefox, FirefoxOptions

USER = "01022620307"
PASS = "ksb030700!"
#Firefox 실행하기

browser=Firefox()

#로그인 페이지에 접근하기
url_login = "https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fwww.daum.net%252F"
browser.get(url_login)
print("로그인 페이지에 접근합니다.")
e=browser.find_element_by_id('id_email_2')
e.clear()
e.send_keys(USER)
e=browser.find_element_by_id("id_password_3")
e.clear()
e.send_keys(PASS)

form = browser.find_element_by_css_selector("button.btn_g.btn_confirm.submit")
form.click()
print("로그인 버튼을 클릭합니다")

browser.implicitly_wait(3)
browser.get("https://mail.daum.net/?nil_profile=min&nil_src=mail")

listmail=browser.find_element_by_css_selector('.tit_subject')
print(listmail)
for board in listmail:
    print("-",board.text)