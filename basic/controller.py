import yaml
import pypinyin, jieba
import re
from .settings import *
from .accessor import DataAccesser

with open(CONFIG_DIR.joinpath("commands.yaml")) as file:
    command_dict = yaml.safe_load(file)

with open(CONFIG_DIR.joinpath("command_target_types.yaml")) as file:
    command_target_types = yaml.safe_load(file)


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

    def deleteLettersAndNumbersFromKeyword(self, keyword: str):
        """
            该函数只负责剔除字符串中的英文字符
            因为后续要经过pypinyin处理，它会自动将汉字和其他字符分组出去，
            而只要先剔除英文字符，就可以在后续轻松通过for循环来找出哪个元素是拼音，哪个元素是杂鱼
        """
        re_res = re.search("[A-Za-z]", keyword)
        if re_res:
            keyword = re.sub("[A-Za-z]", "", keyword)
        return keyword

    def checkWrong(self, keyword):
        pinyin_of_keyword = pypinyin.lazy_pinyin(keyword)
        correct_key_word = ""
        return correct_key_word
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
            keywords_selected = self.checkInNameTable(keyword,command_index)
            if not keywords_selected:
                content += "找不到您要查询的关键词。"
                return content
            elif type(keywords_selected) == str:
                content += "您要查询的关键词{0}是{1}的别称，因此为您查询{1}。\n".format(keyword,keywords_selected)
                keyword = keywords_selected
            elif type(keywords_selected) == list:
                content += "您要查询的关键词应该是个别称，下面是几种可能性：\n"
                for i, v in enumerate(keywords_selected):
                    content += "{}. {}\n".format(i, v)
                content += "请点击您要查询的关键词。"
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
                content += "未知错误，多次出现请联系作者"
            return content

    def checkInNameTable(self,keyword,command_index):
        exists, keyword_selected = self.accesser.findName(keyword,command_target_types[command_index])
        if not exists:
            return False
        else:
            return keyword_selected

    def defendSQLInjectionAttack(self,content:str):
        content = re.sub("--", "——", content)
        content = re.sub(";", "；", content)
        content = re.sub("[(]", "（", content)
        content = re.sub("[)]", "）", content)
        content = re.sub("/[*]", "{", content)
        content = re.sub("[*]/", "}", content)
        while re.search("[\'\"]",content):
            content = re.sub("\"", "“", content,count=1)
            content = re.sub("\"", "”", content,count=1)
            content = re.sub("\'", "‘", content,count=1)
            content = re.sub("\'", "’", content,count=1)
        content = re.sub("union\s*select","union_select",content,flags=re.IGNORECASE)
        content = re.sub("union\s*all\s*select","union_all_select",content,flags=re.IGNORECASE)

        return content
