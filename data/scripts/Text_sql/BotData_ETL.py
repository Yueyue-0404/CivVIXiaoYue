import json
import sqlite3
from pathlib import Path

import SQL_function_register as register

with open(Path.cwd().joinpath("BotData_ETL.json"), mode="r",encoding="utf8") as f:
    scripts = json.load(f)
GameplayDB = sqlite3.connect(Path("../../civ6db/DebugGameplay.sqlite").resolve())
SimplizedDB = sqlite3.connect(Path("../../civ6db/SimplizedData.sqlite").resolve())

register.register(GameplayDB)

GP_new_cursor = GameplayDB.cursor()
SP_new_cursor = SimplizedDB.cursor()

print("START!!!")
try:
    for i in scripts:
        #  往GamePlay中灌数
        with open(Path.cwd().joinpath(i), mode="r",encoding="utf8") as etl_script:
            GP_new_cursor.executescript(etl_script.read())
        GameplayDB.commit()
        #  取DDL
        GP_new_cursor.execute("select \"sql\" from sqlite_master where type = 'table' and tbl_name = ?",(i.split(".")[0],))
        ddl = "drop table if exists {};\n".format(i.split(".")[0])
        ddl += GP_new_cursor.fetchone()[0]+";"
        #  取DML
        GP_new_cursor.execute("select * from {}".format(i.split(".")[0]))
        data = GP_new_cursor.fetchall()
        dml = "insert into {} values ".format(i.split(".")[0])
        dml += ",".join([str(i).replace("None","null") for i in data])
        dml += ";"
        #  往Simplized中灌数
        SP_new_cursor.executescript(ddl)
        SP_new_cursor.executescript(dml)
        print("{} DONE!".format(i))
    print("ACCOMPLISHED!!!")
finally:
    GP_new_cursor.close()
    SP_new_cursor.close()
