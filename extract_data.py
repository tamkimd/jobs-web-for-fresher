from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from html import unescape
import re


class PostScraper:
    TIME_CLASS = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xt0b8zv xo1l8bm"
    IMG_CLASS = "x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3"
    USER_CLASS = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f"
    POST_TEXT_CLASS = "x1iorvi4 x1pi30zi"
    POST_TEXT_CLASS2 = "x5yr21d xyqdw3p"

    def __init__(self, html_content=None, file_path=None):
        self.html_content = html_content
        self.file_path = file_path
        self.html = self._read_html()

        if html_content is not None:
            self.soup = BeautifulSoup(self.html_content, 'html.parser')
        else:
            self.soup = BeautifulSoup(self.html, 'html.parser')

    def _read_html(self):
        if self.file_path is not None:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return file.read()
        return ""

    @staticmethod
    def calculate_post_age(time_str):
        # Lấy thời gian hiện tại
        now = datetime.now()

        # Kiểm tra nếu giá trị thời gian là "vừa xong" hoặc "x giây"
        if time_str == "vừa xong" or re.match(r'\d+\s*giây', time_str):
            return now

        # Sử dụng regex để tìm xem có số và đơn vị thời gian nào trong chuỗi
        match = re.match(r'(\d+)\s*(phút|giờ|ngày)', time_str)
        if match:
            amount = int(match.group(1))
            unit = match.group(2)
            if unit == "phút":
                delta = timedelta(minutes=amount)
            elif unit == "giờ":
                delta = timedelta(hours=amount)
            elif unit == "ngày":
                delta = timedelta(days=amount)
            return (now - delta).strftime("%Y-%m-%d %H:%M:%S")

        return None  # Trả về None nếu không nhận diện được định dạng

    def scrape_post_data(self):
        user_class = " ".join(self.USER_CLASS.split())
        user = self.soup.find(class_=user_class)
        if user is not None:
            user_link = self.extract_user_link(user)
            name = user.text
        else:
            user_link = None
            name = None

        time_html = self.soup.find("a", class_=self.TIME_CLASS)
        if time_html is not None:
            time = time_html.get('aria-label')
            time = self.calculate_post_age(time)
            post_link = time_html.get('href').split("/?")[0]
        else:
            time = None
            post_link = None

        img_src_list = []
        try:
            img_html = self.soup.select(f"img[class='{self.IMG_CLASS}']")
            img_src_list = [unescape(img["src"]) for img in img_html]
        except Exception as e:
            print(f"Error processing images: {str(e)}")

        divs_with_dir_auto = self.soup.find_all('div', dir='auto', style=False)
        post_text = ""
        for div in divs_with_dir_auto:
            post_text = post_text + div.text
        post_text = re.sub(r'\s+', ' ', post_text).strip()

        return {
            "post_link": post_link,
            "time": time,
            "post_text": post_text,
            "name": name,
            "user_link": user_link,
            "img_src_list": img_src_list
        }

    @staticmethod
    def extract_user_link(user_tag):
        if user_tag is not None:
            link = user_tag.get('href', "").split("/?")[0]
            link = f"https://www.facebook.com{link}"

            return link
        return None

