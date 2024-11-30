drop table if exists BotData_Improvement_BonusYieldChanges;
CREATE TABLE if not exists BotData_Improvement_BonusYieldChanges(id int);
drop table if exists BotData_Improvement_BonusYieldChanges;
CREATE TABLE if not exists BotData_Improvement_BonusYieldChanges(
  ImprovementType TEXT,
  YieldType TEXT,
  BonusYieldChange INT,
  Prereq TEXT
);
insert into BotData_Improvement_BonusYieldChanges
select
    iby.ImprovementType
    ,t1."Text" as YieldType
    ,iby.BonusYieldChange 
    ,case
        when iby.PrereqTech is not null then '科技：'||t2."Text"
        when iby.PrereqCivic  is not null then '市政：'||t2."Text"
    end as Prereq
from
    Improvement_BonusYieldChanges as iby
left join
    Yields y 
on
    iby.YieldType = y.YieldType 
left join 
    Technologies t 
on
    t.TechnologyType = iby.PrereqTech 
left join 
    Civics c 
on
    c.CivicType = iby.PrereqCivic
left join 
    zh_Hans_Text t1
on
    t1.Tag = y.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = coalesce(t.Name ,c.Name);