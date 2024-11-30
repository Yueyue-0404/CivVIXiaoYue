drop table if exists BotData_Technology_Unlocks;
create table if not exists BotData_Technology_Unlocks(id int);
drop table if exists BotData_Technology_Unlocks;
CREATE TABLE if not exists BotData_Technology_Unlocks(
  Name TEXT,
  Technology TEXT,
  obj_type text
);
insert into BotData_Technology_Unlocks 
select
    zht."Text" as Name
    ,tg.Technology as Technology
    ,tg.obj_type
from
    (
    select 
        b.Name
        ,bdt.Technology
        ,'建筑' as obj_type
    from 
        Buildings b
    left join
        BotData_Technologies bdt 
    on
        b.PrereqTech = bdt.TechnologyType
    union all
    select 
        d.Name
        ,bdt.Technology
        ,'区域' as obj_type
    from 
        Districts d
    left join
        BotData_Technologies bdt 
    on
        d.PrereqTech = bdt.TechnologyType
    union all
    select 
        i.Name
        ,bdt.Technology
        ,'改良设施' as obj_type
    from 
        Improvements i
    left join
        BotData_Technologies bdt 
    on
        i.PrereqTech = bdt.TechnologyType
    union all
    select 
        u.Name
        ,bdt.Technology
        ,'单位' as obj_type
    from 
        Units u
    left join
        BotData_Technologies bdt 
    on
        u.PrereqTech = bdt.TechnologyType
    ) as tg
left join
    zh_Hans_Text zht 
on
    zht.Tag = tg.Name
where 
    tg.Technology is not null