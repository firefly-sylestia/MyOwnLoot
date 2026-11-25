## function mol:worldgen/search/

# find a chest in the chunk
item modify entity @s container.0 mol:worldgen/search/search_chest

# summon a marker at the chest
scoreboard players set #temp mol.chest_looted 1
function mol:worldgen/search/goto_chest with entity @s Item.components."minecraft:custom_data"

execute if score #temp mol.chest_looted matches 0 run function mol:worldgen/search/search_chest
