drop table if exists BotData_District_CitizenYieldChanges;
create table if not exists BotData_District_CitizenYieldChanges(id int);
drop table if exists BotData_District_CitizenYieldChanges;
create table if not exists BotData_District_CitizenYieldChanges(
    DistrictName TEXT
    ,YieldName TEXT
    ,YieldChange INT
);
insert into BotData_District_CitizenYieldChanges
select 
    t1."Text" as DistrictName
    ,t2."Text" as YieldName
    ,dc.YieldChange
from 
    District_CitizenYieldChanges dc
left join
    Districts d
on
    dc.DistrictType = d.DistrictType 
left join 
    Yields y
on
    dc.YieldType = y.YieldType 
left join 
    zh_Hans_Text t1
on
    t1.Tag = d.Name 
left join   
    zh_Hans_Text t2
on  
    t2.Tag = y.Name 
;