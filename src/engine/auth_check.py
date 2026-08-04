from playwright.sync_api import sync_playwright
from pathlib import Path
import src.config as config_path
from src.utils.common import load_ymal
import logging
from src.utils.block import apply_extreme_filter
'''
功能:抓登入cookie
成功登入後，cookie會在存在根目錄的.sessions
'''
def login_auth():
    '''
    功能:登入帳號
    '''
    with sync_playwright() as p:
        # 讀取 config
        config = load_ymal(config_path.CONFIG_DEFAULT)

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.route("**/*", apply_extreme_filter)
        page.goto(config['url']['5278_site'])
        
        logging.info("等待使用者手動登入")
        print("輸入完帳號按下登入(螢幕會靜止)，按 Enter 後繼續...")
        input()  # 程式會在這裡暫停，直到你按下 Enter

        logging.info("使用者確認登入完成，繼續執行")
        page.wait_for_timeout(2000)
        config_path.COOKIE_FOILDER.mkdir(parents=True, exist_ok=True)

        #儲存 storage_state 裡面包含登auth狀態
        context.storage_state(path=config_path.COOKIE_FILE)
        if  config_path.COOKIE_FILE.exists():
            logging.info(f"登入狀態已保存至 {config_path.COOKIE_FOILDER}")
        else:
            logging.info(f"登入狀態保存失敗")
        browser.close()


