drop table if exists BotData_Unique_Districts;
CREATE TABLE if not exists BotData_Unique_Districts(id int);
drop table if exists BotData_Unique_Districts;
CREATE TABLE if not exists BotData_Unique_Districts(
  Civilization TEXT,
  Owner TEXT,
  DistrictName TEXT,
  DistrictType TEXT,
  Prereq TEXT,
  Coast NUM,
  Description TEXT,
  Cost INT,
  RequiresPlacement NUM,
  RequiresPopulation NUM,
  NoAdjacentCity NUM,
  CityCenter NUM,
  Aqueduct NUM,
  InternalOnly NUM,
  ZOC NUM,
  FreeEmbark NUM,
  HitPoints INT,
  CaptureRemovesBuildings NUM,
  CaptureRemovesCityDefenses NUM,
  PlunderType TEXT,
  PlunderAmount INT,
  TradeEmbark NUM,
  MilitaryDomain TEXT,
  CostProgressionModel TEXT,
  CostProgressionParam1 INT,
  Appeal INT,
  Housing INT,
  Entertainment INT,
  OnePerCity NUM,
  AllowsHolyCity NUM,
  Maintenance INT,
  AirSlots INT,
  CitizenSlots INT,
  TravelTime INT,
  CityStrengthModifier INT,
  AdjacentToLand NUM,
  CanAttack NUM,
  AdvisorType TEXT,
  CaptureRemovesDistrict NUM,
  MaxPerPlayer REAL
);
insert into BotData_Unique_Districts
select
    coalesce(t5."Text",'') as Civilization
    ,coalesce(t4."Text",t5."Text",'') as Owner
    ,t1."Text" as DistrictName
    ,d.DistrictType
    ,case
        when tc.mark='t' then '科技：'||t2."Text"
        when tc.mark='c' then '市政：'||t2."Text"
    end as Prereq
    ,d.Coast
    ,t3."Text" as Description
    ,d.Cost
    ,d.RequiresPlacement
    ,d.RequiresPopulation
    ,d.NoAdjacentCity
    ,d.CityCenter
    ,d.Aqueduct
    ,d.InternalOnly
    ,d.ZOC
    ,d.FreeEmbark
    ,d.HitPoints
    ,d.CaptureRemovesBuildings
    ,d.CaptureRemovesCityDefenses
    ,case
        when d.PlunderType = 'NO_PLUNDER' then '不提供任何产出'
        when d.PlunderType = 'PLUNDER_FAITH' then '后将获得信仰值'
        when d.PlunderType = 'PLUNDER_SCIENCE' then '后将获得科技值'
        when d.PlunderType = 'PLUNDER_GOLD' then '后将获得金币'
        when d.PlunderType = 'PLUNDER_HEAL' then '后单位将获得50HP的治疗'
        when d.PlunderType = 'PLUNDER_CULTURE' then '后将获得文化值'
    end as PlunderType
    ,d.PlunderAmount
    ,d.TradeEmbark
    ,case
        when d.MilitaryDomain = 'NO_DOMAIN' then ''
        when d.MilitaryDomain = 'DOMAIN_LAND' then '陆军'
        when d.MilitaryDomain = 'DOMAIN_SEA' then '海军'
        when d.MilitaryDomain = 'DOMAIN_AIR' then '空军'
    end as MilitaryDomain
    ,case
        when CostProgressionModel = 'NO_COST_PROGRESSION' then '该区域不会涨价'
        when CostProgressionModel = 'COST_PROGRESSION_GAME_PROGRESS' then '文明发展进程'
        when CostProgressionModel = 'COST_PROGRESSION_NUM_UNDER_AVG_PLUS_TECH' then '文明发展进程与六折机制'
    end as CostProgressionModel
    ,d.CostProgressionParam1
    ,case
        when d.Appeal > 0 then '+'||d.Appeal
        else d.Appeal
    end as Appeal
    ,d.Housing
    ,d.Entertainment
    ,d.OnePerCity
    ,d.AllowsHolyCity
    ,d.Maintenance
    ,d.AirSlots
    ,d.CitizenSlots
    ,case
        when d.TravelTime = -1 then 0
        else d.TravelTime
    end as TravelTime
    ,d.CityStrengthModifier
    ,d.AdjacentToLand
    ,d.CanAttack
    ,d.AdvisorType
    ,d.CaptureRemovesDistrict
    ,case
        when d.MaxPerPlayer = -1 then 0
        else d.MaxPerPlayer
    end as MaxPerPlayer
from 
    Districts as d
left join
    (select TechnologyType as "type",Name as Prereq,"t" as mark from Technologies t
    union all
    select CivicType as "type",Name as Prereq,"c" as mark from Civics c
    ) as tc
on
    d.PrereqTech = tc."type"
    or d.PrereqCivic = tc."type"
left join
    (select CivilizationType as "Type",TraitType from CivilizationTraits ct 
        union all
    select LeaderType as "Type",TraitType from LeaderTraits lt 
    ) trait
on
    d.TraitType = trait.TraitType
left join
    Leaders l
on
    l.LeaderType = trait."Type"
left join 
    CivilizationLeaders cl
on
    cl.LeaderType = l.LeaderType
left join
    Civilizations c 
on
    c.CivilizationType = trait."Type"
    or cl.CivilizationType = c.CivilizationType
left join
    zh_Hans_Text t1
on
    d.Name = t1.Tag 
left join 
    zh_Hans_Text t2
on
    tc.Prereq = t2.Tag 
left join
    zh_Hans_Text t3
on
    d.Description = t3.Tag 
left join 
    zh_Hans_Text t4
on
    t4."Tag" = l.Name
left join 
    zh_Hans_Text t5
on
    t5."Tag" = c.Name
where 
    DistrictType != 'DISTRICT_WONDER'
    and trait."Type" is not null;