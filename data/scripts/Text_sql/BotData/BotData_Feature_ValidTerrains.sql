drop table if exists BotData_Feature_ValidTerrains;
create table if not exists BotData_Feature_ValidTerrains(id int);
drop table if exists BotData_Feature_ValidTerrains;
create table BotData_Feature_ValidTerrains(
Feature Text
,Terrain Text
);
insert into BotData_Feature_ValidTerrains
select
    t1."Text" as Feature
    ,t2."Text" as Terrain
from
    Feature_ValidTerrains fv
left join
    Features f
on
    f.FeatureType = fv.FeatureType 
left join 
    Terrains t
on
    t.TerrainType = fv.TerrainType 
left join
    zh_Hans_Text t1
on
    t1.Tag = f.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = t.Name 