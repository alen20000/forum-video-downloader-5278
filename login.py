from playwright.sync_api import sync_playwright
import config
from pathlib import Path
'''
功能:抓登入cookie
成功登入後，cookie會在存在根目錄的.sessions
'''
def save_auth():
    with sync_playwright() as p:
        # 記得 headless=False 才能手動操作登入
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://5278.cc/")
        
        # --- 這裡手動輸入帳密並點擊登入 ---
        print("請在瀏覽器中完成登入...")
        
        # 登入介面停留時間
        page.wait_for_timeout(30000)  
        
        # 將登入狀態（Cookies, LocalStorage）儲存起來
        context.storage_state(path=config.COOKIE_FILE)
        print(f"登入狀態已保存至 {config.COOKIE_FOILDER}")
        browser.close()


if __name__ =="__main__":
    save_auth()
