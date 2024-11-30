"""
    该脚本用于
        1. 将游戏文件夹中的xml文本文件跑入 DebugLocalization.sqlite 库中本不存在的表 zh_Hans_Text
        2. 生成一个数据迁移脚本
"""

import sqlite3
from pathlib import Path

from lxml import etree

TEXT_DIR = Path("../../text").resolve()
DB_Path = Path("../../civ6db/DebugLocalization.sqlite").resolve()
DB = sqlite3.connect(DB_Path)


def sort_key(file: Path):
    if file.name == 'Vanilla_zh_Hans_CN.xml':
        return 1
    elif file.name == 'Expansion1':
        return 2
    elif file.name == 'Expansion2':
        return 3
    else:
        return 4


def recursionOperation(f):
    def wrapper(dir_path: Path):
        if not dir_path.is_dir():
            raise ValueError("Directory expected!")
        file_list = list(dir_path.rglob("*"))
        file_list.sort(key=sort_key)
        print("\nSTART!!!")
        new_cursor = DB.cursor()
        new_cursor.execute("drop table if exists zh_Hans_Text")
        new_cursor.execute("create table if not exists zh_Hans_Text (id int);")
        new_cursor.execute("drop table if exists zh_Hans_Text")
        new_cursor.execute("create table if not exists zh_Hans_Text (Tag TEXT primary key,Text TEXT,Gender TEXT,Plurality TEXT);")
        new_cursor.close()
        for i in file_list:
            if not i.is_dir() and i.suffix == ".xml":
                f(i)
        print("FINISHED")
    return wrapper


@recursionOperation
def operate(file: Path):
    new_cursor = DB.cursor()
    try:
        with open(file, mode="r",encoding="utf-8") as f:
            print("PARSING {}...".format(str(file).replace(str(TEXT_DIR), "", 1)), end=" ")
            content = f.read()
            try:
                e_obj = etree.XML(content)
            except ValueError:
                e_obj = etree.XML(content.encode("utf-8"))
            matches = e_obj.xpath("/GameData/LocalizedText/*")
            for i in matches:
                if i.tag == "Delete" and i.get("Language") == 'zh_Hans_CN':
                    basic_sql = "delete from zh_Hans_Text where Tag = ?;"
                    new_cursor.execute(basic_sql, (i.get("Tag"),))
                elif i.tag == "Replace" and i.get("Language") == 'zh_Hans_CN':
                    basic_sql = "insert or replace into zh_Hans_Text values (?,?,null,null);"
                    new_cursor.execute(basic_sql, (i.get("Tag"), i.find("Text").text))
                else:
                    pass
            print(" DONE!")
        DB.commit()
    finally:
        new_cursor.close()



def generateScript():
    with open(Path("./zh_Hans_Text.sql"), mode="w",encoding="utf-8") as sql:
        sql.write("drop table if exists zh_Hans_Text;\n")
        sql.write("create table if not exists zh_Hans_Text (id int);\n")
        sql.write("drop table if exists zh_Hans_Text;\n")
        sql.write("create table if not exists zh_Hans_Text (Tag TEXT primary key,Text TEXT,Gender TEXT,Plurality TEXT);\n")
        new_cursor = DB.cursor()
        try:
            new_cursor.execute("select * from zh_Hans_Text")
            res = new_cursor.fetchall()
            insert_sql = "insert into zh_Hans_Text values "
            for i in res:
                insert_sql += "('{}',{},null,null),\n".format(i[0], i[1].replace("\n", "\\n").replace("\'", "\'\'").join(("'","'")) if i[1] else 'null')
            insert_sql = insert_sql[:-2] + ";"
            sql.write(insert_sql)
        finally:
            new_cursor.close()

def loadIntpSimplizedDB():
    if Path("./zh_Hans_Text.sql").exists():
        new_cursor = sqlite3.connect(Path("../../civ6db/SimplizedData.sqlite").resolve()).cursor()
        try:
            with open(Path("./zh_Hans_Text.sql"), mode="r", encoding="utf-8") as sql_file:
                sql = sql_file.read()
                new_cursor.executescript(sql)
        finally:
            new_cursor.close()

        new_cursor = sqlite3.connect(Path("../../civ6db/DebugGameplay.sqlite").resolve()).cursor()
        try:
            with open(Path("./zh_Hans_Text.sql"), mode="r", encoding="utf-8") as sql_file:
                sql = sql_file.read()
                new_cursor.executescript(sql)
        finally:
            new_cursor.close()
    else:
        raise FileNotFoundError


operate(TEXT_DIR)
generateScript()
loadIntpSimplizedDB()
