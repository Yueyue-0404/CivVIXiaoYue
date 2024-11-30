import re
import sqlite3

import json
import yaml

#  todo 该代码仅限调试时用，正式上线时只保留 上半 的内容
if __name__ != '__main__':
    from .model import CivDataDict
    from .settings import *

    with open(CONFIG_DIR.joinpath("table.yaml")) as file:
        table_dict = yaml.safe_load(file)
    with open(CONFIG_DIR.joinpath("unitdata.json"), mode="r") as file:
        unit_info_dict = json.load(file)
    with open(CONFIG_DIR.joinpath("improvementdata.json"), mode="r") as file:
        improvement_info_dict = json.load(file)
else:
    from settings import *
    from model import CivDataDict

    CIVVI6DB_DIR = Path("/home/tarena/Yueyue/PyCharmProject/Own/qqbot/CivVIXiaoYue/data/civ6db")
    CONFIG_DIR = Path("/home/tarena/Yueyue/PyCharmProject/Own/qqbot/CivVIXiaoYue/config")
    # todo 该代码调试时缩进，正式上线时退格
    with open(CONFIG_DIR.joinpath("table.yaml"), mode="r") as file:
        table_dict = yaml.safe_load(file)
    with open(CONFIG_DIR.joinpath("unitdata.json"), mode="r") as file:
        unit_info_dict = json.load(file)
    with open(CONFIG_DIR.joinpath("improvementdata.json"), mode="r") as file:
        improvement_info_dict = json.load(file)


class DataAccesser:
    def __init__(self):
        self.confDB = sqlite3.connect(CIVVI6DB_DIR.joinpath("DebugConfiguration.sqlite"))
        self.GamePlayDB = sqlite3.connect(CIVVI6DB_DIR.joinpath("DebugGameplay.sqlite"))
        self.locDB = sqlite3.connect(CIVVI6DB_DIR.joinpath("DebugLocalization.sqlite"))
        self.simplizedDB = sqlite3.connect(CIVVI6DB_DIR.joinpath("SimplizedData.sqlite"))

        #  设定为以字典形式输出
        def dict_row_factory(cursor, row):
            fields = tuple(i[0] for i in cursor.description)
            return CivDataDict(fields, row)

        self.confDB.row_factory = dict_row_factory
        self.GamePlayDB.row_factory = dict_row_factory
        self.locDB.row_factory = dict_row_factory
        self.simplizedDB.row_factory = dict_row_factory

        #  把输出调回默认值
        #  self.confDB.row_factory = None
        #      ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.confDB.close()
        self.GamePlayDB.close()
        self.locDB.close()
        self.simplizedDB.close()

    @staticmethod
    def doSelectAndGetResult(db: sqlite3.Connection, sql: str, params=()) -> list[dict]:
        new_cursor = db.cursor()
        try:
            new_cursor.execute(sql, params)
            return new_cursor.fetchall()
        finally:
            new_cursor.close()

    def findName(self, keyword, command_target_types: list or tuple):
        use_db = self.simplizedDB
        # 先检查是不是真实存在的名字
        sql = "select Truename from BotData_Alias where Truename = ? and type in ("
        for i, _ in enumerate(command_target_types):
            if i == 0:
                sql += "?"
            else:
                sql += ",?"
        sql += ") limit 1;"
        params = (keyword,) + tuple(command_target_types)
        query_result = self.doSelectAndGetResult(use_db, sql, params)
        if query_result:
            return True, keyword
        else:
            # 不存在则查别名
            sql = "select Truename from BotData_Alias where Alia = ? and type in ("
            for i, _ in enumerate(command_target_types):
                if i == 0:
                    sql += "?"
                else:
                    sql += ",?"
            sql += ");"
            params = (keyword,) + tuple(command_target_types)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                return False, None
            elif len(query_result) == 1:
                return True, query_result[0]["Truename"]
            else:
                return True, [i["Truename"] for i in query_result]

    def selectUU(self, keyword, command_index=None):
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leader =?"
        r2 = self.doSelectAndGetResult(use_db, sql2, params)
        if not (r1 or r2):
            kw_tp = None
        elif not r1 and r2:
            kw_tp = "Leader"
        else:
            kw_tp = "Civilization"

        if kw_tp == "Civilization":
            sql = "select * from {} where Civilization = ? and Civilization=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_unit_data = "文明{}没有UU。\n".format(keyword)
                have_ui = False
            else:
                unique_unit_data = "{}有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += self.formatUnitData(i)
                    unique_unit_data += "=" * 20 + "\n"
                have_ui = True
            sql = "select * from {} where Civilization = ? and Civilization!=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_unit_data
                else:
                    return unique_unit_data + "其所有领袖也都没有UU。"
            else:
                if have_ui:
                    unique_unit_data += "而且{}的领袖有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_unit_data += "但是{}的领袖有{}个UU。以下是它{}}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += "领袖：{}\n".format(i["Owner"])
                    unique_unit_data += self.formatUnitData(i)
                    unique_unit_data += "=" * 20 + "\n"
                return unique_unit_data
        elif kw_tp == "Leader":
            sql = "select * from {} where Owner = ?".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_unit_data = "领袖{}没有UU。\n".format(keyword)
                have_ui = False
            else:
                unique_unit_data = "{}有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += self.formatUnitData(i)
                    unique_unit_data += "=" * 20 + "\n"
                have_ui = 1
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leader = ?) and Owner = Civilization".format(
                table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_unit_data
                else:
                    return unique_unit_data + "其所属国家也没有UU。"
            else:
                if have_ui:
                    unique_unit_data += "同时{}的所属国家有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_unit_data += "但是{}的所属国家有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += "国家：{}\n".format(i["Civilization"])
                    unique_unit_data += self.formatUnitData(i)
                    unique_unit_data += "=" * 20 + "\n"
                return unique_unit_data
        else:
            return "没能找到该领袖或文明。"

    def formatUnitData(self, unit_data: dict):
        unit_name = unit_data["Unitname"]+"\n\n"
        description = re.sub("\s[[]ICON_.*[]]\s","",unit_data["Description"])
        basic_info = "\n" + "=" * 6+"\n"
        for i in unit_info_dict["basic_info"]:
            if unit_data[i]:
                if "{}" in unit_info_dict["basic_info"][i]:
                    basic_info += "{}\n".format(unit_info_dict["basic_info"][i].format(unit_data[i]))
                else:
                    basic_info += "{}\n".format(unit_info_dict["basic_info"][i])
        special_info = "=" * 6+"\n特殊能力\n"
        for i in unit_info_dict["special_info"]:
            if unit_data[i]:
                if "{}" in unit_info_dict["special_info"][i]:
                    special_info += "{}\n".format(unit_info_dict["special_info"][i].format(unit_data[i]))
                else:
                    special_info += "{}\n".format(unit_info_dict["special_info"][i])
        return unit_name + description + basic_info + special_info

    def selectUI(self, keyword, command_index=None):
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leader =?"
        r2 = self.doSelectAndGetResult(use_db, sql2, params)
        if not (r1 or r2):
            kw_tp = None
        elif not r1 and r2:
            kw_tp = "Leader"
        else:
            kw_tp = "Civilization"

        if kw_tp == "Civilization":
            sql = "select * from {} where Civilization = ? and Civilization=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_unit_data = "文明{}没有UI。\n".format(keyword)
                have_ui = False
            else:
                unique_unit_data = "{}有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += self.formatImprovementData(i)
                    unique_unit_data += "=" * 20 + "\n"
                have_ui = True
            sql = "select * from {} where Civilization = ? and Civilization!=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_unit_data
                else:
                    return unique_unit_data + "其所有领袖也都没有UI。"
            else:
                if have_ui:
                    unique_unit_data += "而且{}的领袖有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_unit_data += "但是{}的领袖有{}个UI。以下是它{}}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += "领袖：{}\n".format(i["Owner"])
                    unique_unit_data += self.formatImprovementData(i)
                    unique_unit_data += "=" * 20 + "\n"
                return unique_unit_data
        elif kw_tp == "Leader":
            sql = "select * from {} where Owner = ?".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_unit_data = "领袖{}没有UI。\n".format(keyword)
                have_ui = False
            else:
                unique_unit_data = "{}有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += self.formatImprovementData(i)
                    unique_unit_data += "=" * 20 + "\n"
                have_ui = 1
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leader = ?) and Owner = Civilization".format(
                table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_unit_data
                else:
                    return unique_unit_data + "其所属国家也没有UI。"
            else:
                if have_ui:
                    unique_unit_data += "同时{}的所属国家有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_unit_data += "但是{}的所属国家有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_unit_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_unit_data += "国家：{}\n".format(i["Civilization"])
                    unique_unit_data += self.formatImprovementData(i)
                    unique_unit_data += "=" * 20 + "\n"
                return unique_unit_data
        else:
            return "没能找到该领袖或文明。"

    def formatImprovementData(self, unit_data: dict):
        improvement_name = unit_data["Improvementname"]+"\n\n"
        description = re.sub("\s*\[ICON_.+?]\s*","",unit_data["Description"])
        description = re.sub("\s*\[NEWLINE]\s*(\[NEWLINE])*\s*","\n",description)
        basic_info = "\n" + "=" * 6+"\n"
        for i in improvement_info_dict["basic_info"]:
            if unit_data[i]:
                if "{}" in improvement_info_dict["basic_info"][i]:
                    basic_info += "{}\n".format(improvement_info_dict["basic_info"][i].format(unit_data[i]))
                else:
                    basic_info += "{}\n".format(improvement_info_dict["basic_info"][i])
        special_info = "=" * 6+"\n特殊能力\n"
        for i in improvement_info_dict["special_info"]:
            if unit_data[i]:
                if "{}" in improvement_info_dict["special_info"][i]:
                    special_info += "{}\n".format(improvement_info_dict["special_info"][i].format(unit_data[i]))
                else:
                    special_info += "{}\n".format(improvement_info_dict["special_info"][i])
        return improvement_name + description + basic_info + special_info


#  todo 以下代码仅限调试时用，正式上线时删除
if __name__ == "__main__":
    new_accesser = DataAccesser()
    test_sql = "select * from zh_Hans_Text limit 10"
    r = new_accesser.doSelectAndGetResult(new_accesser.locDB, test_sql)
    print("=" * 35)
    for i in r:
        print(i)
