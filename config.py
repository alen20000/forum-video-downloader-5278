from pathlib import Path


BATH_DIR = Path(__file__).resolve().parent

DOWNLOAD_FOLDER = BATH_DIR / "Downloads"


DONLOADER_PATH = BATH_DIR / "bin" / "N_m3u8DL-RE.exe"


DEPENDENCIES={
    "N_m3u8DL-RE":{
        "url":"https://github.com/nilaoda/N_m3u8DL-RE/releases/download/v0.5.1-beta/N_m3u8DL-RE_v0.5.1-beta_win-x64_20251029.zip",
        "saving_path":DONLOADER_PATH
    }
}

if __name__ =="__main__":
    
    print(DONLOADER_PATH)
    pass