import pytest
import time
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestLoginPage:
    user_name = '김혜원'

    # 로그인 페이지 정상 진입 확인
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_open_login_page(self, driver: WebDriver):
        try:
            login_page = LoginPage(driver)

            login_page.open()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com"))    # url에 쿠팡이 포함되는지 확인

            login_page.open_login()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains("login"))    # url에 login이 포함되는지 확인
            assert 'login' in driver.current_url    # 로그인 페이지로 정상 이동되었는지 확인

            os.makedirs('pass_img', exist_ok=True)  # 폴더 없으면 생성
            driver.save_screenshot('pass_img/로그인페이지-진입-성공.jpg')
        
        except NoSuchElementException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-진입-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-진입-실패-타임에러.jpg')
            assert False


    # 로그인 정상 동작 확인
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_login(self, driver: WebDriver):
        try:
            login_page = LoginPage(driver)
            account_data = login_page.load_account_data()   # json 파일 가져옴
            EMAIL = account_data["EMAIL"]
            PASSWORD = account_data["PASSWORD"]
            NAME = account_data["NAME"]

            login_page.open()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('coupang.com'))    # url에 쿠팡이 포함되는지 확인

            login_page.open_login()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains("login"))    # url에 login이 포함되는지 확인
            assert 'login' in driver.current_url    # 로그인 페이지로 정상 이동되었는지 확인

            login_page.input_email(EMAIL)
            login_page.input_password(PASSWORD)
            login_page.click_login_button()

            time.sleep(2)

            login_check = login_page.is_logged_in() # login 되었는지 확인
            assert NAME in login_check.text

            os.makedirs('pass_img', exist_ok=True)  # 폴더 없으면 생성
            driver.save_screenshot('pass_img/로그인페이지-로그인-성공.jpg')

        except NoSuchElementException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-로그인-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-로그인-실패-타임에러.jpg')
            assert False


    # 로그아웃 정상 동작 확인
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_logout(self, driver: WebDriver):
        try:
            login_page = LoginPage(driver)
            account_data = login_page.load_account_data()
            EMAIL = account_data['EMAIL']
            PASSWORD = account_data['PASSWORD']
            NAME = account_data["NAME"]

            login_page.open()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('coupang.com'))    # url에 쿠팡이 포함되는지 확인

            login_page.open_login()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('login'))    # url에 login이 포함되는지 확인
            assert 'login' in driver.current_url    # 로그인 페이지로 정상 이동되었는지 확인

            login_page.input_email(EMAIL)
            login_page.input_password(PASSWORD)
            login_page.click_login_button()

            time.sleep(2)

            login_check = login_page.is_logged_in()
            assert NAME in login_check.text

            time.sleep(2)

            login_page.click_logout_button()

            login_button = ws(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#login")) # Login 버튼 확인
            )
            assert login_button.is_displayed()

            os.makedirs('pass_img', exist_ok=True)  # 폴더 없으면 생성
            driver.save_screenshot('pass_img/로그인페이지-로그아웃-성공.jpg')
            
        except NoSuchElementException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-로그아웃-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-로그아웃-실패-타임에러.jpg')
            assert False


    # 자동 로그인 및 쿠키 활용
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_login_cookie(self, driver: WebDriver):
        try:
            login_page = LoginPage(driver)
            account_data = login_page.load_account_data()
            EMAIL = account_data['EMAIL']
            PASSWORD = account_data['PASSWORD']
            NAME = account_data["NAME"]

            login_page.open()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('coupang.com'))    # url에 쿠팡이 포함되는지 확인

            login_page.open_login()
            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('login'))    # url에 login이 포함되는지 확인
            assert 'login' in driver.current_url    # 로그인 페이지로 정상 이동되었는지 확인

            self.load_cookies()  # 쿠키 불러오기 (있으면 자동 로그인)
            self.driver.refresh()  # 페이지 새로고침 후 자동 로그인 상태 확인

            if not self.is_logged_in():
                login_page.input_email(EMAIL)
                login_page.input_password(PASSWORD)
                login_page.click_login_button()

                time.sleep(2)

                login_check = login_page.is_logged_in()
                assert NAME in login_check.text

                login_page.save_cookies()  # 로그인 후 쿠키 저장

            os.makedirs('pass_img', exist_ok=True)  # 폴더 없으면 생성
            driver.save_screenshot('pass_img/로그인페이지-쿠키로그인-성공.jpg')
            
        except NoSuchElementException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-쿠키로그인-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/로그인페이지-쿠키로그인-실패-타임에러.jpg')
            assert False

                


