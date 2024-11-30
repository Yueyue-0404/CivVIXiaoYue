drop table if exists BotData_Building_YieldDistrictCopies;
create table if not exists BotData_Building_YieldDistrictCopies(id int);
drop table if exists BotData_Building_YieldDistrictCopies;
create table if not exists BotData_Building_YieldDistrictCopies(
    BuildingName TEXT,
    OldYieldType TEXT,
    NewYieldType TEXT
);
insert into BotData_Building_YieldDistrictCopies 
select
    t1."Text" as BuildingName
    ,t2."Text" as OldYieldType
    ,t3."Text" as NewYieldType
from
    Building_YieldDistrictCopies "by"
left join
    Buildings b
on  
    b.BuildingType = "by".BuildingType 
left join   
    Yields y1
on
    y1.YieldType = "by".OldYieldType 
left join   
    Yields y2
on
    y2.YieldType = "by".NewYieldType 
left join   
    zh_Hans_Text t1
on
    t1.Tag = b.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = y1.Name 
left join   
    zh_Hans_Text t3
on
    t3.Tag = y2.Name 