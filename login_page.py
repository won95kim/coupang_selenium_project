import json
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

class LoginPage: 
    URL = "https://www.coupang.com"
    LOGIN_INPUT_ID = "login-email-input"  # 로그인 이메일 필드
    PASSWORD_INPUT_ID = "login-password-input"  # 비밀번호 필드
    LOGIN_BUTTON = ".login__button"
    LOGOUT_BUTTON = "#logout > a"
    my_coupang = 'myCoupang'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # 메인 페이지 열기
    def open(self):
        self.driver.get(self.URL)

    # 로그인 페이지 열기
    def open_login(self):
        self.driver.find_element(By.CSS_SELECTOR, "#login").click()

    # 이메일 입력
    def input_email(self, user_email):
        user_email_box = self.driver.find_element(By.ID, self.LOGIN_INPUT_ID)
        user_email_box.send_keys(user_email)

    # 비밀번호 입력
    def input_password(self, user_password):
        user_password_box = self.driver.find_element(By.ID, self.PASSWORD_INPUT_ID)
        user_password_box.send_keys(user_password)

    # 로그인 버튼 클릭
    def click_login_button(self):
        login_button = self.driver.find_element(By.CSS_SELECTOR, self.LOGIN_BUTTON)
        login_button.click()

    # 로그아웃 버튼 클릭
    def click_logout_button(self):
        logout_button = self.driver.find_element(By.XPATH, self.LOGOUT_BUTTON)
        logout_button.click()

    # json 파일 불러오기
    @staticmethod
    def load_account_data():
        with open('account.json', 'r', encoding='UTF-8') as file:
            return json.load(file)
        
    # 쿠키 저장
    def save_cookies(self):
        cookies = self.driver.get_cookies()
        with open('cookies.json', 'w', encoding='UTF-8') as file:
            json.dump(cookies, file)

    # 쿠키 불러오기
    def load_cookies(self):
        with open('cookies.json', 'r', encoding='UTF-8') as file:
            cookies = json.load(file)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    # 로그인 상태 확인
    def is_logged_in(self):
        self.driver.find_element(By.ID, self.my_coupang)  # 로그인 후 사용되는 요소
        

