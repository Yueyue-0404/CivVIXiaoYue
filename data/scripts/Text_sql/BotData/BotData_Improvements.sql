drop table if exists BotData_Improvements;
create table BotData_Improvements(id int);
drop table if exists BotData_Improvements;
CREATE TABLE if not exists BotData_Improvements(
  Civilization TEXT,
  Owner TEXT,
  Improvementname TEXT,
  Builderunit TEXT,
  ImprovementType TEXT,
  BarbarianCamp NUM,
  Prereq TEXT,
  Buildable NUM,
  Description TEXT,
  RemoveOnEntry NUM,
  DispersalGold INT,
  PlunderType TEXT,
  PlunderAmount INT,
  Goody NUM,
  TilesPerGoody INT,
  GoodyRange INT,
  Icon TEXT,
  Housing1 NUM,
  SameAdjacentInvalid NUM,
  RequiresRiver INT,
  EnforceTerrain NUM,
  BuildInLine NUM,
  CanBuildOutsideTerritory NUM,
  BuildOnFrontier NUM,
  AirSlots INT,
  DefenseModifier INT,
  GrantFortification INT,
  MinimumAppeal INT,
  Coast NUM,
  YieldFromAppeal,
  WeaponSlots INT,
  ReligiousUnitHealRate INT,
  Appeal TEXT,
  OnePerCity NUM,
  ValidAdjacentTerrainAmount INT,
  Domain TEXT,
  AdjacentSeaResource NUM,
  RequiresAdjacentBonusOrLuxury NUM,
  MovementChange INT,
  Unworkable INT,
  ImprovementOnRemove TEXT,
  GoodyNotify NUM,
  NoAdjacentSpecialtyDistrict NUM,
  RequiresAdjacentLuxury NUM,
  AdjacentToLand NUM,
  Unremovable NUM,
  OnlyOpenBorders NUM,
  Capturable NUM,
  AllowImpassableMovement INT,
  BuildOnAdjacentPlot INT,
  PreventsDrought INT,
  DisasterResistant INT
);
insert into BotData_Improvements
select
    t3."Text" as Civilization
    ,coalesce(t2."Text",t3."Text") as Owner
    ,t1."Text" as Improvementname
    ,t7."Text" as Builderunit
    ,imp.ImprovementType
    ,imp.BarbarianCamp
    ,case
        when pre1.pretype = 'c' then concat('市政：',t4."Text")
        when pre1.pretype = 't' then concat('科技：',t4."Text")
        when pre1.pretype is null then '无前置'
    end as Prereq
    --,imp.PrereqTech
    --,imp.PrereqCivic
    ,imp.Buildable
    ,t5."Text" as Description
    ,imp.RemoveOnEntry
    ,imp.DispersalGold
    ,case
        when imp.PlunderType = 'NO_PLUNDER' then '不提供任何产出'
        when imp.PlunderType = 'PLUNDER_NONE' then '不提供任何产出'
        when imp.PlunderType = 'PLUNDER_FAITH' then '后将获得信仰值'
        when imp.PlunderType = 'PLUNDER_GOLD' then '后将获得金币'
        when imp.PlunderType = 'PLUNDER_HEAL' then '后单位将获得50HP的治疗'
    end as PlunderType
    ,imp.PlunderAmount
    ,imp.Goody
    ,imp.TilesPerGoody
    ,imp.GoodyRange
    ,imp.Icon
    --,imp.TraitType
    ,cast(imp.Housing as float)/cast(imp.TilesRequired as float) as Housing1
    --,imp.Housing as Housing
    --,imp.TilesRequired
    ,case
        when imp.SameAdjacentValid = 0 then 1
        when imp.SameAdjacentValid = 1 then 0
    end as SameAdjacentInvalid
    ,imp.RequiresRiver
    ,imp.EnforceTerrain
    ,imp.BuildInLine
    ,imp.CanBuildOutsideTerritory
    ,imp.BuildOnFrontier
    ,imp.AirSlots
    ,imp.DefenseModifier
    ,imp.GrantFortification
    ,imp.MinimumAppeal
    ,imp.Coast
    ,case
        when imp.YieldFromAppeal is not null then cast(imp.YieldFromAppealPercent as text) || '%的'|| t6."Text"
        else ''
    end as YieldFromAppeal
    ,imp.WeaponSlots
    ,imp.ReligiousUnitHealRate
    ,case
        when imp.Appeal < 0 then cast(imp.Appeal as text)
        when imp.Appeal = 0 then ''
        when imp.Appeal > 0 then '+'||cast(imp.Appeal as text)
    end as Appeal
    ,imp.OnePerCity
--    ,imp.YieldFromAppealPercent
    ,imp.ValidAdjacentTerrainAmount
    ,case
        when imp."Domain" = 'DOMAIN_LAND' then '陆地'
        when imp."Domain" = 'DOMAIN_SEA' then '水域'
    end as "Domain"
    ,imp.AdjacentSeaResource
    ,imp.RequiresAdjacentBonusOrLuxury
    ,imp.MovementChange
    ,case
        when imp.Workable = 0 then 1
        else 0
    end as Unworkable
    ,imp.ImprovementOnRemove
    ,imp.GoodyNotify
    ,imp.NoAdjacentSpecialtyDistrict
    ,imp.RequiresAdjacentLuxury
    ,imp.AdjacentToLand
    ,case
        when imp.Removable = 0 then 1
        when imp.Removable = 1 then 0
    end as Unremovable
    ,imp.OnlyOpenBorders
    ,imp.Capturable
    ,coalesce(imp2.AllowImpassableMovement,0) as AllowImpassableMovement
    ,coalesce(imp2.BuildOnAdjacentPlot,0) as BuildOnAdjacentPlot
    ,coalesce(imp2.PreventsDrought,0) as PreventsDrought
    ,coalesce(imp2.DisasterResistant,0) as DisasterResistant
from
    Improvements imp
left join
    (select CivilizationType as "Type",TraitType from CivilizationTraits ct
        union all
    select LeaderType as "Type",TraitType from LeaderTraits lt
    ) trait
on
    imp.TraitType = trait.TraitType
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
    pre1."Type" = imp.PrereqTech
    or pre1."Type" = imp.PrereqCivic
left join
    Yields y
on
    y.YieldType = imp.YieldFromAppeal
left join
    Improvements_XP2 as imp2
on
    imp2.ImprovementType = imp.ImprovementType
left join
    Improvement_ValidBuildUnits as iv
on
    iv.ImprovementType =imp.ImprovementType
left join
    Units as u
on
    u.UnitType =iv.UnitType
left join
    zh_Hans_Text t1
on
    imp.Name = t1."Tag"
left join
    zh_Hans_Text t2
on
    t2."Tag" = l.Name
left join
    zh_Hans_Text t3
on
    t3."Tag" = c.Name
left join
    zh_Hans_Text t4
on
    t4."Tag" = pre1.Name
left join
    zh_Hans_Text t5
on
    t5."Tag" = imp.Description
left join
    zh_Hans_Text t6
on
    t6."Tag" = y.Name
left join
    zh_Hans_Text t7
on
    t7."Tag" = u.Name
;