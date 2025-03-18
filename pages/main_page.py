from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class MainPage:
    URL = "https://www.coupang.com"
    SEARCH_INPUT_ID = "headerSearchKeyword"

    #객체 -> 인스턴스화 \ 제가 원하는 설정으로 셋업 하는 함수
    def __init__(self, driver: WebDriver): #
        self.driver = driver


    #메인 페이지 열기
    def open(self):
        self.driver.get(self.URL)
    

    # 검색어 입력
    def search_items(self, item_name: str):
        search_input_box = self.driver.find_element(By.ID, self.SEARCH_INPUT_ID)
        search_input_box.send_keys(item_name)
        search_input_box.send_keys(Keys.ENTER)


    # 버튼 클릭
    def click_by_LINK_TEXT(self, link_text: str):
        login_button = self.driver.find_element(By.LINK_TEXT, link_text)
        login_button.click()


    # 입력값 순차로 입력
    def search_text_input(self, item_name: str, pause_between_chars=4):
        """item_name 을 자모 단위(또는 영문자)로 순차 입력하며 타이핑"""
        search_input_box = self.driver.find_element(By.ID, self.SEARCH_INPUT_ID)
        # 1) ActionChains 객체 생성
        actions = ActionChains(self.driver)
        # 2) 검색창을 클릭하여 포커스 이동
        #    (이미 포커스가 가 있다면 생략 가능)
        actions.move_to_element(search_input_box).click().pause(0.1)
        # 3) item_name의 각 글자를 순차 입력 + 글자마다 잠시 pause
        for char in item_name:
            actions.send_keys(char).pause(pause_between_chars)
        # 4) 한 번에 실행
        actions.perform()


    # 마우스로 이동
    def search_text_enter(self):
        search_input_box = self.driver.find_element(By.ID, self.SEARCH_INPUT_ID)
        actions = ActionChains(self.driver)
        actions.move_to_element(search_input_box).click().pause(0.1)
        actions.send_keys(Keys.ENTER)
        actions.perform()

    