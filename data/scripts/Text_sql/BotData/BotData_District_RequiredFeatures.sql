drop table if exists BotData_District_RequiredFeatures;
create table if not exists BotData_District_RequiredFeatures(id int);
drop table if exists BotData_District_RequiredFeatures;
create table if not exists BotData_District_RequiredFeatures(
    DistrictName text
    ,Feature text
);
insert into BotData_District_RequiredFeatures
select 
    t1."Text" as DistrictName
    ,t2."Text" as Terrain
from 
    District_RequiredFeatures dr
left join
    Districts d
on
    dr.DistrictType = d.DistrictType 
left join 
    Features f
on
    f.FeatureType  = dr.FeatureType 
left join 
    zh_Hans_Text t1
on  
    t1.Tag = d.Name 
left join   
    zh_Hans_Text t2
on
    t2.Tag = f.Name 
;