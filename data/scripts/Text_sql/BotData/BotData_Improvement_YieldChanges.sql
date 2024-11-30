drop table if exists BotData_Improvement_YieldChanges;
CREATE TABLE if not exists BotData_Improvement_YieldChanges(id int);
drop table if exists BotData_Improvement_YieldChanges;
CREATE TABLE BotData_Improvement_YieldChanges(
  ImprovementType TEXT,
  YieldType TEXT,
  YieldChange INT
);
insert into BotData_Improvement_YieldChanges
select
    iyc.ImprovementType
    ,zht."Text" as YieldType
    ,iyc.YieldChange
from
    Improvement_YieldChanges iyc
left join
    Yields y
on
    y.YieldType = iyc.YieldType
left join
    zh_Hans_Text zht
on
    zht.Tag = y.Name
    ;