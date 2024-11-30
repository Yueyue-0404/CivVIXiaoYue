drop table if exists BotData_Alias;
create table BotData_Alias as
select * from BotData_Alias_Leaders
union all
select * from BotData_Alias_Civilizations;