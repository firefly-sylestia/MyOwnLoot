## Toggle MyOwnLoot diagnostic messages.
scoreboard players add #debug mol.data 1
execute if score #debug mol.data matches 2.. run scoreboard players set #debug mol.data 0
execute if score #debug mol.data matches 1 run tellraw @s [{"text":"[MyOwnLoot] Debug mode: ","color":"dark_aqua"},{"text":"ON","color":"green"},{"text":". Open/close tracked chests to see ownership diagnostics.","color":"gray"}]
execute if score #debug mol.data matches 0 run tellraw @s [{"text":"[MyOwnLoot] Debug mode: ","color":"dark_aqua"},{"text":"OFF","color":"red"}]
