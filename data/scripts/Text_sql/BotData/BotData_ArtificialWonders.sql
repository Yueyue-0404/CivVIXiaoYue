drop table if exists BotData_ArtificialWonders;
create table if not exists BotData_ArtificialWonders(id int);
drop table if exists BotData_ArtificialWonders;
create table BotData_ArtificialWonders(
  BuildingType TEXT,
  Name TEXT,
  Prereq TEXT,
  Cost INT,
  AdjacentDistrict TEXT,
  Description TEXT,
  RequiresRiver NUM,
  Housing INT,
  Entertainment INT,
  AdjacentResource TEXT,
  Coast NUM,
  EnabledByReligion NUM,
  AllowsHolyCity NUM,
  MustBeLake NUM,
  MustNotBeLake NUM,
  RegionalRange INT,
  AdjacentToMountain NUM,
  ObsoleteEra TEXT,
  Quote TEXT,
  QuoteAudio TEXT,
  MustBeAdjacentLand NUM,
  AdjacentCapital NUM,
  AdjacentImprovement TEXT
);
insert into BotData_ArtificialWonders
select
    b.BuildingType
    ,t1."Text" as Name
    ,case
        when tc.mark='t' then '科技：'||t2."Text"
        when tc.mark='c' then '市政：'||t2."Text"
    end as Prereq
--    ,b.PrereqTech
--    ,b.PrereqCivic
    ,b.Cost
--    ,b.MaxPlayerInstances
--    ,b.MaxWorldInstances
--    ,b.Capital
--    ,b.PrereqDistrict
    ,b.AdjacentDistrict
    ,t3."Text" as Description
--    ,b.RequiresPlacement
    ,b.RequiresRiver
--    ,b.OuterDefenseHitPoints
    ,b.Housing
    ,b.Entertainment
    ,b.AdjacentResource
    ,b.Coast
    ,b.EnabledByReligion
    ,b.AllowsHolyCity
--    ,b.PurchaseYield
--    ,b.MustPurchase
--    ,b.Maintenance
--    ,b.IsWonder
--    ,b.TraitType
--    ,b.OuterDefenseStrength
--    ,b.CitizenSlots
    ,b.MustBeLake
    ,b.MustNotBeLake
    ,b.RegionalRange
    ,b.AdjacentToMountain
    ,b.ObsoleteEra
--    ,b.RequiresReligion
--    ,b.GrantFortification
--    ,b.DefenseModifier
--    ,b.InternalOnly
--    ,b.RequiresAdjacentRiver
    ,t4."Text" as Quote
    ,b.QuoteAudio
    ,b.MustBeAdjacentLand
--    ,b.AdvisorType
    ,b.AdjacentCapital
    ,b.AdjacentImprovement
--    ,b.CityAdjacentTerrain
--    ,b.UnlocksGovernmentPolicy
--    ,b.GovernmentTierRequirement
from
    Buildings b
left join
    (select TechnologyType as "type",Name as Prereq,"t" as mark from Technologies t
    union all
    select CivicType as "type",Name as Prereq,"c" as mark from Civics c
    ) as tc
on
    b.PrereqTech = tc."type"
    or b.PrereqCivic = tc."type"
left join
    zh_Hans_Text t1
on
    b.Name = t1.Tag
left join
    zh_Hans_Text t2
on
    tc.Prereq = t2.Tag
left join
    zh_Hans_Text t3
on
    b.Description = t3.Tag
left join
    zh_Hans_Text t4
on
    b.Quote = t4.Tag
where 
    b.IsWonder = 1