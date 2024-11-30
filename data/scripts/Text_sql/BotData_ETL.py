import sqlite3
import json
from pathlib import Path
import SQL_function_register as register

with open(Path.cwd().joinpath("BotData_ETL.json"), mode="r") as f:
    scripts = json.load(f)
DB = sqlite3.connect(Path("../../civ6db/DebugGameplay.sqlite").resolve())
register.register(DB)
new_cursor = DB.cursor()
print("START!!!")
try:
    for i in scripts:
        with open(Path.cwd().joinpath(i), mode="r") as etl_script:
            new_cursor.executescript(etl_script.read())
            print("{} DONE!".format(i))
    DB.commit()
    print("ACCOMPLISHED!!!")
finally:
    new_cursor.close()
