drop table if exists BotData_CivilizationLeaders;
create table BotData_CivilizationLeaders as
select
    zht1."Text" as Civilization
    ,zht2."Text" as Leaders
from 
    CivilizationLeaders as t1
left join
    Leaders as l
on
    l.LeaderType = t1.LeaderType 
left join 
    Civilizations as c
on
    c.CivilizationType = t1.CivilizationType 
left join 
    zh_Hans_Text zht1
on
    zht1.Tag = c.Name 
left join 
    zh_Hans_Text zht2
on
    zht2.Tag = l.Name 
union all 
select '野蛮人','野蛮人'