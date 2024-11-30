drop table if exists BotData_Unique_District_TradeRouteYields;
create table if not exists BotData_Unique_District_TradeRouteYields(id int);
drop table if exists BotData_Unique_District_TradeRouteYields;
create table if not exists BotData_Unique_District_TradeRouteYields(
    District text 
    ,ReplacedDistrict text 
);
insert into BotData_Unique_District_TradeRouteYields
select 
    t1."Text" as District
    ,t2."Text" as ReplacedDistrict
from 
    DistrictReplaces dr
left join
    Districts d1
on
    dr.CivUniqueDistrictType = d1.DistrictType  
left join 
    Districts d2
on
    dr.ReplacesDistrictType = d2.DistrictType 
left join 
    zh_Hans_Text t1
on  
    t1.Tag = d1.Name 
left join   
    zh_Hans_Text t2
on
    t2.Tag = d2.Name 
;