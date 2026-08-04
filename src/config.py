from pathlib import Path
import yaml

'''PATH SETTING'''
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DEFAULT = BASE_DIR / "config" / "config_default.yaml"
DOWNLOAD_FOLDER = BASE_DIR / "Downloads"
DOWNLOADER_PATH = BASE_DIR / "bin" / "N_m3u8DL-RE.exe"
LOGGING_PATH = BASE_DIR / "log"