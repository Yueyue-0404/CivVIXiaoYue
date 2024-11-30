from pathlib import Path

BASE_DIR = Path.cwd().resolve()
BASIC_DIR = BASE_DIR.joinpath("basic")
CONFIG_DIR = BASE_DIR.joinpath("config")
DATA_DIR = BASE_DIR.joinpath("data")
CIVVI6DB_DIR = DATA_DIR.joinpath("civ6db")
RSS_DIR = BASE_DIR.joinpath("resources")

KEYWORD_SIMILARITY = 75  # 这个是规定有百分之多少相似度的拼音才识别为错别字
