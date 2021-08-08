import time
from multiprocessing import Process
from loguru import logger
from settings import *
from utils import import_object


def run_login():
    logger.info("开启登录监控")
    while True:
        for site, lib in PROJECTS.items():
            # 导入包，传入项目网站，启动登录
            import_object(lib)(site).run_login()
        time.sleep(LOGIN_DELAY)


def run_heart():
    logger.info("开启心跳监控")
    while True:
        for site, lib in PROJECTS.items():
            import_object(lib)(site).run_heart()
        time.sleep(HEART_DELAY)


if __name__ == '__main__':
    login_process = Process(target=run_login)
    login_process.start()

    heart_process = Process(target=run_heart)
    heart_process.start()
