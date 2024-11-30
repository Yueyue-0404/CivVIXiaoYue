import re
import sqlite3
from pathlib import Path

import pypinyin

DB = sqlite3.connect(Path("../../civ6db/SimplizedData.sqlite"))
new_cursor = DB.cursor()
try:
    new_cursor.execute("select * from BotData_Alias")
    alias = new_cursor.fetchall()
finally:
    new_cursor.close()


def deleteLettersAndNumbersFromKeyword(keyword: str):
    """
        该函数:
            # 已弃用： 1. 剔除字符串中的英文字符
            2. pypinyin.lazy_pinyin处理
            3. 通过for循环来找出哪个元素是拼音，哪个元素是杂鱼，并把拼音重新串起来
    """
    # re_res = re.search("[A-Za-z\d]", keyword)
    # if re_res:
    #     keyword = re.sub("[A-Za-z\d]", "", keyword)
    keyword_pinyin_list = pypinyin.lazy_pinyin(keyword)
    return "".join([i for i in keyword_pinyin_list if re.search("[A-Za-z]",i)])


alias_pinyin_dict = {}
alias_dict = {}
for i in alias:
    kw = i[2]
    kw_pinyin = deleteLettersAndNumbersFromKeyword(kw)
    kw_pinyin_length = len(kw_pinyin)
    if kw_pinyin_length not in alias_dict:
        alias_dict[kw_pinyin_length] = [kw]
        alias_pinyin_dict[kw_pinyin_length] = [kw_pinyin]
    else:
        alias_dict[kw_pinyin_length].append(kw)
        alias_pinyin_dict[kw_pinyin_length].append(kw_pinyin)


import json
from pathlib import Path
def write_into_json(json_path: Path, data: dict or list):
    with open(json_path, mode="w",encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4,)

json_dir = Path("../..").resolve()
print("请确认路径，json将存储在该目录下：")
input(json_dir)
write_into_json(json_dir.joinpath("alias_dict.json"),alias_dict)
write_into_json(json_dir.joinpath("alias_pinyin_dict.json"),alias_pinyin_dict)
