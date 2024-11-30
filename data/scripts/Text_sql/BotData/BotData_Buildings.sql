drop table if exists BotData_Buildings;
create table if not exists BotData_Buildings(id int);
drop table if exists BotData_Buildings;
CREATE TABLE BotData_Buildings(
  Civilization TEXT,
  Owner TEXT,
  Name TEXT,
  Prereq TEXT,
  Cost INT,
  MaxPlayerInstances INT,
  MaxWorldInstances INT,
  Capital NUM,
  PrereqDistrict TEXT,
  AdjacentDistrict TEXT,
  Description TEXT,
  RequiresPlacement NUM,
  RequiresRiver NUM,
  OuterDefenseHitPoints INT,
  Housing INT,
  Entertainment INT,
  AdjacentResource TEXT,
  Coast NUM,
  EnabledByReligion NUM,
  AllowsHolyCity NUM,
  PurchaseYield TEXT,
  MustPurchase NUM,
  Maintenance INT,
  IsWonder NUM,
  TraitType TEXT,
  OuterDefenseStrength INT,
  CitizenSlots INT,
  MustBeLake NUM,
  MustNotBeLake NUM,
  RegionalRange INT,
  AdjacentToMountain NUM,
  RequiresReligion NUM,
  GrantFortification INT,
  DefenseModifier INT,
  InternalOnly NUM,
  RequiresAdjacentRiver NUM,
  Quote TEXT,
  QuoteAudio TEXT,
  MustBeAdjacentLand NUM,
  AdjacentCapital NUM,
  AdjacentImprovement TEXT,
  CityAdjacentTerrain TEXT,
  UnlocksGovernmentPolicy NUM,
  GovernmentTierRequirement TEXT
);
insert into BotData_Buildings
select 
    coalesce(t5."Text",'') as Civilization
    ,coalesce(t4."Text",t5."Text",'') as Owner
--    ,b.BuildingType
    ,t1."Text" as Name
    ,case
        when tc.mark='t' then '科技：'||t2."Text"
        when tc.mark='c' then '市政：'||t2."Text"
    end as Prereq
--    ,b.PrereqTech
--    ,b.PrereqCivic
    ,b.Cost
    ,b.MaxPlayerInstances
    ,b.MaxWorldInstances
    ,b.Capital
    ,t6."Text" as PrereqDistrict
    ,b.AdjacentDistrict
    ,t3."Text" as Description
    ,b.RequiresPlacement
    ,b.RequiresRiver
    ,b.OuterDefenseHitPoints
    ,b.Housing
    ,b.Entertainment
    ,b.AdjacentResource
    ,b.Coast
    ,b.EnabledByReligion
    ,b.AllowsHolyCity
    ,t7."Text" as PurchaseYield
    ,b.MustPurchase
    ,b.Maintenance
    ,b.IsWonder
    ,b.TraitType
    ,b.OuterDefenseStrength
    ,b.CitizenSlots
    ,b.MustBeLake
    ,b.MustNotBeLake
    ,b.RegionalRange
    ,b.AdjacentToMountain
--    ,b.ObsoleteEra
    ,b.RequiresReligion
    ,b.GrantFortification
    ,b.DefenseModifier
    ,b.InternalOnly
    ,b.RequiresAdjacentRiver
    ,b.Quote
    ,b.QuoteAudio
    ,b.MustBeAdjacentLand
--    ,b.AdvisorType
    ,b.AdjacentCapital
    ,b.AdjacentImprovement
    ,b.CityAdjacentTerrain
    ,b.UnlocksGovernmentPolicy
    ,b.GovernmentTierRequirement
from
    Buildings b 
left join
    (select CivilizationType as "Type",TraitType from CivilizationTraits ct 
        union all
    select LeaderType as "Type",TraitType from LeaderTraits lt 
    ) trait
on
    b.TraitType = trait.TraitType
left join
    Leaders l
on
    l.LeaderType = trait."Type"
left join 
    CivilizationLeaders cl
on
    cl.LeaderType = l.LeaderType
left join
    Civilizations c 
on
    c.CivilizationType = trait."Type"
    or cl.CivilizationType = c.CivilizationType
left join
    (select TechnologyType as "type",Name as Prereq,"t" as mark from Technologies t
    union all
    select CivicType as "type",Name as Prereq,"c" as mark from Civics c
    ) as tc
on
    b.PrereqTech = tc."type"
    or b.PrereqCivic = tc."type"
left join
    Districts d
on
    d.DistrictType = b.PrereqDistrict
left join
    Yields y 
on
    y.YieldType = b.PurchaseYield 
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
    t4."Tag" = l.Name
left join 
    zh_Hans_Text t5
on
    t5."Tag" = c.Name
left join
    zh_Hans_Text t6
on
    t6.Tag = d.Name 
left join
    zh_Hans_Text t7
on
    y.Name = t7.Tag 
where 
    b.IsWonder = 0