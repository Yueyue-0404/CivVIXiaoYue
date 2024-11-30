drop table if exists BotData_District_GreatPersonPoints;
create table if not exists BotData_District_GreatPersonPoints(iud int);
drop table if exists BotData_District_GreatPersonPoints;
create table if not exists BotData_District_GreatPersonPoints(
    DistrictName TEXT
    ,GreatPersonClassName TEXT
    ,PointsPerTurn INT
);
insert into BotData_District_GreatPersonPoints
select 
    t1."Text" as DistrictName
    ,t2."Text" as GreatPersonClassName
    ,PointsPerTurn
from 
    District_GreatPersonPoints dg
left join
    Districts d
on
    dg.DistrictType = d.DistrictType 
left join 
    GreatPersonClasses gpc 
on
    dg.GreatPersonClassType = gpc.GreatPersonClassType 
left join 
    zh_Hans_Text t1
on
    t1.Tag = d.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = gpc.Name 
;