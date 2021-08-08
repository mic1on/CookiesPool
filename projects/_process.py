import json
from loguru import logger
from db import RedisClient


class Process(object):
    """
    处理登录和心跳逻辑
        run_login()
            从Redis中获取未获取cookie的账号进行登录，子类实现登录功能
        run_heart()
            从Redis中获取存在的cookie进行检测是否有效，子类实现心跳功能
    """

    def __init__(self, site):
        self.site = site
        self.accounts_db = RedisClient('accounts', self.site)
        self.cookies_db = RedisClient('cookies', self.site)

    def login(self, username, password):
        """
        外部子类实现login登录方法
        :param username: 用户名
        :param password: 密码
        :return: dict

        登录存在三种可能：
            1.登录成功
                { 'status': 1, 'cookies': 'cookies' }
            2.登录失败
                pass = 重试
            3.密码错误
                { 'status': -1, 'cookies': None }
        """
        raise NotImplementedError

    def heart(self, username, cookies):
        """
        外部子类实现heart心跳方法
        :param username: 用户名
        :param cookies:
        :return: True/False

        心跳刷新存在两种可能：
            1.心跳成功
                True
            2.心跳失败
                False
                cookie失效，在 cookie_db 中删除username
                self.cookies_db.delete(username)
        """
        raise NotImplementedError

    def process_cookies(self, cookies: list):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        dict = {}
        for cookie in cookies:
            dict[cookie['name']] = cookie['value']
        return dict

    def run_login(self):

        # 取得所有账号及账号的cookies
        accounts_usernames = self.accounts_db.usernames()
        cookies_usernames = self.cookies_db.usernames()

        for username in accounts_usernames:
            if username not in cookies_usernames:
                # 用户如果不在cookies集合中，那么就需要登录
                password = self.accounts_db.get(username)
                logger.info(f'正在生成账号{username}的cookies')
                res = self.login(username, password)
                if res.get('status') == 1:
                    cookies = self.process_cookies(res.get('cookies', []))
                    self.cookies_db.set(username, json.dumps(cookies))
                elif res.get('status') == -1:
                    self.accounts_db.delete(username)
                else:
                    pass
        # else:
        #     logger.info("所有账号cookie获取完毕！")

    def run_heart(self):
        cookies_groups = self.cookies_db.all()
        for username, cookies in cookies_groups.items():
            res = self.heart(username, cookies)
            if res:
                logger.info(f"{username}的cookies有效")
            else:
                logger.debug(f"{username}的cookies失效，已删除")
                self.cookies_db.delete(username)
