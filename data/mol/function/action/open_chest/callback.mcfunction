## mol:action/open_chest/

# Guarantee an ownership ID before reading or writing any personal inventory.
execute unless score @s mol.id matches 1.. run function mol:action/join

tag @s add mol.temp
execute store result storage mol:data temp.owner int 1 run scoreboard players get @s mol.id
execute align xyz positioned ~.5 ~.5 ~.5 as @e[type=item_display, tag=mol.chest, tag=!mol.open, distance=...01, limit=1] run function mol:action/open_chest/mol_chest with storage mol:data temp
execute align xyz positioned ~.5 ~.5 ~.5 unless entity @e[type=item_display, tag=mol.chest, tag=!mol.open, distance=...01, limit=1] if score #debug mol.data matches 1 run tellraw @s [{"text":"[MyOwnLoot DEBUG] ","color":"gold"},{"text":"No tracked MyOwnLoot chest was found at this barrel.","color":"red"}]
tag @s remove mol.temp
