from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from db import RedisClient


class ChromeReality(object):

    def __init__(self):
        # 配置真实浏览器环境
        # self.chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 1. 指定本地浏览器绝对路径
        # self.remote_debugging_port = random.randint(9222, 9999)  # 2. 指定浏览器启动端口
        self.user_data_dir = r'C:\Users\Administrator\Desktop\SeleniumUserData'  # 3. 指定浏览器的UserDataDir
        # 启动真实浏览器
        # subprocess.Popen([
        #     self.chrome_path,
        #     f'--remote-debugging-port={self.remote_debugging_port}',
        #     f'--user-data-dir={self.user_data_dir}'
        # ], shell=True)
        # 初始化浏览器参数以及接管真实浏览器
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
        # self.chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{self.remote_debugging_port}")
        self.browser = webdriver.Chrome(options=self.chrome_options)
        # 写入防止检测ChromeDriver
        # with open('stealth.min.js') as f:
        #     js = f.read()
        #
        # self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source": js
        # })

    def __del__(self):
        try:
            self.browser.close()
        except TypeError:
            pass


class SeleniumReality(ChromeReality):

    def __init__(self):
        super().__init__()
        # self.cookies_db = RedisClient('cookies', self.site)
        # self.accounts_db = RedisClient('accounts', self.site)

