drop table if exists BotData_District_TradeRouteYields;
create table if not exists BotData_District_TradeRouteYields(id int);
drop table if exists BotData_District_TradeRouteYields;
create table if not exists BotData_District_TradeRouteYields(
    DistrictName text 
    ,Yield text 
    ,YieldChangeAsOrigin int
    ,YieldChangeAsDomesticDestination int
    ,YieldChangeAsInternationalDestination int
);
insert into BotData_District_TradeRouteYields
select 
    t1."Text" as DistrictName
    ,t2."Text" as Yield
    ,dt.YieldChangeAsOrigin
    ,dt.YieldChangeAsDomesticDestination
    ,dt.YieldChangeAsInternationalDestination
from 
    District_TradeRouteYields dt
left join
    Districts d
on
    dt.DistrictType = d.DistrictType 
left join 
    Yields y
on
    dt.YieldType = y.YieldType 
left join 
    zh_Hans_Text t1
on  
    t1.Tag = d.Name 
left join   
    zh_Hans_Text t2
on
    t2.Tag = y.Name 
;