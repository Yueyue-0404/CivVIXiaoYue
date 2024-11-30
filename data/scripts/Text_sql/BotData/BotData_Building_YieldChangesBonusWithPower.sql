drop table if exists BotData_Building_YieldChangesBonusWithPower;
create table if not exists BotData_Building_YieldChangesBonusWithPower(id int);
drop table if exists BotData_Building_YieldChangesBonusWithPower;
create table if not exists BotData_Building_YieldChangesBonusWithPower(
    BuildingName TEXT,
    Yield TEXT,
    YieldChange int
);
insert into BotData_Building_YieldChangesBonusWithPower
select 
    t1."Text" as BuildingName
    ,t2."Text" as Yield
    ,"by".YieldChange
from
    Building_YieldChangesBonusWithPower "by"
left join
    Buildings b
on
    b.BuildingType = "by".BuildingType 
left join   
    Yields y 
on
    y.YieldType = "by".YieldType 
left join   
    zh_Hans_Text t1
on
    t1.Tag = b.Name 
left join   
    zh_Hans_Text t2
on
    t2.Tag = y.Name