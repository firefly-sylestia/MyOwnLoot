## function mol:smithed_block/block/mol_chest
## function mol:worldgen/chest_location

data merge entity @s {item:{id:"minecraft:furnace",count:1,components:{"minecraft:custom_model_data":9449900,"minecraft:custom_data":{mol:{Items:[],Lock:""}}}},brightness:{block:15,sky:15},transformation:{scale:[0.5f,0.5f,0.5f]},Tags:["mol.chest","itemio.container.nope","itemio.comtainer"]}
function #itemio:calls/container/init

function mol:worldgen/become_barrel

#rotate
execute if block ~ ~ ~ barrel[facing=east] run data modify entity @s Rotation[0] set value 270f
execute if block ~ ~ ~ barrel[facing=north] run data modify entity @s Rotation[0] set value 180f
execute if block ~ ~ ~ barrel[facing=south] run data modify entity @s Rotation[0] set value 0f
execute if block ~ ~ ~ barrel[facing=west] run data modify entity @s Rotation[0] set value 90f
