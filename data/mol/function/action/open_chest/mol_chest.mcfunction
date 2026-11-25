## mol:action/open_chest/callback

# Find this player's saved inventory. If none exists, generate a personal copy.
$execute store success score @s mol.chest_looted if data entity @s item.components."minecraft:custom_data".mol.Items[{Owner:$(owner)}]
execute if score @s mol.chest_looted matches 0 run function mol:action/open_chest/loot_chest with entity @s item.components."minecraft:custom_data".mol
$execute if score @s mol.chest_looted matches 1 run data modify block ~ ~ ~ Items set from entity @s item.components."minecraft:custom_data".mol.Items[{Owner:$(owner)}].Items

# Optional owner-level diagnostics (toggle with /function mol:debug/toggle).
execute if score #debug mol.data matches 1 if score @s mol.chest_looted matches 1 run tellraw @p[tag=mol.temp] [{"text":"[MyOwnLoot DEBUG] ","color":"gold"},{"text":"Restored your saved personal inventory for this chest.","color":"green"}]
execute if score #debug mol.data matches 1 if score @s mol.chest_looted matches 0 run tellraw @p[tag=mol.temp] [{"text":"[MyOwnLoot DEBUG] ","color":"gold"},{"text":"No saved inventory for you yet; generated your personal loot copy.","color":"yellow"}]

# lock the chest with an unobtainable password (the § symbol can't be typed)
data modify entity @s item.components."minecraft:custom_data".mol.Lock set from block ~ ~ ~ Lock
data modify block ~ ~ ~ Lock set value "§mol:chest"

# make the chest easier to track
tag @s add mol.open
scoreboard players operation @s mol.id = @p[tag=mol.temp] mol.id
$data modify entity @s item.components."minecraft:custom_data".mol.owner set value $(owner)
