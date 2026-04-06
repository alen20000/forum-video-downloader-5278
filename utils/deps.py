import os
import config
from pathlib import Path
import logging

class DeployDep:
    

    def __init__(self):
        
        self.save_path = config.DOWNLOAD_FOLDER


    def setup_enviroment(self):
        self._ensure_folder()
        self._ensure_N_m3u8DL_RE()

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

    def _ensure_N_m3u8DL_RE(self):
        try:
            if not config.DONLOADER_PATH.exists():
                print("[!]尚未依賴 N_m3u8DL-RE ")
                print("[。]自動部屬依賴 N_m3u8DL-RE ")
                
                #自動抓取
                self._download_dependency()
            else:
                pass
        except OSError as e:
            logging.error(f'建立失敗:{e}')
            raise

    def _download_dependency(self) -> None:
        import requests
        import zipfile
        import io
        info = config.DEPENDENCIES.get("N_m3u8DL-RE")
        target_url = info.get("url")
        saving_path = info.get("saving_path")

        try:
            response = requests.get(target_url, timeout=60, stream=True)
            response.raise_for_status()

            zip_data = io.BytesIO(response.content) #直接抓到記憶體

            with zipfile.ZipFile(zip_data) as z:
                '''
                下面那排語法我看不太懂，直接抄
                功能:尋找zip 內的 exe 

                '''
                exe_name = next((f for f in z.namelist() if f.endswith(".exe")), None)

                if exe_name:
                    # 直接讀取該檔案內容並寫入到你的 config.DONLOADER_PATH
                    with open(saving_path, "wb") as f:
                        f.write(z.read(exe_name))
                    print(f"[+] 部署成功: {saving_path}")
                else:
                    raise FileNotFoundError("壓縮檔內找不到執行檔 (.exe)")
                

        except Exception as e:
            print(f"[!]下載失敗:{e}")
            raise

if __name__ == "__main__":
    deploy = DeployDep()
    deploy.setup_enviroment()
