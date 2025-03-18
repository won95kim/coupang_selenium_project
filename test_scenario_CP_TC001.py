# 쿠팡 - 상품 검색 기능 테스트
# TestCaseID: CP_TC001
# 웹 크롬으로 접속 후 검색 기능 정상 작동 여부 확인

import pytest
import time
import os
import logging
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib import parse
from PIL import Image, ImageChops
from pages.main_page import MainPage
from pages.login_page import LoginPage


@pytest.mark.usefixtures("driver")
def test_scenario_001(driver: WebDriver):
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    wait = ws(driver, 10)
    product_list = "productList"

    # 로그 저장할 폴더 생성
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True) # 폴더가 없으면 생성

    # 이미지 저장 폴더 생성용
    os.makedirs("pass_img", exist_ok=True) # 폴더가 없으면 생성
    os.makedirs("fail_img", exist_ok=True) # 폴더가 없으면 생성

    log_file = os.path.join(log_dir, "TC001_test.log")
    
    # 로깅 설정 (FileHandler 사용)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # FileHandler 추가
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # 포맷 설정
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # 핸들러 등록
    logger.addHandler(file_handler)

    pass_img_path = "pass_img/"
    fail_img_path = "fail_img/"
    tc_name = "CP_TC001-"
    
    # 로그인 정보 가져오기
    account_data = login_page.load_account_data()
    EMAIL = account_data["EMAIL"]
    PASSWORD = account_data["PASSWORD"]
    NAME = account_data["NAME"]

    logger.info("CP_TC001 테스트를 시작합니다.")

    # 메인페이지 진입
    main_page.open()
    time.sleep(2)

    wait.until(EC.url_contains("coupang.com"))
    assert "coupang.com" in driver.current_url
    driver.save_screenshot(pass_img_path + tc_name + "메인페이지-진입-성공.jpg")
    logger.info("메인페이지 진입 성공")

    # Step 1
    # 쿠팡 로그인 전 "노트북" 검색
    try:
        # "노트북" 검색
        main_page.search_items("노트북")
        
        wait.until(EC.presence_of_element_located((By.ID, product_list)))

        products = driver.find_elements(By.ID, product_list)
        item_name = parse.quote("노트북")

        assert len(products) > 0
        assert item_name in driver.current_url
        driver.save_screenshot(pass_img_path + tc_name + "로그인전-노트북-검색-성공.jpg")
        logger.info("로그인전 노트북 검색 성공")
    
    except NoSuchElementException as e:  
        driver.save_screenshot(fail_img_path + tc_name + "로그인전-노트북-검색-실패-노서치.jpg")
        logger.error("로그인전 노트북 검색 실패 노서치")
        assert False
    
    except TimeoutException as e:
        driver.save_screenshot(fail_img_path + tc_name + "로그인전-노트북-검색-실패-타임에러.jpg")
        logger.error("로그인전 노트북 검색 실패 타임에러")
        assert False
    
    except Exception as e:
        driver.save_screenshot(fail_img_path + tc_name + "로그인전_노트북_검색_실패_예외.jpg")
        logger.error("로그인전 노트북 검색 실패 예외")
        assert False
    
    
    time.sleep(3)


    # Step 2
    # 쿠팡 로그인 후 "노트북" 검색
    try:
        # 로그인 페이지 진입
        login_page.open_login()
        time.sleep(2)

        wait.until(EC.url_contains("login"))
        assert "login" in driver.current_url
        driver.save_screenshot(pass_img_path + tc_name + "로그인후-로그인페이지-진입-성공.jpg")
        logger.info("로그인페이지 진입 성공")

        # 로그인 진행
        login_page.load_cookies()  # 쿠키 불러오기 (있으면 자동 로그인)
        login_page.driver.refresh()  # 페이지 새로고침 후 자동 로그인 상태 확인

        login_check = login_page.is_logged_in() # 로그인 확인
        assert NAME in login_check
        driver.save_screenshot(pass_img_path + tc_name + "로그인후-자동-로그인-성공.jpg")
        logger.info("자동 로그인 성공")

        # 쿠키 자동 로그인 실패 시 수동 로그인 진행
        if not login_check():
            logger.info("자동 로그인 실패, 수동 로그인 진행")

            login_page.input_email(EMAIL)
            login_page.input_password(PASSWORD)
            time.sleep(1)
            login_page.click_login_button()

            time.sleep(2)

            assert NAME in login_check
            driver.save_screenshot(pass_img_path + tc_name + "로그인후-수동-로그인-성공.jpg")
            logger.info("수동 로그인 성공")

            login_page.save_cookies()  # 로그인 후 쿠키 저장
        
        time.sleep(2)

        # "노트북" 검색
        main_page.search_items("노트북")
        
        wait.until(EC.presence_of_element_located((By.ID, product_list)))

        products = driver.find_elements(By.ID, product_list)
        item_name = parse.quote("노트북")

        assert len(products) > 0
        assert item_name in driver.current_url
        driver.save_screenshot(pass_img_path + tc_name + "로그인후-노트북-검색-성공.jpg")
        logger.info("로그인후 노트북 검색 성공")

    except NoSuchElementException as e:  
        driver.save_screenshot(fail_img_path + tc_name + "로그인후-노트북-검색-실패-노서치.jpg")
        logger.error("로그인후 노트북 검색 실패 노서치")
        assert False
    
    except TimeoutException as e:
        driver.save_screenshot(fail_img_path + tc_name + "로그인후-노트북-검색-실패-타임에러.jpg")
        logger.error("로그인후 노트북 검색 실패 타임에러")
        assert False
    
    except Exception as e:
        driver.save_screenshot(fail_img_path + tc_name + "로그인후_노트북_검색_실패_예외.jpg")
        logger.error("로그인후 노트북 검색 실패 예외")
        assert False
    

    time.sleep(3)


    # Step 3
    # 로그인 전/후 차이 비교
    logout_img = Image.open(pass_img_path + tc_name + "로그인전-노트북-검색-성공.jpg")
    login_img = Image.open(pass_img_path + tc_name + "로그인후-노트북-검색-성공.jpg")

    diff = ImageChops.difference(logout_img, login_img)

    # 이미지 차이 점이 있으면 PASS
    if diff.histogram():
        logger.info("이미지에 차이가 있습니다.")
        assert True
    else:
        logger.error("이미지가 동일합니다.")
        assert False


    time.sleep(3)


    # 로그아웃 진행
    login_page.click_logout_button()
    driver.save_screenshot(pass_img_path + tc_name + "로그아웃-성공.jpg")
    logger.INFO("로그아웃이 완료되었습니다.")
    
    logger.info("CP_TC001 테스트가 종료되었습니다.")



