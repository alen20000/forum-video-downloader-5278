import logging
import src.config as config


class DeployDep:
    '''
    安裝依賴
    '''

    def __init__(self):
        
        self.save_path = config.DOWNLOAD_FOLDER
        self.config_dev = None

    def run(self):
        #檢查"bin"資料夾
        if not config.DOWNLOADER_FOLDER_PATH.exists():
            config.DOWNLOADER_FOLDER_PATH.mkdir(parents=True, exist_ok=True)
        #檢查是否安裝，沒有則跳出
        if not config.DOWNLOADER_FILE_PATH.exists():
            logging.info("[!]尚未必要依賴依賴，開始部屬『N_m3u8DL-RE』 ")

            import requests
            import zipfile
            import io
            from src.utils.common import load_ymal
            # 讀取 config
            self.config_dev = load_ymal(config.CONFIG_DEV)
            binary_url = self.config_dev['N_m3u8DL-RE']['download_link']

            try:
                res = requests.get(binary_url)
                #若狀態不對，會跳到最近的excep，或直接報錯。主要是避免抓到空檔案然後還解壓縮
                res.raise_for_status()
                #下載的檔案直接給記憶體，不給實體地址
                zip_data = io.BytesIO(res.content)
                #在記憶體曾用zip解壓
                with zipfile.ZipFile(zip_data) as z:
                    #把符合exe檔名的檔案取出；neext為只取第一個
                    exe_name = next((f for f in z.namelist() if f.endswith(".exe")), None)

                    if exe_name:
                        with open(config.DOWNLOADER_FILE_PATH, "wb") as f:
                            f.write(z.read(exe_name))

                        return True
                    else:
                        raise FileNotFoundError("壓縮檔內找不到執行檔 (.exe)")
            except Exception as e:
                logging.error(f'下載失敗，錯誤原因:{e}')
                return False
        #不需要安裝依賴
        else:
            return False 

