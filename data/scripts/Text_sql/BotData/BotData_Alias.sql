drop table if exists BotData_Alias;
create table BotData_Alias as
select * from BotData_Alias_ArtificialWonders
union all
select * from BotData_Alias_Buildings
union all
select * from BotData_Alias_Civics_and_Technologies
union all
select * from BotData_Alias_Civilizations
union all
select * from BotData_Alias_Improvements
union all
select * from BotData_Alias_Leaders
union all
select * from BotData_Alias_NatureWonders
union all
select * from BotData_Alias_Units
;