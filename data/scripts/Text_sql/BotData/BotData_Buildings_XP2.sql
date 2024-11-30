drop table if exists BotData_Buildings_XP2;
create table if not exists BotData_Buildings_XP2(id int);
drop table if exists BotData_Buildings_XP2;
create table if not exists BotData_Buildings_XP2(
    BuildingName text,
    RequiredPower int,
    ResourceTypeConvertedToPower text,
    EntertainmentBonusWithPower int,
    Pillage int
);
insert into BotData_Buildings_XP2
select 
    t1."Text" as BuildingName
    ,b_xp2.RequiredPower
    ,t2."Text" as ResourceTypeConvertedToPower
    ,b_xp2.EntertainmentBonusWithPower
    ,b_xp2.Pillage
from
    Buildings_XP2 b_xp2
left join
    Buildings b 
on
    b.BuildingType = b_xp2.BuildingType 
left join   
    Resources r
on
    r.ResourceType = b_xp2.ResourceTypeConvertedToPower
left join 
    zh_Hans_Text t1
on
    t1.Tag = b.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = r.Name 