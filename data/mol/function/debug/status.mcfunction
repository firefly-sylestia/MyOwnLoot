## Show MyOwnLoot debug configuration.
execute if score #debug mol.data matches 1 run tellraw @s [{"text":"[MyOwnLoot] Debug mode is ON.","color":"green"}]
execute unless score #debug mol.data matches 1 run tellraw @s [{"text":"[MyOwnLoot] Debug mode is OFF.","color":"gray"}]
