##function mol:close_chest/close_chest

# Remember which player owns this open inventory for the optional debug confirmation.
execute if score #debug mol.data matches 1 run scoreboard players operation #mol_debug_owner mol.data = @s mol.id

# Store this player's inventory in the chest entity.
$execute if score @s mol.chest_looted matches 0 run data modify entity @s item.components."minecraft:custom_data".mol.Items append value {Owner:$(owner)}
$data modify entity @s item.components."minecraft:custom_data".mol.Items[{Owner:$(owner)}].Items set from block ~ ~ ~ Items

# put the data back
data modify block ~ ~ ~ Items set value []
data modify block ~ ~ ~ Lock set from entity @s item.components."minecraft:custom_data".mol.Lock

# Confirm the save to the owning player when debug mode is enabled.
execute if score #debug mol.data matches 1 as @a if score @s mol.id = #mol_debug_owner mol.data run tellraw @s [{"text":"[MyOwnLoot DEBUG] ","color":"gold"},{"text":"Saved your personal inventory for this chest.","color":"green"}]

#remove the information that it's open
tag @s remove mol.open
scoreboard players reset @s mol.chest_looted
scoreboard players reset @s mol.id
