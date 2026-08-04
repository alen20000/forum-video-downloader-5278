from pathlib import Path
import yaml
import src.config as config




def load_ymal(file_path: Path) -> dict:
    if not file_path.exists():
        raise FileNotFoundError(f"""找不到配置文件:{file_path}""")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}