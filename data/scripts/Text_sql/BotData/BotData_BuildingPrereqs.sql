drop table if exists BotData_BuildingPrereqs;
create table if not exists BotData_BuildingPrereqs(id int);
drop table if exists BotData_BuildingPrereqs;
create table if not exists BotData_BuildingPrereqs(
    Building text
    ,PrereqBuilding text
);
insert into BotData_BuildingPrereqs
select 
    t1."Text" as Building
    ,t2."Text" as PrereqBuilding
from
    BuildingPrereqs bp
left join
    Buildings b1
on
    bp.Building = b1.BuildingType 
left join   
    Buildings b2
on
    bp.PrereqBuilding = b2.BuildingType 
left join   
    zh_Hans_Text t1
on
    t1.Tag = b1.Name    
left join   
    zh_Hans_Text t2
on
    t2.Tag = b2.Name    
