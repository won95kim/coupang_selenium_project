import pytest
import time
import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from pages.main_page import MainPage
from urllib import parse


@pytest.mark.usefixtures("driver")
class TestMainPage:
    # 메인 페이지 진입 확인
    #@pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_open_main_page(self, driver: WebDriver):
        try:
            login_page = MainPage(driver)
            login_page.open()

            time.sleep(2)

            wait = ws(driver, 10)   # 최대 10초까지 기다림
            wait.until(EC.url_contains('coupang.com'))    # url에 login이 포함되는지 확인
            assert 'coupang.com' in driver.current_url    # 로그인 페이지로 정상 이동되었는지 확인

            os.makedirs('pass_img', exist_ok=True)  # 폴더 없으면 생성
            driver.save_screenshot('pass_img/메인페이지-진입-성공.jpg')
        
        except NoSuchElementException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/메인페이지-진입-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            os.makedirs('fail_img', exist_ok=True)
            driver.save_screenshot('fail_img/메인페이지-진입-실패-타임에러.jpg')
            assert False


    # 검색어 입력 확인
    @pytest.mark.skip(reason="아직 테스트 케이스 발동 안함")
    def test_search_items(self, driver: WebDriver):
        try:    
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()

            time.sleep(2)

            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("coupang.com")) #URL 검증
            assert "coupang.com" in driver.current_url #검증 
        
            time.sleep(2) #2초 왜? 봇인거 안들키기 위해서 
        
            main_page.search_items('노트북')

            ws(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')

            # 상품이 1개 이상이면 성공
            assert len(items) > 0
            assert item_name in driver.current_url
            
            driver.save_screenshot('메인페이지-검색-성공.jpg')
        except NoSuchElementException as e:
            driver.save_screenshot('메인페이지-검색-실패-노서치.jpg')
            assert False

        except TimeoutException as e:
            driver.save_screenshot('메인페이지-검색-실패-타임에러.jpg')
            assert False