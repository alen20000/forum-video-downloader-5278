from pathlib import Path
import yaml

#PATH
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "settings.yaml"


def load_ymal(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"""找不到配置文件:{file_path}""")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}