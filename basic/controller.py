import json
import re

import pypinyin
import yaml
from fuzzywuzzy import process

from .accessor import DataAccesser
from .settings import *

with open(CONFIG_DIR.joinpath("commands.yaml"), mode="r", encoding="utf8") as file:
    command_dict = yaml.safe_load(file)

with open(CONFIG_DIR.joinpath("command_target_types.yaml"), mode="r", encoding="utf8") as file:
    command_target_types = yaml.safe_load(file)

with open(DATA_DIR.joinpath("alias_dict.json"), mode="r", encoding="utf8") as file:
    alias_dict = json.load(file)

with open(DATA_DIR.joinpath("alias_pinyin_dict.json"), mode="r", encoding="utf8") as file:
    alias_pinyin_dict = json.load(file)


class Controller:
    def __init__(self):
        self.accesser = DataAccesser()

    def parseMSG(self, content: str):
        """
        这里应当是bot_process收到消息后进行消息处理的唯一入口
        """
        content_split_with_space = self.splitMessage(content)
        command_index, keyword = self.checkCommandAndContent(content_split_with_space)
        return command_index, keyword

    def splitMessage(self, content: str):
        content = content.strip()
        content = content.replace("\r\n", " ").replace("\t", " ").replace("\n", " ")
        content_split_with_space = content.split(" ")
        for i in content_split_with_space[:]:
            if not i:
                content_split_with_space.remove(i)
        return content_split_with_space

    def checkCommandAndContent(self, content_split_with_space: list):
        if not content_split_with_space:
            # 如果是空消息，视为全局帮助指令
            return command_dict["/help"], ""

        command = content_split_with_space[0]
        # 如果是普通消息，返回一个100和全部消息内容
        if command[0] != "/":
            return 100, " ".join(content_split_with_space)

        # 如果是指令消息，根据文件内容返回指令编号和消息内容
        if command in command_dict:
            if len(content_split_with_space) > 1:
                return command_dict[command], " ".join(content_split_with_space[1:])
            else:
                return command_dict["/help"], ""
        else:
            # 如果没有这个指令
            return 0, ""

    # 该函数已弃用
    # def deleteLettersAndNumbersFromKeyword(self, keyword: str):
    #     """
    #         该函数应该在无法搜索到真名或别名时才被调用，并在之后继续调用getPinyin
    #         该函数只负责剔除字符串中的英文字符
    #         因为后续要在getPinyin中处理，它会自动将汉字和其他字符分组出去，
    #         而只要先剔除英文字符，就可以在后续轻松通过for循环来找出哪个元素是拼音，哪个元素是杂鱼
    #     """
    #     re_res = re.search("[A-Za-z]", keyword)
    #     if re_res:
    #         keyword = re.sub("[A-Za-z]", "", keyword)
    #     return keyword

    def getPinyin(self, keyword):
        """
            该函数负责将字符串转化为拼音串
        """
        pinyin_of_keyword_list = pypinyin.lazy_pinyin(keyword)
        keyword_pinyin = "".join([i for i in pinyin_of_keyword_list if re.search("[A-Za-z]", i)])
        return keyword_pinyin

    def checkWrong(self, keyword_pinyin):
        """
        函数输入拼音，返回匹配目标及其相似度
        由于有一些真名不一样的关键词有一样的别名，所以返回的结果要去重
        """
        keyword_length = len(keyword_pinyin)
        candidate_alias_list, candidate_alias_pinyin_list = [], []
        for i in (-1, 0, 1):
            candidate_alias_list += alias_dict.get(str(keyword_length + i), [])
            candidate_alias_pinyin_list += alias_pinyin_dict.get(str(keyword_length + i), [])
        parsedkeyword_pinyin, similarity = process.extractOne(keyword_pinyin, candidate_alias_pinyin_list)
        print("比较完成，", keyword_pinyin, parsedkeyword_pinyin, similarity)
        if similarity < KEYWORD_SIMILARITY:  # 这里是在setting.py里改的
            return None, similarity
        else:
            possible_keywords = [candidate_alias_list[i] for i, v in enumerate(candidate_alias_pinyin_list) if v == parsedkeyword_pinyin]
            return list(set(possible_keywords)), similarity
        # 这是纠正错别字的函数

    def assignQueryMission(self, command_index, keyword) -> str:
        """
            这个函数应当是bot_process获取查询结果的唯一入口，且应该传入parseMSG返回的结果
            然后根据指令和关键字分配查询任务
        """
        content = ""
        if command_index == command_dict["/help"]:
            content += "这是帮助"
        else:
            keywords_selected = self.checkInNameTable(keyword, command_index)
            res,keyword,content_plus = self.ifIsAlia(keyword,keywords_selected)
            if res == 2:
                content += content_plus
                return content
            elif res == 1:
                content += content_plus
            else:  # elif res == 0
                content += content_plus
                possible_keywords = self.checkWrong(self.getPinyin(keyword))[0]
                res, keyword, content_plus = self.ifIsWrongTyped(keyword,possible_keywords)
                if res == 2:
                    content += content_plus
                    return content
                elif res == 1:
                    content += content_plus
                    keywords_selected = self.checkInNameTable(keyword, command_index)
                    res, keyword, content_plus = self.ifIsAlia(keyword, keywords_selected)
                    if res == 2:
                        content += content_plus
                        return content
                    elif res == 1:
                        content += content_plus
                    else:  # res不可能是0，因为元数据都是存在的
                        content = "错误，错别字候选词中存在该候选词，但别名表中不存在此关键词，发生该错误请联系开发者。"
                        return content
                else:
                    return content

            if command_index == 100:
                content += "这是个普通指令，直接查询关键字{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword, command_index))
            elif command_index == command_dict["/uu"]:
                content += "这是uu指令，应该查询国家或领袖{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword, command_index))
                # 这是uu指令
            elif command_index == command_dict["/ud"]:
                content += "这是ud指令，应该查询国家或领袖{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword))
                # 这是ud指令
            elif command_index == command_dict["/ub"]:
                content += "这是ub指令，应该查询国家或领袖{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword))
                # 这是ub指令
            elif command_index == command_dict["/ui"]:
                content += "这是ui指令，应该查询国家或领袖{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword))
                # 这是ui指令
            elif command_index == command_dict["/ability"]:
                content += "这是ability指令，应该查询国家或领袖{}\n".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword))
                # 这是ab指令
            elif command_index == command_dict["/bug"]:
                content += "这是bug指令{}".format(keyword)
                content += "结果为：{}".format(self.accesser.selectUU(keyword))
                # 这是bug指令
            elif command_index == 0:
                content += "不存在这个指令"
                # 这是错误指令，这个指令并不存在，这个指令会返回一个帮助图片
            else:
                content += "未知错误，多次出现请联系作者。"
            return content

    def checkInNameTable(self, keyword, command_index):
        exists, keyword_selected = self.accesser.findName(keyword, command_target_types[command_index])
        if not exists:
            return False
        else:
            return keyword_selected

    def ifIsAlia(self,keyword,keywords_selected):
        """
            断言它是别名，进行流程控制
            返回：
                2代表多个，1代表唯一，0代表无结果
                keyword只有唯一时发生了改变返回，其他时候都是原样返回，效果是把用户输入的别名换成真名
                content就是文本
        """
        content = ""
        if type(keywords_selected) == list:
            content += "您要查询的关键词应该是个别称，下面是几种可能性：\n"
            for i, v in enumerate(keywords_selected):
                content += "{}. {}\n".format(i + 1, v)
            content += "请点击您要查询的关键词。"
            return 2, keyword, content
        elif type(keywords_selected) == str:
            content += "您要查询的关键词{0}是{1}的别称，因此为您查询{1}。\n".format(keyword, keywords_selected)
            keyword = keywords_selected
            return 1,keyword,content
        elif not keywords_selected:
            content += "找不到您要查询的关键词。\n"
            return 0,keyword,content

    def ifIsWrongTyped(self,keyword,possible_keywords):
        """
           断言它是错别字，进行流程控制
           返回：
               2代表多个，1代表唯一，0代表无结果
               keyword只有唯一时发生了改变返回，其他时候都是原样返回，效果是把用户输入的错名换成别名
               content就是文本
       """
        content = "尝试对“{0}”进行错别字纠正……".format(keyword)
        if possible_keywords is None:
            return 0,keyword,content
        elif len(possible_keywords) > 1:
            content += "猜测您可能想找：\n"
            for i, v in enumerate(possible_keywords):
                content += "{}. {}\n".format(i + 1, v)
            content += "请点击您要查询的关键词。"
            return 2,keyword,content
        else:  # len(possible_keywords) == 1
            content += "猜测您可能想找：{0}。\n".format(possible_keywords[0])
            keyword = possible_keywords[0]
            return 1,keyword,content

    def defendSQLInjectionAttack(self, content: str):
        content = re.sub("--", "——", content)
        content = re.sub(";", "；", content)
        content = re.sub("[(]", "（", content)
        content = re.sub("[)]", "）", content)
        content = re.sub("/[*]", "{", content)
        content = re.sub("[*]/", "}", content)
        while re.search("[\'\"]", content):
            content = re.sub("\"", "“", content, count=1)
            content = re.sub("\"", "”", content, count=1)
            content = re.sub("\'", "‘", content, count=1)
            content = re.sub("\'", "’", content, count=1)
        content = re.sub("union\s*select", "union_select", content, flags=re.IGNORECASE)
        content = re.sub("union\s*all\s*select", "union_all_select", content, flags=re.IGNORECASE)

        return content
