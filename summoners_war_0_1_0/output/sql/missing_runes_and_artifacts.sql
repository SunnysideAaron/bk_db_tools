select sfmn.full_name
, sxul.class as stars
, CASE
	WHEN sxul.rune_slot_1_id = 0 THEN "Missing"
  END AS Rune1
, CASE
	WHEN sxul.rune_slot_2_id = 0 THEN "Missing"
  END AS Rune2
, CASE
	WHEN sxul.rune_slot_3_id = 0 THEN "Missing"
  END AS Rune3
, CASE
	WHEN sxul.rune_slot_4_id = 0 THEN "Missing"
  END AS Rune4
, CASE
	WHEN sxul.rune_slot_5_id = 0 THEN "Missing"
  END AS Rune5
, CASE
	WHEN sxul.rune_slot_6_id = 0 THEN "Missing"
  END AS Rune6  
, CASE
	WHEN sxul.class = 6 AND sxul.artifact_slot_1_rid = 0 THEN "Missing"
  END AS Artifact1
, CASE
	WHEN sxul.class = 6 AND sxul.artifact_slot_2_rid = 0 THEN "Missing"
  END AS Artifact2  
from swex_unit_list as sxul
left join swarfarm_monster_names sfmn on sxul.unit_master_id = sfmn.com2us_id
where sxul.class >= 5
and (sxul.rune_slot_1_id = 0
  or sxul.rune_slot_2_id = 0
  or sxul.rune_slot_3_id = 0
  or sxul.rune_slot_4_id = 0
  or sxul.rune_slot_5_id = 0
  or sxul.rune_slot_6_id = 0
  or (
	sxul.class = 6
	and (sxul.artifact_slot_1_rid = 0
	  or sxul.artifact_slot_2_rid = 0)
  )
)
order by sxul.class desc
, sfmn.full_name;