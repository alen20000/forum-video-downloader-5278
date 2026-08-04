import src.engine.engine.scraper 
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
    testing_url = "https://5278.cc/forum.php?mod=viewthread&tid=1711330&extra=page%3D1"
    scraper = src.engine.engine.scraper.Scraper()
    scraper.url = testing_url
    scraper.run()