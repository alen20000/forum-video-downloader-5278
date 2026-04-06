from pathlib import Path


BATH_DIR = Path(__file__).resolve().parent

DOWNLOAD_FOLDER = BATH_DIR / "Downloads"


DONLOADER_PATH = BATH_DIR / "bin" / "N_m3u8DL-RE"


if __name__ =="__main__":
    
    print(DONLOADER_PATH)
    pass