## Place only into air; never overwrite a block.
scoreboard players set #test_created mol.data 0
execute store success score #test_created mol.data if block ~ ~ ~ air run setblock ~ ~ ~ chest[facing=north]{LootTable:"mol:debug/multi_player",LootTableSeed:12345L}
execute if score #test_created mol.data matches 1 positioned ~.5 ~.5 ~.5 summon item_display run function mol:worldgen/transform_chest
execute if score #test_created mol.data matches 1 run tellraw @s [{"text":"[MyOwnLoot TEST] ","color":"gold"},{"text":"Test chest spawned. Ask another player to open the same chest after you close it.","color":"green"}]
execute if score #test_created mol.data matches 0 run tellraw @s [{"text":"[MyOwnLoot TEST] ","color":"gold"},{"text":"No chest spawned: the target block is not air. Move to a clear spot and try again.","color":"red"}]
