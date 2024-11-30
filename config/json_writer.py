import json
from pathlib import Path

data = {
    "basic_info": {
        "Prereq": "{} 解锁",
        "Coast": "是必须建造在水域上的区域",
        "Cost": "基础花费{}锤",
        "RequiresPopulation": "需要有足够的人口才能建造",
        "PlunderType": "掠夺{}",
        "CostProgressionModel": "区域涨价机制：{}",
        "Appeal": "令周围的陆地单元格魅力{}",
        "Entertainment": "提供{}宜居度",
        "Housing": "提供{}住房",
        "OnePerCity": "每座城市仅限建造一个",
        "Maintenance": "维护费：{}金/回合",
    },
    "special_info": {
        "NoAdjacentCity": "不能与市中心相邻",
        "ZOC": "能对周围的单元格施加控制区",
        "FreeEmbark": "能免除在此处上下船的行动力惩罚",
        "TradeEmbark": "商人可以在此处上下船",
        "HitPoints": "拥有{}生命值上限",
        "CaptureRemovesBuildings": "被占领时，其所有建筑都会被摧毁",
        "CaptureRemovesCityDefenses": "被占领时，摧毁城市的防御设施",
        "CaptureRemovesDistrict": "被占领时该区域会被摧毁",
        "MilitaryDomain": "建成后将成为{}的出生点",
        "AirSlots": "能提供{}个停机位",
        "TravelTime": "该区域会为敌国间谍提供一个需要{}回合潜逃回国的路线选择",
        "CityStrengthModifier": "该区域能令城市的防御力提高{}点",
        "AdjacentToLand": "必须紧靠陆地",
        "MaxPerPlayer": "该区域整个国家只能建造{}个"
    },
    "no_use": {
        "RequiresPlacement": "不知道是什么，需要地块？",
        "CityCenter": "是市中心",
        "Aqueduct": "是引水渠",
        "InternalOnly": "都是0，不知道啥意思",
        "PlunderAmount": "基础掠夺收益系数",
        "CostProgressionParam1": "涨价步长",
        "AllowsHolyCity": "允许成为圣城？",
        "CitizenSlots": "看起来像塞专家的字段，但全是null",
        "CanAttack": "能否攻击，可能是建墙以后会变的字段",
        "AdvisorType": "顾问，啥用没有",
    },
}


def write_into_json(json_path: Path, data: dict or list):
    with open(json_path, mode="w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


write_into_json(Path.cwd().joinpath("districtdata.json"),data)