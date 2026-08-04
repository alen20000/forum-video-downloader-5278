import src.engine.engine.scraper  as sc
import src.utils.logger as logger
import src.config as config
from src.engine.engine.auth_check import login_auth
if __name__ == "__main__":
    #pre-porcess
    logger.setup_logging()

    #check cookie
    if  not config.COOKIE_FILE.exists():
        print("是否需要登入狀態?[y/n] [Enter預設為y]")
        input_status = input().strip().lower()
        if input_status in ('y',''):
            login_auth()
        else:
            print("無登入狀態下，部分影片無權限進入")

    #main process
    while True:
        try:
            print('-'*60 )
            print('影片論壇網址:https://5278.cc/')
            print('-'*60 )  
            url = input("\n請輸入網址(或輸入 'q' 離開):\n ")
            
            if url.lower() == 'q':
                print("程式結束。")
                break

            scraper = sc.Scraper()
            scraper.url = input("\n請輸入網址:\n ")
            scraper.run()
        except Exception as e:
            logger.error(f'錯誤原因:{e}')