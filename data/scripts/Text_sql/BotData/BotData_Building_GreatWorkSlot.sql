drop table if exists BotData_Building_GreatWorkSlot;
create table if not exists BotData_Building_GreatWorkSlot(id int);
drop table if exists BotData_Building_GreatWorkSlot;
create table if not exists BotData_Building_GreatWorkSlot(
    BuildingName text
    ,GreatWorkSlotType text
    ,NumSlots int
);
insert into BotData_Building_GreatWorkSlot
select 
    zht."Text" as BuildingName
    ,case 
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_PALACE' then '任意'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_RELIC' then '遗物'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_WRITING' then '著作'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_ART' then '艺术品'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_ARTIFACT' then '文物'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_CATHEDRAL' then '宗教画'
       when bg.GreatWorkSlotType = 'GREATWORKSLOT_MUSIC' then '音乐'
    end as GreatWorkSlotType
    ,bg.NumSlots
from 
    Building_GreatWorks as bg
left join
    Buildings b
on
    bg.BuildingType = b.BuildingType 
left join 
    zh_Hans_Text zht 
on
    zht.Tag = b.Name 