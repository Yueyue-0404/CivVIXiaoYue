drop table if exists BotData_Building_CitizenYieldChanges;
create table if not exists BotData_Building_CitizenYieldChanges(id int);
drop table if exists BotData_Building_CitizenYieldChanges;
create table if not exists BotData_Building_CitizenYieldChanges(
    BuildingType text
    ,YieldType text
    ,YieldChange int
);
insert into BotData_Building_CitizenYieldChanges
select 
    t1."Text" as BuildingType
    ,t2."Text" as YieldType
    ,bcyc.YieldChange
from 
    Building_CitizenYieldChanges bcyc 
left join
    Buildings b 
on
    bcyc.BuildingType = b.BuildingType 
left join 
    Yields y 
on
    bcyc.YieldType = y.YieldType 
left join
    zh_Hans_Text t1
on
    t1.Tag = b.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = y.Name 
