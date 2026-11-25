## function mol:schedule/

# Ensure every online player has a persistent ownership ID.
# The join advancement handles new joins; this also repairs players who were
# already online or had the advancement completed before this datapack version.
execute unless score @s mol.id matches 1.. run function mol:action/join

# First-time welcome, plus a reliable returning-player welcome.
execute unless entity @s[tag=mol.joined] run tellraw @s [{"text":"[MyOwnLoot v1.2.1] ","color":"dark_aqua"},{"text":"Datapack is active. Your personal chest and barrel loot is enabled.","color":"green"}]
tag @s add mol.joined
execute if score @s mol.leave matches 1.. run tellraw @s [{"text":"[MyOwnLoot v1.2.1] ","color":"dark_aqua"},{"text":"Welcome back! Your personal chest and barrel loot is enabled.","color":"green"}]
scoreboard players reset @s mol.leave

# get the x and z position of the player
execute store result score #pos_x mol.data run data get entity @s Pos[0]
execute store result score #pos_z mol.data run data get entity @s Pos[2]

# get the x and z position +/- the area_size, this is done by dividing the position by the area_size, then multiplying the position by the area_size again, this can be done because scoreboard values are integers
scoreboard players operation #pos_x mol.data /= #area_size mol.data
scoreboard players operation #pos_x mol.data *= #area_size mol.data
scoreboard players operation #pos_z mol.data /= #area_size mol.data
scoreboard players operation #pos_z mol.data *= #area_size mol.data

# put the x and z position in the temp storage
data modify storage mol:data temp set value {}
execute store result storage mol:data temp.x int 1 run scoreboard players get #pos_x mol.data
execute store result storage mol:data temp.z int 1 run scoreboard players get #pos_z mol.data
execute store result storage mol:data temp.area_size int 1 run scoreboard players get #area_size mol.data

# get the 8 chunks around the player
function mol:schedule/worldgen/get_chunk_pos with storage mol:data temp
