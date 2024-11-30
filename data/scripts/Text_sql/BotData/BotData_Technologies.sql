drop table if exists BotData_Technologies;
create table if not exists BotData_Technologies(id int);
drop table if exists BotData_Technologies;
create table if not exists BotData_Technologies(
    TechnologyType text    
    ,Technology text
    ,Cost int
    ,"Repeatable" int
    ,Description text
    ,EraType text
);
insert into BotData_Technologies
select 
    t.TechnologyType
    ,t1."Text" as Technology
    ,t.Cost
    ,t."Repeatable"
    ,t2."Text" as Description
    ,t3."Text" as EraType
from 
    Technologies t
left join
    zh_Hans_Text t1
on
    t1.Tag = t.Name 
left join 
    zh_Hans_Text t2
on
    t2.Tag = t.Description
left join
    Eras e 
on
    t.EraType = e.EraType 
left join   
    zh_Hans_Text t3
on
    t3.Tag = e.Name 