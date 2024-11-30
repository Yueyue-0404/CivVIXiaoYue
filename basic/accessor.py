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
    with open(CONFIG_DIR.joinpath("districtdata.json"), mode="r") as file:
        district_info_dict = json.load(file)
    with open(CONFIG_DIR.joinpath("buildingdata.json"), mode="r") as file:
        building_info_dict = json.load(file)
else:
    from settings import *
    from model import CivDataDict

    CIVVI6DB_DIR = Path("/home/tarena/Yueyue/PyCharmProject/Own/qqbot/CivVIXiaoYue/data/civ6db")
    CONFIG_DIR = Path("/home/tarena/Yueyue/PyCharmProject/Own/qqbot/CivVIXiaoYue/config")
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
        params = (keyword,) + (tuple(command_target_types) if command_target_types else tuple())
        if command_target_types:
            sql = "select Truename from BotData_Alias where Truename = ? and type in ("
            for i, _ in enumerate(command_target_types):
                if i == 0:
                    sql += "?"
                else:
                    sql += ",?"
            sql += ") limit 1;"
        else:
            sql = "select Truename from BotData_Alias where Truename = ? limit 1;"
        query_result = self.doSelectAndGetResult(use_db, sql, params)
        if query_result:
            return True, keyword
        else:
            # 不存在则查别名
            if command_target_types:
                sql = "select Truename from BotData_Alias where Alia = ? and type in ("
                for i, _ in enumerate(command_target_types):
                    if i == 0:
                        sql += "?"
                    else:
                        sql += ",?"
                sql += ");"
            else:
                sql = "select Truename from BotData_Alias where Alia = ?;"
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
        sql2 = "select 1 from BotData_CivilizationLeaders where Leaders =?"
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
                    unique_unit_data += "但是{}的领袖有{}个UU。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
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
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leaders = ?) and Owner = Civilization".format(
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
        description = re.sub("\s*\[ICON_.+?]\s*","",unit_data["Description"])
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
        """
            因为improvements的信息比较分散，所以还要额外进行查询之后再进行格式化
        """
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leaders =?"
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
                unique_improvement_data = "文明{}没有UI。\n".format(keyword)
                have_ui = False
            else:
                unique_improvement_data = "{}有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_improvement_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_improvement_data += self.formatImprovementData(i)
                    unique_improvement_data += "=" * 20 + "\n"
                have_ui = True
            sql = "select * from {} where Civilization = ? and Civilization!=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_improvement_data
                else:
                    return unique_improvement_data + "其所有领袖也都没有UI。"
            else:
                if have_ui:
                    unique_improvement_data += "而且{}的领袖有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                else:
                    unique_improvement_data += "但是{}的领袖有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_improvement_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_improvement_data += "领袖：{}\n".format(i["Owner"])
                    unique_improvement_data += self.formatImprovementData(i)
                    unique_improvement_data += "=" * 20 + "\n"
                return unique_improvement_data
        elif kw_tp == "Leader":
            sql = "select * from {} where Owner = ?".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_improvement_data = "领袖{}没有UI。\n".format(keyword)
                have_ui = False
            else:
                unique_improvement_data = "{}有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_improvement_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_improvement_data += self.formatImprovementData(i)
                    unique_improvement_data += "=" * 20 + "\n"
                have_ui = 1
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leaders = ?) and Owner = Civilization".format(
                table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_improvement_data
                else:
                    return unique_improvement_data + "其所属国家也没有UI。"
            else:
                if have_ui:
                    unique_improvement_data += "同时{}的所属国家有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                else:
                    unique_improvement_data += "但是{}的所属国家有{}个UI。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_improvement_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_improvement_data += "国家：{}\n".format(i["Civilization"])
                    unique_improvement_data += self.formatImprovementData(i)
                    unique_improvement_data += "=" * 20 + "\n"
                return unique_improvement_data
        else:
            return "没能找到该领袖或文明。"

    def formatImprovementData(self, improvement_data: dict):
        medium_split_line = "=" * 12 + "\n"
        short_split_line = "=" * 6 + "\n"

        improvement_name = "名称：" + improvement_data["Improvementname"] + "\n"
        description = re.sub("\s*\[ICON_.+?]\s*","", improvement_data["Description"])
        description = medium_split_line + "官方介绍：\n" + re.sub("\s*\[NEWLINE]\s*(\[NEWLINE])*\s*", "\n", description) + "\n"+medium_split_line
        extra_info = self.doExtraImprovementQuery(improvement_data["ImprovementType"])
        basic_info = "\n" + short_split_line
        for i in improvement_info_dict["basic_info"]:
            if improvement_data[i]:
                if "{}" in improvement_info_dict["basic_info"][i]:
                    basic_info += "{}\n".format(improvement_info_dict["basic_info"][i].format(improvement_data[i]))
                else:
                    basic_info += "{}\n".format(improvement_info_dict["basic_info"][i])
        special_info = short_split_line+"特殊能力\n"
        for i in improvement_info_dict["special_info"]:
            if improvement_data[i]:
                if "{}" in improvement_info_dict["special_info"][i]:
                    special_info += "{}\n".format(improvement_info_dict["special_info"][i].format(improvement_data[i]))
                else:
                    special_info += "{}\n".format(improvement_info_dict["special_info"][i])
        return improvement_name + description + extra_info + basic_info + special_info

    def doExtraImprovementQuery(self, improvement_key):
        """
            improvement_key就是ImprovementType字段
        """
        new_cursor = self.simplizedDB.cursor()
        extra_content_list = []
        try:
            # 1. 在Improvement_YieldChanges查询产出
            new_cursor.execute("select YieldType,YieldChange from BotData_Improvement_YieldChanges where ImprovementType = ? and YieldChange != 0", (improvement_key,))
            res = new_cursor.fetchall()
            # todo 这里应该把execute重写成自己之前封装的方法
            if res:
                extra_content = "基础产出："+"，".join(["+{}{}".format(i["YieldChange"],i["YieldType"],) for i in res])
                extra_content_list.append(extra_content)

            # 2. 在BotData_Improvement_BonusYieldChanges查询随着文明进步带来的额外产出
            new_cursor.execute("select YieldType,BonusYieldChange,Prereq from BotData_Improvement_BonusYieldChanges where ImprovementType = ?", (improvement_key,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "时代进步产出："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {} +{}{}".format(i+1, row["Prereq"], row["BonusYieldChange"], row["YieldType"])
                extra_content_list.append(extra_content)

            # 3. 在BotData_Improvement_AdjacencyYieldChanges查询相邻加成
            new_cursor.execute("select ImprovementType,YieldChange,Prereq,Obsolete from BotData_Improvement_AdjacencyYieldChanges where ImprovementType = ?",(improvement_key,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "相邻加成："
                for i, row in enumerate(res):
                    if not row["Prereq"] and not row["Obsolete"]:
                        extra_content += "\n" + " "*4 + "{}. {}".format(i+1, row["YieldChange"])
                    elif row["Prereq"] and not row["Obsolete"]:
                        extra_content += "\n" + " "*4 + "{}. {}解锁，{}".format(i+1,row["Prereq"], row["YieldChange"])
                    elif not row["Prereq"] and row["Obsolete"]:
                        extra_content += "\n" + " "*4 + "{}. {}，于{}淘汰".format(i+1,row["YieldChange"], row["Obsolete"])
                    else:  #  elif row["Prereq"] and row["Obsolete"]:
                        extra_content += "\n" + " " * 4 + "{}. {}解锁，{}，于{}淘汰".format(i + 1,row["Prereq"], row["YieldChange"],row["Obsolete"])
                extra_content_list.append(extra_content)
        finally:
            new_cursor.close()
            return "\n===\n".join(extra_content_list)

    def selectUD(self, keyword, command_index=None):
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leaders =?"
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
                unique_district_data = "文明{}没有UD。\n".format(keyword)
                have_ui = False
            else:
                unique_district_data = "{}有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_district_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_district_data += self.formatDistrictData(i)
                    unique_district_data += "=" * 20 + "\n"
                have_ui = True
            sql = "select * from {} where Civilization = ? and Civilization!=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_district_data
                else:
                    return unique_district_data + "其所有领袖也都没有UD。"
            else:
                if have_ui:
                    unique_district_data += "而且{}的领袖有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_district_data += "但是{}的领袖有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_district_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_district_data += "领袖：{}\n".format(i["Owner"])
                    unique_district_data += self.formatDistrictData(i)
                    unique_district_data += "=" * 20 + "\n"
                return unique_district_data
        elif kw_tp == "Leader":
            sql = "select * from {} where Owner = ?".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_district_data = "领袖{}没有UD。\n".format(keyword)
                have_ui = False
            else:
                unique_district_data = "{}有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_district_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_district_data += self.formatDistrictData(i)
                    unique_district_data += "=" * 20 + "\n"
                have_ui = 1
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leaders = ?) and Owner = Civilization".format(
                table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_district_data
                else:
                    return unique_district_data + "其所属国家也没有UD。"
            else:
                if have_ui:
                    unique_district_data += "同时{}的所属国家有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                else:
                    unique_district_data += "但是{}的所属国家有{}个UD。以下是它{}的信息：\n".format(keyword, len(query_result),"们" if len(query_result)>1 else "")
                unique_district_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_district_data += "国家：{}\n".format(i["Civilization"])
                    unique_district_data += self.formatDistrictData(i)
                    unique_district_data += "=" * 20 + "\n"
                return unique_district_data
        else:
            return "没能找到该领袖或文明。"

    def formatDistrictData(self, district_data: dict):
        medium_split_line = "=" * 12 + "\n"
        short_split_line = "=" * 6 + "\n"

        district_name = "名称：" + district_data["DistrictName"] + "\n"
        description = re.sub("\s*\[ICON_.+?]\s*","", district_data["Description"])
        description = medium_split_line + "官方介绍：\n" + re.sub("\s*\[NEWLINE]\s*(\[NEWLINE])*\s*", "\n", description) + "\n"+medium_split_line
        extra_info = self.doExtraDistrictQuery(district_data["DistrictName"])
        basic_info = "\n" + short_split_line
        for i in district_info_dict["basic_info"]:
            if district_data[i]:
                if "{}" in district_info_dict["basic_info"][i]:
                    basic_info += "{}\n".format(district_info_dict["basic_info"][i].format(district_data[i]))
                else:
                    basic_info += "{}\n".format(district_info_dict["basic_info"][i])
        special_info = short_split_line+"特殊能力\n"
        for i in district_info_dict["special_info"]:
            if district_data[i]:
                if "{}" in district_info_dict["special_info"][i]:
                    special_info += "{}\n".format(district_info_dict["special_info"][i].format(district_data[i]))
                else:
                    special_info += "{}\n".format(district_info_dict["special_info"][i])
        return district_name + description + extra_info + basic_info + special_info

    def doExtraDistrictQuery(self, district_name):
        """
            district_name已经在ETL的过程中转化为中文字段
        """
        new_cursor = self.simplizedDB.cursor()
        extra_content_list = []
        try:
            # 1. 在BotData_District_GreatPersonPoints查询伟人点产出
            new_cursor.execute("select GreatPersonClassName,PointsPerTurn from BotData_District_GreatPersonPoints where DistrictName = ?", (district_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "伟人点产出："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {}点数+{}".format(i+1,  row["GreatPersonClassName"], row["PointsPerTurn"])
                extra_content_list.append(extra_content)

            # 2. 在BotData_District_CitizenYieldChanges查询专家产出
            new_cursor.execute("select YieldName,YieldChange from BotData_District_CitizenYieldChanges where DistrictName = ?", (district_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "专家产出："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {}+{}".format(i+1, row["YieldName"], row["YieldChange"])
                extra_content_list.append(extra_content)

            # 3. 在BotData_District_AdjacencyYieldChanges查询相邻加成
            new_cursor.execute("select YieldChange from BotData_District_AdjacencyYieldChanges where DistrictName = ?", (district_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "相邻加成："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {}".format(i+1, row["YieldChange"])
                extra_content_list.append(extra_content)
            # 4. 在BotData_District_TradeRouteYields查询商路加成
            new_cursor.execute("select Yield,YieldChangeAsOrigin from BotData_District_TradeRouteYields where DistrictName = ? and YieldChangeAsOrigin != 0", (district_name,))
            YieldChangeAsOrigin = new_cursor.fetchall()
            new_cursor.execute("select Yield,YieldChangeAsDomesticDestination from BotData_District_TradeRouteYields where DistrictName = ? and YieldChangeAsOrigin != 0", (district_name,))
            YieldChangeAsDomesticDestination = new_cursor.fetchall()
            new_cursor.execute("select Yield,YieldChangeAsInternationalDestination from BotData_District_TradeRouteYields where DistrictName = ? and YieldChangeAsOrigin != 0", (district_name,))
            YieldChangeAsInternationalDestination = new_cursor.fetchall()
            if YieldChangeAsOrigin or YieldChangeAsDomesticDestination or YieldChangeAsInternationalDestination:
                extra_content = "商路收益：\n"
                if YieldChangeAsOrigin:
                    extra_content += "        ".join(["   当商路出发地有该区域时："]+["+{}{}".format(i["YieldChangeAsInternationalDestination"],i["Yield"]) for i in YieldChangeAsOrigin])
                if YieldChangeAsDomesticDestination:
                    extra_content += "        ".join(["   当内贸目的地有该区域时："]+["+{}{}".format(i["YieldChangeAsInternationalDestination"],i["Yield"]) for i in YieldChangeAsOrigin])
                if YieldChangeAsInternationalDestination:
                    extra_content += "        ".join(["   当外贸目的地有该区域时："]+["+{}{}".format(i["YieldChangeAsInternationalDestination"],i["Yield"]) for i in YieldChangeAsOrigin])
        finally:
            new_cursor.close()
            return "\n===\n".join(extra_content_list)

    def selectUB(self, keyword, command_index=None):
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leaders =?"
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
                unique_building_data = "文明{}没有UB。\n".format(keyword)
                have_ui = False
            else:
                unique_building_data = "{}有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_building_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_building_data += self.formatBuildingData(i)
                    unique_building_data += "=" * 20 + "\n"
                have_ui = True
            sql = "select * from {} where Civilization = ? and Civilization!=Owner".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_building_data
                else:
                    return unique_building_data + "其所有领袖也都没有UB。"
            else:
                if have_ui:
                    unique_building_data += "而且{}的领袖有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                else:
                    unique_building_data += "但是{}的领袖有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_building_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_building_data += "领袖：{}\n".format(i["Owner"])
                    unique_building_data += self.formatBuildingData(i)
                    unique_building_data += "=" * 20 + "\n"
                return unique_building_data
        elif kw_tp == "Leader":
            sql = "select * from {} where Owner = ?".format(table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                unique_building_data = "领袖{}没有UB。\n".format(keyword)
                have_ui = False
            else:
                unique_building_data = "{}有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_building_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_building_data += self.formatBuildingData(i)
                    unique_building_data += "=" * 20 + "\n"
                have_ui = 1
            sql = "select * from {} where Civilization in (select Civilization from BotData_CivilizationLeaders where Leaders = ?) and Owner = Civilization".format(
                table)
            query_result = self.doSelectAndGetResult(use_db, sql, params)
            if not query_result:
                if have_ui:
                    return unique_building_data
                else:
                    return unique_building_data + "其所属国家也没有UB。"
            else:
                if have_ui:
                    unique_building_data += "同时{}的所属国家有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                else:
                    unique_building_data += "但是{}的所属国家有{}个UB。以下是它{}的信息：\n".format(keyword, len(query_result), "们" if len(query_result) > 1 else "")
                unique_building_data += "=" * 20 + "\n"
                for i in query_result:
                    unique_building_data += "国家：{}\n".format(i["Civilization"])
                    unique_building_data += self.formatBuildingData(i)
                    unique_building_data += "=" * 20 + "\n"
                return unique_building_data
        else:
            return "没能找到该领袖或文明。"

    def formatBuildingData(self, building_data: dict):
        medium_split_line = "=" * 12 + "\n"
        short_split_line = "=" * 6 + "\n"

        building_name = "名称：" + building_data["Name"] + "\n"
        description = re.sub("\s*\[ICON_.+?]\s*","", building_data["Description"])
        description = medium_split_line + "官方介绍：\n" + re.sub("\s*\[NEWLINE]\s*(\[NEWLINE])*\s*", "\n", description) + "\n"+medium_split_line
        extra_info = self.doExtraBuildingQuery(building_data["Name"])
        basic_info = "\n" + short_split_line
        for i in building_info_dict["basic_info"]:
            if building_data[i]:
                if "{}" in building_info_dict["basic_info"][i]:
                    basic_info += "{}\n".format(building_info_dict["basic_info"][i].format(building_data[i]))
                    # if i == "CitizenSlots":
                    #     basic_info += self.doBuildingCitizenYieldChangesQuery(building_data["Name"]) + "\n"
                else:
                    basic_info += "{}\n".format(building_info_dict["basic_info"][i])
        special_info = short_split_line+"特殊能力\n"
        for i in building_info_dict["special_info"]:
            if building_data[i]:
                if "{}" in building_info_dict["special_info"][i]:
                    special_info += "{}\n".format(building_info_dict["special_info"][i].format(building_data[i]))
                else:
                    special_info += "{}\n".format(building_info_dict["special_info"][i])
        return building_name + description + extra_info + basic_info + special_info

    def doExtraBuildingQuery(self, building_name):
        """
            building_name已经在ETL的过程中转化为中文字段
        """
        new_cursor = self.simplizedDB.cursor()
        extra_content_list = []
        try:
            # 1. 在BotData_Building_YieldChanges查询基础产出
            new_cursor.execute("select BuildingName,Yield,YieldChange from BotData_Building_YieldChanges where BuildingName = ?", (building_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "基础产出："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {}+{}".format(i+1,  row["Yield"], row["YieldChange"])
                extra_content_list.append(extra_content)

            # 2. 在BotData_Building_YieldChangesBonusWithPower查询通电产出
            # 在BotData_Buildings_XP2中查询通电宜居
            # 如果有，在BotData_Buildings_XP2中查询通电消耗
            new_cursor.execute("select BuildingName,Yield,YieldChange from BotData_Building_YieldChangesBonusWithPower where BuildingName = ? union all select BuildingName,'宜居度',EntertainmentBonusWithPower from BotData_Buildings_XP2 where BuildingName = ?", (building_name,building_name))
            res1 = new_cursor.fetchall()
            if sum([i["YieldChange"] for i in res1]) != 0:
                new_cursor.execute("select RequiredPower from BotData_Buildings_XP2 where BuildingName = ?",
                (building_name,))
                res2 = new_cursor.fetchall()
                if res2[0]["RequiredPower"]:
                    extra_content = "该建筑会消耗{}点电力来提供电力额外产出：".format(res2[0]["RequiredPower"])
                    for i, row in enumerate([i for i in res1 if i["YieldChange"]]):
                        extra_content += "\n"+" "*4 + "{}. {}+{}".format(i+1, row["Yield"], row["YieldChange"])
                    extra_content_list.append(extra_content)
                else:
                    # 这段代码应该是不可能发生的，只是为了逻辑完整才写
                    extra_content = "该建筑不消耗电力就能提供电力产出".format(res2[0]["RequiredPower"])
                    for i, row in enumerate([i for i in res1 if i["YieldChange"]]):
                        extra_content += "\n" + " " * 4 + "{}. {}+{}".format(i + 1, row["Yield"], row["YieldChange"])
                    extra_content_list.append(extra_content)

            # 3. 在BotData_Building_YieldDistrictCopies查询相邻产出
            new_cursor.execute("select BuildingName,OldYieldType,NewYieldType from BotData_Building_YieldDistrictCopies where BuildingName = ?", (building_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "相邻产出："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. 所在区域每有多少点{}相邻加成，该建筑就提供多少{}产出".format(i+1, row["OldYieldType"], row["NewYieldType"])
                extra_content_list.append(extra_content)

            # 4. 在BotData_Building_CitizenYieldChanges中查询专家增强效果
            new_cursor.execute("select YieldType,YieldChange from BotData_Building_CitizenYieldChanges where BuildingType = ?",(building_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "该建筑能使基底区域的专家产出获得以下额外提升："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4+"{}. {}+{}".format(i+1,row["YieldType"], row["YieldChange"])
                extra_content_list.append(extra_content)

            # 5. 在BotData_Building_GreatWorkSlot中查询巨作的槽位
            new_cursor.execute("select GreatWorkSlotType,NumSlots from BotData_Building_GreatWorkSlot where BuildingName = ?",(building_name,))
            res = new_cursor.fetchall()
            if res:
                if len(res) == 1:
                    extra_content = "该建筑能提供巨作槽位："
                else:
                    extra_content = "该建筑提供多种巨作槽位，玩家可以自选填充："
                for i, row in enumerate(res):
                    extra_content += "\n"+" "*4+"{}. {} {}槽位".format(i+1,row["NumSlots"], row["GreatWorkSlotType"])
                extra_content_list.append(extra_content)
            # 6. 在BotData_BuildingPrereqs中查询前置建筑
            new_cursor.execute("select PrereqBuilding from BotData_BuildingPrereqs where Building = ?",(building_name,))
            res = new_cursor.fetchall()
            if res:
                extra_content = "所在的基底区域里，以下建筑必须竣工至少一个才能建造该建筑："
                for i,row in enumerate(res):
                    extra_content += "\n"+" "*4 + "{}. {}".format(i+1,row["PrereqBuilding"])
            else:
                extra_content = "这个建筑不需要任何前置建筑。"
            extra_content_list.append(extra_content)

        finally:
            new_cursor.close()
            return "\n===\n".join(extra_content_list)


    def selectAB(self, keyword, command_index=None):
        use_db = self.simplizedDB if command_index else self.GamePlayDB
        table = table_dict[command_index]
        params = (keyword,)

        #  先查询是国家还是领袖
        sql1 = "select 1 from BotData_CivilizationLeaders where Civilization =?"
        r1 = self.doSelectAndGetResult(use_db, sql1, params)
        sql2 = "select 1 from BotData_CivilizationLeaders where Leaders =?"
        r2 = self.doSelectAndGetResult(use_db, sql2, params)
        if not (r1 or r2):
            return "没能找到该领袖或文明。"
        else:
            sql = "select Owner,TraitName,TraitDescription from BotData_CivilizationsAndLeaders_Traits where Owner = ?"
            res = self.doSelectAndGetResult(use_db, sql, params)
            if res:
                ability_content = "{}拥有能力如下：".format(keyword)
                for i,row in enumerate(res):
                    ability_content += "\n"+" "*4+"{}. {}".format(i+1,row["TraitName"])
                    description = re.sub("\s*\[ICON_.+?]\s*", "", row["TraitDescription"])
                    description = re.sub("\s*\[NEWLINE]\s*(\[NEWLINE])*\s*", "\n", description)
                    ability_content += "\n" + " " * 4 + "{}".format(description)
                return ability_content
            else:
                return "{}没有特殊能力".format(keyword)

    def findCategory(self,keyword):
        result = self.doSelectAndGetResult(
            self.simplizedDB,
            "select Type from BotData_Alias where Truename = ?;",
            (keyword,)
        )
        category = result[0].get("Type")
        return category



#  todo 以下代码仅限调试时用，正式上线时删除
if __name__ == "__main__":
    new_accesser = DataAccesser()
    test_sql = "select * from zh_Hans_Text limit 10"
    r = new_accesser.doSelectAndGetResult(new_accesser.locDB, test_sql)
    print("=" * 35)
    for i in r:
        print(i)
