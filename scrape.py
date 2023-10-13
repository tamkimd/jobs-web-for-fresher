from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from extract_data import PostScraper
import time
import os
import json

class FbScraper:
    def __init__(self, url, scroll_times=100):
        self.url = url
        self.driver = None
        self.data_list = []
        self.USER_DATA_DIR = r'F:\YT\tam\selenium\chr\tk1'
        self.SCROLL_TIMES = scroll_times

    def setup_driver(self):

        chrome_options = Options()

        # Tạo một options object và thêm tùy chọn để sử dụng profile cụ thể
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--user-data-dir=' + self.USER_DATA_DIR)
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument(
            '--disable-gpu') if os.name == 'nt' else None
        chrome_options.add_argument("--verbose")
        chrome_options.add_argument("--no-default-browser-check")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument(
            "--disable-feature=IsolateOrigins,site-per-process")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--ignore-certificate-error-spki-list")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControllered")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        self.driver = webdriver.Chrome(
            options=chrome_options, service=Service(
                ChromeDriverManager().install())
        )

    def wait_for_page_to_load(self, max_time=10):
        wait = WebDriverWait(self.driver, max_time)
        wait.until(lambda driver: self.driver.execute_script(
            'return document.readyState;') == 'complete')

    def scroll_down(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        for _ in range(self.SCROLL_TIMES):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.2)

    def click_xem_them_buttons(self):
        self.driver.execute_script("""
        const xemThemButtons = document.querySelectorAll('.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.xt0b8zv.xzsf02u.x1s688f[role="button"][tabindex="0"]');
        for (const button of xemThemButtons) {
            button.click();
        }""")

    def scrape_data(self):
        self.driver.get(self.url)
        self.wait_for_page_to_load()
        self.scroll_down()
        self.click_xem_them_buttons()
        elements = self.driver.find_elements(
            By.CLASS_NAME, "x1yztbdb.x1n2onr6.xh8yej3.x1ja2u2z")
        post_list = []
        for element in elements:
            html_content = element.get_attribute("innerHTML")
            post_scraper = PostScraper(html_content=html_content)
            post_data = post_scraper.scrape_post_data()
            print(post_data)
            post_list.append(post_data)
        with open('post_data.json', 'w', encoding='utf-8') as json_file:
            json.dump(post_list, json_file, ensure_ascii=False, indent=4)
        
        self.quit_driver()

    def quit_driver(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    scraper = FbScraper(
        url="https://www.facebook.com/groups/368698476630471/search?q=FRESHER&filters=eyJycF9jaHJvbm9_fc29ydDowIjoie1wibmFtZVwiOlwiY2hyb25vc29ydFwiLFwiYXJnc1wiOlwiXCJ9In0%3D")
    scraper.setup_driver()
    scraper.scrape_data()
