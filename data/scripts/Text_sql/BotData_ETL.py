import json
import sqlite3
from pathlib import Path

import SQL_function_register as register
from new_print import *

with open(Path.cwd().joinpath("BotData_ETL.json"), mode="r",encoding="utf8") as f:
    scripts = json.load(f)
with open(Path.cwd().joinpath("BotData_L.json"), mode="r", encoding="utf8") as f:
    tables_need_to_load = json.load(f)
GameplayDB = sqlite3.connect(Path("../../civ6db/DebugGameplay.sqlite").resolve())
SimplizedDB = sqlite3.connect(Path("../../civ6db/SimplizedData.sqlite").resolve())

register.register(GameplayDB)

GP_new_cursor = GameplayDB.cursor()
SP_new_cursor = SimplizedDB.cursor()

try:
    # 先清库
    SP_new_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [i[0] for i in SP_new_cursor.fetchall()]
    for i in tables:
        SP_new_cursor.execute("drop table if exists {}".format(i))

    # 这些是跑数的
    print("ETL START!!!")
    for i in scripts:
        #  往GamePlay中灌数
        sql_script_path = Path.cwd().joinpath("BotData").joinpath(i)
        if not sql_script_path.exists():
            new_print("{}不存在！！！".format(sql_script_path),color=RED)
            break
        with open(sql_script_path, mode="r",encoding="utf8") as etl_script:
            GP_new_cursor.executescript(etl_script.read())
        GameplayDB.commit()
        #  取DDL
        GP_new_cursor.execute("select \"sql\" from sqlite_master where type = 'table' and tbl_name = ?", (i.split(".")[0],))
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
    print("ETL ACCOMPLISHED!!!")

    print("="*50)
    # 这些是只进行数据转移的
    print("DATA LOADING START!!!")
    for i in tables_need_to_load:
        #  检查是否有数据，没数据的不迁移
        GP_new_cursor.execute("select 1 from {}".format(i.split(".")[0]))
        if not GP_new_cursor.fetchone():
            continue
        #  取DDL
        GP_new_cursor.execute("select \"sql\" from sqlite_master where type = 'table' and tbl_name = ?",(i.split(".")[0],))
        ddl = "drop table if exists BotData_{};\n".format(i.split(".")[0])
        ddl += GP_new_cursor.fetchone()[0].replace("CREATE TABLE \"", "CREATE TABLE \"BotData_") + ";"
        #  取DML
        GP_new_cursor.execute("select * from {}".format(i.split(".")[0]))
        data = GP_new_cursor.fetchall()
        dml = "insert into BotData_{} values ".format(i.split(".")[0])
        dml += ",".join([str(i).replace("None", "null") for i in data])
        dml += ";"
        #  往Simplized中灌数
        SP_new_cursor.executescript(ddl)
        SP_new_cursor.executescript(dml)
        print("{} DONE!".format(i))
    print("DATA LOADING ACCOMPLISHED!!!")
finally:
    GP_new_cursor.close()
    SP_new_cursor.close()
