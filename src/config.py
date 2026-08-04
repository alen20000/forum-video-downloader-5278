from pathlib import Path
import yaml

'''PATH SETTING'''
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DEFAULT = BASE_DIR / "config" / "config_default.yaml"
CONFIG_DEV = BASE_DIR / "config" / "config_dev.yaml"
DOWNLOAD_FOLDER = BASE_DIR / "Downloads"
DOWNLOADER_FOLDER_PATH = BASE_DIR / "bin"
DOWNLOADER_FILE_PATH = BASE_DIR / "bin" / "N_m3u8DL-RE.exe"
LOGGING_PATH = BASE_DIR / "log"
COOKIE_FOILDER = BASE_DIR / ".sessions"
COOKIE_FILE = COOKIE_FOILDER / 'auth.json'
