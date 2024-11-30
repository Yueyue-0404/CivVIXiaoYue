drop table if exists BotData_District_AdjacencyYieldChanges;
create table if not exists BotData_District_AdjacencyYieldChanges(id int);
drop table if exists BotData_District_AdjacencyYieldChanges;
create table if not exists BotData_District_AdjacencyYieldChanges(
    DistrictName TEXT
    ,YieldChange TEXT
);
insert into BotData_District_AdjacencyYieldChanges
select 
    t1."Text" as DistrictName
    ,case
        when ay."Self" = 1 then '无条件'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentRiver = 1 then '在河流旁边'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentResource = 1 and ay.AdjacentResourceClass = 'NO_RESOURCECLASS' then'每与'||ay.TilesRequired||'个任意资源'||'相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentResourceClass = 'RESOURCECLASS_STRATEGIC' then'每与'||ay.TilesRequired||'个战略资源'||'相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentResourceClass = 'RESOURCECLASS_LUXURY' then'每与'||ay.TilesRequired||'个奢侈品资源'||'相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentResourceClass = 'RESOURCECLASS_BONUS' then'每与'||ay.TilesRequired||'个加成资源'||'相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentWonder = 1 then '每与'||ay.TilesRequired||'个人造奇观相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentNaturalWonder = 1 then '每与'||ay.TilesRequired||'个自然奇观相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.AdjacentSeaResource = 1 then '每与'||ay.TilesRequired||'个海洋资源相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        when ay.OtherDistrictAdjacent = 1 then '每与'||ay.TilesRequired||'个区域相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
        else '每与'||ay.TilesRequired||'个'||t3."Text"||'相邻'||case when ay.YieldChange>=0 then '+'||ay.YieldChange else ay.YieldChange end||t2."Text"
    end as YieldChange
from
    District_Adjacencies as da
left join
    Districts as d
on  
    da.DistrictType = d.DistrictType 
left join 
    Adjacency_YieldChanges as ay
on
    da.YieldChangeId = ay.ID 
left join 
    Yields y 
on
    ay.YieldType = y.YieldType 
left join
    (select t.TerrainType as "type",Name from Terrains as t
    union all
    select f.FeatureType as "type",Name from Features as f
    union all
    select d.DistrictType as "type",Name from Districts as d
    union all
    select i.ImprovementType as "type",Name from Improvements as i
    ) tile
on 
    ay.AdjacentTerrain = tile."type"
    or ay.AdjacentFeature = tile."type"
    or ay.AdjacentDistrict = tile."type"
    or ay.AdjacentImprovement = tile."type"
left join 
    zh_Hans_Text t1
on
    t1.Tag = d.Name
left join 
    zh_Hans_Text t2
on
    t2.Tag = y.Name 
left join 
    zh_Hans_Text t3
on
    t3.Tag = tile.Name
left join 
    zh_Hans_Text t4
on
    t4.Tag = ay.Description
;