drop table if exists BotData_TechnologyPrereqs;
create table if not exists BotData_TechnologyPrereqs(id int);
drop table if exists BotData_TechnologyPrereqs;
create table if not exists BotData_TechnologyPrereqs(
    Technology text
    ,PrereqTech text
);
insert into BotData_TechnologyPrereqs
select 
    zht1."Text" as Technology
    ,zht2."Text" as PrereqTech
from
    TechnologyPrereqs tp
left join
    Technologies t1
on
    tp.Technology = t1.TechnologyType 
left join 
    Technologies t2
on
    tp.PrereqTech = t2.TechnologyType 
left join
    zh_Hans_Text zht1
on
    t1.Name = zht1.Tag 
left join
    zh_Hans_Text zht2
on
    t2.Name = zht2.Tag 
