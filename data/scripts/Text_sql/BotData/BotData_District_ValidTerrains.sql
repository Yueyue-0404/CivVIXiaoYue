drop table if exists BotData_District_ValidTerrains;
create table if not exists BotData_District_ValidTerrains(id int);
drop table if exists BotData_District_ValidTerrains;
create table if not exists BotData_District_ValidTerrains(
    DistrictName text
    ,Terrain text
);
insert into BotData_District_ValidTerrains 
select 
    t1."Text" as DistrictName
    ,t2."Text" as Terrain
from 
    District_ValidTerrains dv
left join
    Districts d
on
    dv.DistrictType = d.DistrictType 
left join 
    Terrains t 
on
    t.TerrainType = dv.TerrainType 
left join 
    zh_Hans_Text t1
on  
    t1.Tag = d.Name 
left join   
    zh_Hans_Text t2
on
    t2.Tag = t.Name 
;