## function mol:worldgen/transform_chest

data modify entity @s item.components."minecraft:custom_data".mol.LootTable set from block ~ ~ ~ LootTable
data modify entity @s item.components."minecraft:custom_data".mol.Lock set from block ~ ~ ~ Lock

#setblock barrel
execute if block ~ ~ ~ chest[facing=east] run setblock ~ ~ ~ barrel[facing=east]
execute if block ~ ~ ~ chest[facing=north] run setblock ~ ~ ~ barrel[facing=north]
execute if block ~ ~ ~ chest[facing=south] run setblock ~ ~ ~ barrel[facing=south]
execute if block ~ ~ ~ chest[facing=west] run setblock ~ ~ ~ barrel[facing=west]

# Convert any remaining tagged chest (including modded/gilded variants)\n# into the barrel interaction block used by MyOwnLoot.\nexecute if block ~ ~ ~ #mol:chests run setblock ~ ~ ~ barrel[facing=north]\n\n#put data back
data modify block ~ ~ ~ Lock set from entity @s item.components."minecraft:custom_data".mol.Lock

#remove all item poping out
function mol:tick/remove_chest/kill_item
