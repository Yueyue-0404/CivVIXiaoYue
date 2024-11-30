drop table if exists BotData_CivilizationsAndLeaders_Traits;
create table if not exists BotData_CivilizationsAndLeaders_Traits(id int);
drop table if exists BotData_CivilizationsAndLeaders_Traits;
create table if not exists BotData_CivilizationsAndLeaders_Traits(
    "Type" text
    ,Owner text
    ,TraitName text
    ,TraitDescription text
);
insert into BotData_CivilizationsAndLeaders_Traits
select 
    "领袖" as "Type"
    ,t1."Text" as Owner
    ,t2."Text" as TraitName
    ,t3."Text" as TraitDescription
from
    LeaderTraits as lt
left join
    Leaders l
on
    lt.LeaderType = l.LeaderType 
left join   
    Traits t 
on
    lt.TraitType = t.TraitType 
left join 
    zh_Hans_Text t1
on
    l.Name = t1."Tag" 
left join 
    zh_Hans_Text t2
on
    t.Name  = t2.Tag 
left join 
    zh_Hans_Text t3
on
    t.Description  = t3.Tag
where 
    t1."Text" is not null
    and t3."Text" is not null
union all 
select 
    "文明" as "Type"
    ,t1."Text" as OwnerName
    ,t2."Text" as TraitName
    ,t3."Text" as TraitDescription
from
    CivilizationTraits as ct
left join
    Civilizations c
on
    ct.CivilizationType = c.CivilizationType 
left join   
    Traits t 
on
    ct.TraitType = t.TraitType 
left join 
    zh_Hans_Text t1
on
    c.Name = t1."Tag" 
left join 
    zh_Hans_Text t2
on
    t.Name  = t2.Tag 
left join 
    zh_Hans_Text t3
on
    t.Description  = t3.Tag
where 
    t1."Text" is not null
    and t3."Text" is not null