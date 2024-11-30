drop table if exists BotData_Alias_Buildings;
CREATE TABLE BotData_Alias_Buildings(
	Tag TEXT,
	Truename TEXT,
	Alia TEXT
, "Type" TEXT);
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_MONUMENT_NAME','纪念碑','纪念碑','建筑'),
	 ('LOC_BUILDING_PALACE_NAME','宫殿','宫殿','建筑'),
	 ('LOC_BUILDING_BARRACKS_NAME','兵营','兵营','建筑'),
	 ('LOC_BUILDING_GRANARY_NAME','粮仓','粮仓','建筑'),
	 ('LOC_BUILDING_LIBRARY_NAME','图书馆','图书馆','建筑'),
	 ('LOC_BUILDING_SHRINE_NAME','神社','神社','建筑'),
	 ('LOC_BUILDING_WALLS_NAME','远古城墙','远古城墙','建筑'),
	 ('LOC_BUILDING_WATER_MILL_NAME','水磨','水磨','建筑'),
	 ('LOC_BUILDING_ARENA_NAME','竞技场','竞技场','建筑'),
	 ('LOC_BUILDING_LIGHTHOUSE_NAME','灯塔','灯塔','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_MARKET_NAME','市场','市场','建筑'),
	 ('LOC_BUILDING_STABLE_NAME','马厩','马厩','建筑'),
	 ('LOC_BUILDING_TEMPLE_NAME','寺庙','寺庙','建筑'),
	 ('LOC_BUILDING_STAVE_CHURCH_NAME','木板教堂','木板教堂','建筑'),
	 ('LOC_BUILDING_AMPHITHEATER_NAME','古罗马剧场','古罗马剧场','建筑'),
	 ('LOC_BUILDING_CASTLE_NAME','中世纪城墙','中世纪城墙','建筑'),
	 ('LOC_BUILDING_UNIVERSITY_NAME','大学','大学','建筑'),
	 ('LOC_BUILDING_MADRASA_NAME','伊斯兰学校','伊斯兰学校','建筑'),
	 ('LOC_BUILDING_WORKSHOP_NAME','工作坊','工作坊','建筑'),
	 ('LOC_BUILDING_ARMORY_NAME','兵工厂','兵工厂','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_SHIPYARD_NAME','造船厂','造船厂','建筑'),
	 ('LOC_BUILDING_BANK_NAME','银行','银行','建筑'),
	 ('LOC_BUILDING_STAR_FORT_NAME','文艺复兴城墙','文艺复兴城墙','建筑'),
	 ('LOC_BUILDING_MUSEUM_ART_NAME','艺术博物馆','艺术博物馆','建筑'),
	 ('LOC_BUILDING_MUSEUM_ARTIFACT_NAME','考古博物馆','考古博物馆','建筑'),
	 ('LOC_BUILDING_FACTORY_NAME','工厂','工厂','建筑'),
	 ('LOC_BUILDING_ELECTRONICS_FACTORY_NAME','电子厂','电子厂','建筑'),
	 ('LOC_BUILDING_STOCK_EXCHANGE_NAME','证券交易所','证券交易所','建筑'),
	 ('LOC_BUILDING_MILITARY_ACADEMY_NAME','军事学院','军事学院','建筑'),
	 ('LOC_BUILDING_SEWER_NAME','下水道','下水道','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_ZOO_NAME','动物园','动物园','建筑'),
	 ('LOC_BUILDING_HANGAR_NAME','机库','机库','建筑'),
	 ('LOC_BUILDING_SEAPORT_NAME','码头','码头','建筑'),
	 ('LOC_BUILDING_POWER_PLANT_EXPANSION2_NAME','核电站','核电站','建筑'),
	 ('LOC_BUILDING_BROADCAST_CENTER_NAME','广播中心','广播中心','建筑'),
	 ('LOC_BUILDING_FILM_STUDIO_NAME','电影制片厂','电影制片厂','建筑'),
	 ('LOC_BUILDING_RESEARCH_LAB_NAME','研究实验室','研究实验室','建筑'),
	 ('LOC_BUILDING_AIRPORT_NAME','机场','机场','建筑'),
	 ('LOC_BUILDING_STADIUM_NAME','体育场','体育场','建筑'),
	 ('LOC_BUILDING_CATHEDRAL_NAME','大教堂','大教堂','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_GURDWARA_NAME','谒师所','谒师所','建筑'),
	 ('LOC_BUILDING_MEETING_HOUSE_NAME','礼拜堂','礼拜堂','建筑'),
	 ('LOC_BUILDING_MOSQUE_NAME','清真寺','清真寺','建筑'),
	 ('LOC_BUILDING_PAGODA_NAME','宝塔','宝塔','建筑'),
	 ('LOC_BUILDING_SYNAGOGUE_NAME','犹太教堂','犹太教堂','建筑'),
	 ('LOC_BUILDING_WAT_NAME','佛寺','佛寺','建筑'),
	 ('LOC_BUILDING_STUPA_NAME','窣堵波','窣堵波','建筑'),
	 ('LOC_BUILDING_DAR_E_MEHR_NAME','拜火神庙','拜火神庙','建筑'),
	 ('LOC_BUILDING_TLACHTLI_NAME','蹴球场','蹴球场','建筑'),
	 ('LOC_BUILDING_PRASAT_NAME','高棉庙堂','高棉庙堂','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_SUKIENNICE_NAME','纺织会馆','纺织会馆','建筑'),
	 ('LOC_BUILDING_BASILIKOI_PAIDES_NAME','皇家学堂','皇家学堂','建筑'),
	 ('LOC_BUILDING_ORDU_NAME','斡耳朵','斡耳朵','建筑'),
	 ('LOC_BUILDING_TSIKHE_NAME','堡垒','堡垒','建筑'),
	 ('LOC_BUILDING_FERRIS_WHEEL_NAME','摩天轮','摩天轮','建筑'),
	 ('LOC_BUILDING_AQUARIUM_NAME','水族馆','水族馆','建筑'),
	 ('LOC_BUILDING_AQUATICS_CENTER_NAME','水上运动中心','水上运动中心','建筑'),
	 ('LOC_BUILDING_GOV_TALL_NAME','谒见厅','谒见厅','建筑'),
	 ('LOC_BUILDING_GOV_WIDE_NAME','祠堂','祠堂','建筑'),
	 ('LOC_BUILDING_GOV_CONQUEST_NAME','军阀宝座','军阀宝座','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_GOV_CITYSTATES_NAME','外交部','外交部','建筑'),
	 ('LOC_BUILDING_GOV_SPIES_NAME','情报局','情报局','建筑'),
	 ('LOC_BUILDING_GOV_FAITH_NAME','骑士团长礼拜堂','骑士团长礼拜堂','建筑'),
	 ('LOC_BUILDING_GOV_MILITARY_NAME','作战部','作战部','建筑'),
	 ('LOC_BUILDING_GOV_CULTURE_NAME','国家历史博物馆','国家历史博物馆','建筑'),
	 ('LOC_BUILDING_GOV_SCIENCE_NAME','皇家学会','皇家学会','建筑'),
	 ('LOC_BUILDING_FOOD_MARKET_NAME','食品市场','食品市场','建筑'),
	 ('LOC_BUILDING_SHOPPING_MALL_NAME','购物商场','购物商场','建筑'),
	 ('LOC_BUILDING_FLOOD_BARRIER_NAME','拦洪坝','拦洪坝','建筑'),
	 ('LOC_BUILDING_HYDROELECTRIC_DAM_NAME','水电站坝','水电站坝','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_COAL_POWER_PLANT_NAME','燃煤发电厂','燃煤发电厂','建筑'),
	 ('LOC_BUILDING_FOSSIL_FUEL_POWER_PLANT_NAME','燃油发电厂','燃油发电厂','建筑'),
	 ('LOC_BUILDING_GRAND_BAZAAR_NAME','大巴扎','大巴扎','建筑'),
	 ('LOC_BUILDING_MARAE_NAME','毛利会堂','毛利会堂','建筑'),
	 ('LOC_BUILDING_QUEENS_BIBLIOTHEQUE_NAME','女王图书馆','女王图书馆','建筑'),
	 ('LOC_BUILDING_THERMAL_BATH_NAME','温泉浴场','温泉浴场','建筑'),
	 ('LOC_BUILDING_GROVE_NAME','古树林','古树林','建筑'),
	 ('LOC_BUILDING_SANCTUARY_NAME','避难所','避难所','建筑'),
	 ('LOC_BUILDING_CONSULATE_NAME','领事馆','领事馆','建筑'),
	 ('LOC_BUILDING_CHANCERY_NAME','外交办','外交办','建筑');
insert into BotData_Alias_Buildings (Tag,Truename,Alia,"Type") values
	 ('LOC_BUILDING_PALGUM_NAME','沟渠','沟渠','建筑'),
	 ('LOC_BUILDING_NAVIGATION_SCHOOL_NAME','航海学校','航海学校','建筑'),
	 ('LOC_BUILDING_WALLS_NAME','远古城墙','墙','建筑'),
	 ('LOC_BUILDING_AMPHITHEATER_NAME','古罗马剧场','剧场','建筑'),
	 ('LOC_BUILDING_WORKSHOP_NAME','工作坊','作坊','建筑'),
	 ('LOC_BUILDING_WORKSHOP_NAME','工作坊','工坊','建筑'),
	 ('LOC_BUILDING_STAR_FORT_NAME','文艺复兴城墙','星型要塞','建筑'),
	 ('LOC_BUILDING_RESEARCH_LAB_NAME','研究实验室','实验室','建筑'),
	 ('LOC_BUILDING_WALLS_NAME','远古城墙','城墙','建筑');
