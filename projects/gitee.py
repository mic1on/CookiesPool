import time

from loguru import logger
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from projects._process import Process
from tools.selenium_reality import SeleniumReality


class Gitee(Process):
    """实现一个GitHub的登录"""

    def __init__(self, site):
        self.site = site
        super().__init__(self.site)

        self.url = "https://gitee.com/login"
        self.browser = None
        self.wait = None

    def before_login(self, username, password):
        self.browser.delete_all_cookies()
        self.browser.get(self.url)
        el_username = self.wait.until(EC.presence_of_element_located((By.ID, 'user_login')))
        el_password = self.wait.until(EC.presence_of_element_located((By.ID, 'user_password')))
        el_submit = self.wait.until(EC.element_to_be_clickable((By.NAME, 'commit')))
        el_username.send_keys(username)
        el_password.send_keys(password)
        el_submit.click()

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'session__2verify'))))
        except TimeoutException:
            return False

    def login(self, username, password):
        logger.info(f"我准备使用{username}，{password}来进行登录")
        # 具体ccgp是如何登录的
        sr = SeleniumReality()
        self.browser = sr.browser
        self.wait = WebDriverWait(self.browser, 20)

        self.before_login(username, password)

        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.browser.get_cookies()
            logger.info(f"cookies{cookies}")
            return {
                'status': 1,
                'cookies': cookies
            }

    def heart(self, username, cookies):
        logger.info(f"我准备使用{username}，{cookies}来进行心跳")
        return False
