drop table if exists BotData_NatureWonders;
create table if not exists BotData_NatureWonders(id int);
drop table if exists BotData_NatureWonders;
create table BotData_NatureWonders(
FeatureType Text
,Name Text
,Description Text
,Quote Text
);
insert into BotData_NatureWonders
select 
    FeatureType
    ,t1."Text" as Name
    ,t2."Text" as Description
    ,t3."Text" as Quote
--    ,f.Coast
--    ,f.NoCoast
--    ,f.NoRiver
--    ,f.NoAdjacentFeatures
--    ,f.RequiresRiver
--    ,f.MovementChange
--    ,f.SightThroughModifier
--    ,f.Impassable
--    ,f.NaturalWonder
--    ,f.RemoveTech
--    ,f.Removable
--    ,f.AddCivic
--    ,f.DefenseModifier
--    ,f.AddsFreshWater
--    ,f.Appeal
--    ,f.MinDistanceLand
--    ,f.MaxDistanceLand
--    ,f.NotNearFeature
--    ,f.Lake
--    ,f.Tiles
--    ,f.Adjacent
--    ,f.NoResource
--    ,f.DoubleAdjacentTerrainYield
--    ,f.NotCliff
--    ,f.MinDistanceNW
--    ,f.CustomPlacement
--    ,f.Forest
--    ,f.AntiquityPriority
--    ,f.QuoteAudio
--    ,f.Settlement
--    ,f.FollowRulesInWB
--    ,f.DangerValue
from 
    Features f
left join
    zh_Hans_Text t1
on
    f.Name = t1.Tag 
left join 
    zh_Hans_Text t2
on  
    f.Description = t2.Tag 
left join 
    zh_Hans_Text t3
on
    f.Quote = t3.Tag
where 
    f.NaturalWonder = 1
