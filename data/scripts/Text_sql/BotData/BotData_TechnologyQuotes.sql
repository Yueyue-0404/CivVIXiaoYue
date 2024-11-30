drop table if exists BotData_TechnologyQuotes;
create table if not exists BotData_TechnologyQuotes(id int);
drop table if exists BotData_TechnologyQuotes;
create table if not exists BotData_TechnologyQuotes(
Technology text 
,Quote text
);
insert into BotData_TechnologyQuotes
select 
    zht1."Text" as Technology
    ,zht2."Text" as Quote
from
    TechnologyQuotes tq
left join
    Technologies t 
on
    tq.TechnologyType = t.TechnologyType 
left join 
    zh_Hans_Text zht1
on
    zht1.Tag = t.Name 
left join   
    zh_Hans_Text zht2
on
    zht2.Tag = tq.Quote 