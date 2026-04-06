import os
import config
from pathlib import Path
import logging

class DeployDep:
    

    def __init__(self):
        
        self.save_path = config.DOWNLOAD_FOLDER


    def setup_enviroment(self):
        self._ensure_folder()

    def _ensure_folder(self):
        try:
            if not self.save_path.exists():
                self.save_path.mkdir(parents=True, exist_ok=True)
                print("未發現下載資料夾，建立資料夾。。。")
            else:
                pass
        except OSError as e:
            logging.error(f'建立失敗:{e}')
            raise

if __name__ == "__main__":
    deploy = DeployDep()
    deploy.setup_enviroment()
