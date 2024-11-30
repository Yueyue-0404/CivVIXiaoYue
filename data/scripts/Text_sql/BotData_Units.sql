drop table if exists BotData_Units;
create table BotData_Units ("这行建表语句用于清除库中对表结构的缓存记忆，以防出现N/A类型字段");
drop table if exists BotData_Units;
create table BotData_Units(
  Civilization TEXT,
  Owner TEXT,
  Unitname TEXT,
  BaseSightRange INT,
  BaseMoves INT,
  Combat INT,
  RangedCombat INT,
  "Range" INT,
  Bombard INT,
  "Domain" TEXT,
  FormationClass TEXT,
  Cost INT,
  PopulationCost INT,
  FoundCity NUM,
  FoundReligion NUM,
  MakeTradeRoute NUM,
  EvangelizeBelief NUM,
  LaunchInquisition NUM,
  RequiresInquisition NUM,
  BuildCharges INT,
  ReligiousStrength INT,
  ReligionEvictPercent INT,
  SpreadCharges INT,
  ReligiousHealCharges INT,
  ExtractsArtifacts NUM,
  Description TEXT,
  Flavor TEXT,
  CanCapture NUM,
  CanRetreatWhenCaptured NUM,
  AllowBarbarians NUM,
  CostProgressionModel TEXT,
  CostProgressionParam1 INT,
  PromotionClass TEXT,
  InitialLevel INT,
  NumRandomChoices INT,
  Prereq TEXT,
  PrereqDistrict TEXT,
  PrereqPopulation INT,
  LeaderType TEXT,
  CanTrain NUM,
  StrategicResource TEXT,
  PurchaseYield TEXT,
  MustPurchase NUM,
  Maintenance INT,
  Stackable NUM,
  AirSlots INT,
  CanTargetAir NUM,
  PseudoYieldType TEXT,
  ZoneOfControl NUM,
  AntiAirCombat INT,
  Spy NUM,
  WMDCapable NUM,
  ParkCharges INT,
  IgnoreMoves NUM,
  TeamVisibility NUM,
  Obsolete TEXT,
  AdvisorType TEXT,
  EnabledByReligion NUM,
  TrackReligion NUM,
  DisasterCharges INT,
  UseMaxMeleeTrainedStrength NUM,
  ImmediatelyName NUM,
  CanEarnExperience NUM
);
insert into BotData_Units 
select
    coalesce(t2."Text",'') as Civilization
    ,coalesce(t1."Text",t2."Text",'') as Owner
    ,t3."Text" as Unitname
    ,BaseSightRange
    ,BaseMoves
    ,Combat
    ,RangedCombat
    ,"Range"
    ,Bombard
    ,case
        when "Domain" = 'DOMAIN_LAND' then '陆地'
        when "Domain" = 'DOMAIN_LAND' then '水域'
        when "Domain" = 'DOMAIN_LAND' then '天空'
    end as "Domain"
    ,t5."Text" as FormationClass
    ,Cost
    ,PopulationCost
    ,FoundCity
    ,FoundReligion
    ,MakeTradeRoute
    ,EvangelizeBelief
    ,LaunchInquisition
    ,RequiresInquisition
    ,BuildCharges
    ,ReligiousStrength
    ,ReligionEvictPercent
    ,SpreadCharges
    ,ReligiousHealCharges
    ,ExtractsArtifacts
    ,t9."Text" as Description
    ,Flavor
    ,CanCapture
    ,CanRetreatWhenCaptured
    --,unit.TraitType
    ,AllowBarbarians
    ,case
        when CostProgressionModel = 'NO_COST_PROGRESSION' then ''
        when CostProgressionModel = 'COST_PROGRESSION_GAME_PROGRESS' then '游戏进度'
        when CostProgressionModel = 'COST_PROGRESSION_PREVIOUS_COPIES' then '已建造或购买的数量'
    end as CostProgressionModel
    ,CostProgressionParam1
    ,t6."Text" as PromotionClass
    ,(InitialLevel-1) as InitialLevel
    ,NumRandomChoices
    ,case
        when pre1.pretype = 'c' then concat('市政：',t4."Text")
        when pre1.pretype = 't' then concat('科技：',t4."Text")
        when pre1.pretype is null then '无前置'
    end as Prereq
    ,PrereqDistrict
    ,PrereqPopulation
    ,unit.LeaderType
    ,case when CanTrain = 1 then 0 else 1 end as CanTrain
    ,StrategicResource
    ,t7."Text" as PurchaseYield
    ,MustPurchase
    ,Maintenance
    ,Stackable
    ,AirSlots
    ,CanTargetAir
    ,PseudoYieldType
    ,ZoneOfControl
    ,AntiAirCombat
    ,Spy
    ,WMDCapable
    ,ParkCharges
    ,IgnoreMoves
    ,TeamVisibility
    --,ObsoleteTech
    --,ObsoleteCivic
    --,MandatoryObsoleteTech
    --,MandatoryObsoleteCivic
    ,case
        when pre2.pretype = 'c' then concat('市政：',t8."Text")
        when pre2.pretype = 't' then concat('科技：',t8."Text")
        when pre2.pretype is null then ''
    end as Obsolete
    ,AdvisorType
    ,EnabledByReligion
    ,TrackReligion
    ,DisasterCharges
    ,UseMaxMeleeTrainedStrength
    ,ImmediatelyName
    ,CanEarnExperience
from
    Units unit
left join
    (select CivilizationType as "Type",TraitType from CivilizationTraits ct 
        union all
    select LeaderType as "Type",TraitType from LeaderTraits lt 
    ) trait
on
    unit.TraitType = trait.TraitType
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
    (select TechnologyType as "Type",Name,'t' as "pretype" from Technologies
    union all
    select CivicType as "Type",Name,'c' as "pretype" from Civics
    ) pre1
on
    pre1."Type" = unit.PrereqTech 
    or pre1."Type" = unit.PrereqCivic 
left join
    UnitFormationClasses as formation
on
    formation.FormationClassType = unit.FormationClass
left join 
    UnitPromotionClasses as promo
on
    promo.PromotionClassType = unit.PromotionClass 
left join
    Yields y 
on 
    y.YieldType = unit.PurchaseYield 
left join 
    (select TechnologyType as "Type",Name,'t' as "pretype" from Technologies
    union all
    select CivicType as "Type",Name,'c' as "pretype" from Civics
    ) pre2
on
    pre2."Type" = unit.ObsoleteTech
    or pre2."Type" = unit.MandatoryObsoleteTech
    or pre2."Type" = unit.ObsoleteCivic 
    or pre2."Type" = unit.MandatoryObsoleteCivic
left join 
    zh_Hans_Text t1
on
    t1."Tag" = l.Name
left join 
    zh_Hans_Text t2
on
    t2."Tag" = c.Name
left join 
    zh_Hans_Text t3
on
    t3."Tag" = unit.Name
left join 
    zh_Hans_Text t4
on
    t4."Tag" = pre1.Name
left join 
    zh_Hans_Text t5
on
    t5."Tag" = formation.Name
left join 
    zh_Hans_Text t6
on
    t6."Tag" = promo.Name 
left join 
    zh_Hans_Text t7
on 
    t7."Tag" = y.Name 
left join
    zh_Hans_Text t8
on 
    t8."Tag" = pre2.Name
left join
    zh_Hans_Text t9
on
    t9."Tag" = unit.Description