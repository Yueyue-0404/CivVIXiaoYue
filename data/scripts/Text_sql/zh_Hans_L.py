"""
    该脚本用于
        1. 将游戏文件夹中的xml文本文件跑入 DebugLocalization.sqlite 库中本不存在的表 zh_Hans_Text
        2. 生成一个数据迁移脚本
"""

from lxml import etree
from pathlib import Path
import sqlite3

TEXT_DIR = Path("./data/text").resolve()
print(TEXT_DIR)
DB_Path = Path("./data/civ6db/DebugLocalization.sqlite").resolve()
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
        new_cursor.execute("create table if not exists zh_Hans_Text (Tag TEXT,Text TEXT,Gender TEXT,Plurality TEXT,primary key(Tag,Text))")
        new_cursor.close()
        for i in file_list:
            if not i.is_dir() and i.suffix == ".xml":
                f(i)
    return wrapper


@recursionOperation
def operate(file: Path):
    new_cursor = DB.cursor()
    try:
        with open(file, mode="r") as f:
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
    with open(Path("./data/scripts/zh_Hans_Text.sql"), mode="w") as sql:
        sql.write("drop table if exists zh_Hans_Text;\n")
        sql.write("create table if not exists zh_Hans_Text (Tag TEXT,Text TEXT,Gender TEXT,Plurality TEXT,primary key(Tag,Text));\n")
        new_cursor = DB.cursor()
        try:
            new_cursor.execute("select * from zh_Hans_Text")
            res = new_cursor.fetchall()
            for i in res:
                insert_sql = "insert into zh_Hans_Text values ('{}',{},null,null);\n".format(i[0], i[1].replace("\n", "\\n").join(("'","'")) if i[1] else 'null')
                sql.write(insert_sql)
        finally:
            new_cursor.close()


operate(TEXT_DIR)
generateScript()
