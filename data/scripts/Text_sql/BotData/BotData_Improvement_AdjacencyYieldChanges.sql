drop table if exists BotData_Improvement_AdjacencyYieldChanges;
CREATE TABLE if not exists BotData_Improvement_AdjacencyYieldChanges(id int);
drop table if exists BotData_Improvement_AdjacencyYieldChanges;
CREATE TABLE if not exists BotData_Improvement_AdjacencyYieldChanges(
  ImprovementType TEXT,
  YieldChange TEXT,
  Prereq TEXT,
  Obsolete TEXT
);
insert into BotData_Improvement_AdjacencyYieldChanges
select 
    ia.ImprovementType
--    ,ia.YieldChangeId
--    ,ay.ID
--    ,ay.Description
    ,case
        when ay.OtherDistrictAdjacent != 0 then '每与'||ay.TilesRequired||'个区域相邻+'||YieldChange||t1."Text"
        when ay.AdjacentSeaResource != 0 then '每与'||ay.TilesRequired||'个水域资源相邻+'||YieldChange||t1."Text"
        when coalesce(ay.AdjacentTerrain,ay.AdjacentFeature) is not null then '每与'||ay.TilesRequired||'个'||t8."Text" ||'相邻+'||YieldChange||t1."Text"
        when AdjacentRiver != 0 then '与河流相邻+'||YieldChange||t1."Text"
        when AdjacentWonder != 0 then '每与'||ay.TilesRequired||'个人造奇观相邻+'||YieldChange||t1."Text"
        when AdjacentNaturalWonder != 0 then '每与'||ay.TilesRequired||'个自然奇观相邻+'||YieldChange||t1."Text"
        when coalesce(ay.AdjacentImprovement,ay.AdjacentDistrict) is not null then '每与'||ay.TilesRequired||'个'||t2."Text" ||'相邻+'||YieldChange||t1."Text"
        when ay.AdjacentResourceClass != 'NO_RESOURCECLASS' then '每与'||ay.TilesRequired||'个'||t9."Text" ||'相邻+'||YieldChange||t1."Text"
    end as YieldChange
--    ,t1."Text" as YieldType
--    ,ay.YieldChange
--    ,ay.TilesRequired
--    ,ay.OtherDistrictAdjacent
--    ,ay.AdjacentSeaResource
--    ,ay.AdjacentTerrain
--    ,ay.AdjacentFeature
--    ,ay.AdjacentRiver
--    ,ay.AdjacentWonder
--    ,ay.AdjacentNaturalWonder
--    ,t2."Text" as AdjacentArtificial
----    ,t2."Text" as AdjacentImprovement
----    ,t3."Text" as AdjacentDistrict
    ,case
        when ay.PrereqCivic is not null then '市政：'||t4."Text"
        when ay.PrereqTech is not null then '科技：'||t5."Text"
        else ''
    end as Prereq
    ,case
        when ay.ObsoleteCivic is not null then '市政：'||t6."Text"
        when ay.ObsoleteTech is not null then '科技：'||t7."Text"
        else ''
    end as Obsolete
--    ,ay.AdjacentResource
--    ,case 
--        when ay.AdjacentResourceClass = 'NO_RESOURCECLASS' then ''
--        when ay.AdjacentResourceClass = 'RESOURCECLASS_BONUS' then '加成资源'
--        when ay.AdjacentResourceClass = 'RESOURCECLASS_LUXURY' then '奢侈资源'
--        when ay.AdjacentResourceClass = 'RESOURCECLASS_STRATEGIC' then '战略资源'
--    end
--    ,ay."Self"
from
    Improvement_Adjacencies as ia
left join
    Adjacency_YieldChanges as ay
on
    ia.YieldChangeId = ay.ID
left join 
    Yields y 
on
    y.YieldType = ay.YieldType 
left join 
    Improvements i
on
    i.ImprovementType = ay.AdjacentImprovement
left join 
    Districts d 
on
    d.DistrictType = ay.AdjacentDistrict 
left join 
    Civics c1
on
    c1.CivicType = ay.PrereqCivic 
left join 
    Technologies tech1
on
    tech1.TechnologyType  = ay.PrereqTech  
left join 
    Civics c2
on
    c2.CivicType = ay.ObsoleteCivic 
left join 
    Technologies tech2
on
    tech2.TechnologyType  = ay.ObsoleteTech 
left join 
    Terrains as terrains
on
    terrains.TerrainType = ay.AdjacentTerrain
left join 
    Features as features
on
    features.FeatureType  = ay.AdjacentFeature
left join 
    zh_Hans_Text t1
on
    t1.Tag = y.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = i.Name 
    or t2.Tag = d.Name 
left join 
    zh_Hans_Text t4
on
    t4.Tag = c1.Name 
left join 
    zh_Hans_Text t5
on
    t5.Tag = tech1.Name 
left join 
    zh_Hans_Text t6
on
    t6.Tag = c2.Name 
left join 
    zh_Hans_Text t7
on
    t7.Tag = tech2.Name 
left join 
    zh_Hans_Text t8
on
    t8.Tag = terrains.Name 
    or t8.Tag = features.Name 
left join 
    (select 'NO_RESOURCECLASS' as Tag,'' as Text union all
     select 'RESOURCECLASS_BONUS','加成资源' union all
     select 'RESOURCECLASS_LUXURY','奢侈资源' union all
     select 'RESOURCECLASS_STRATEGIC','战略资源'
    ) as t9
on
    t9.Tag = ay.AdjacentResourceClass 
