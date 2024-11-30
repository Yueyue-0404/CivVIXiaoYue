from pathlib import Path

BASE_DIR = Path.cwd().resolve()
BASIC_DIR = BASE_DIR.joinpath("basic")
CONFIG_DIR = BASE_DIR.joinpath("config")
DATA_DIR = BASE_DIR.joinpath("data")
CIVVI6DB_DIR = DATA_DIR.joinpath("civ6db")
