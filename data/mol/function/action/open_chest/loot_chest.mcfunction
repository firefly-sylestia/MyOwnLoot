## function mol:action/open_chest/mol_chest

# This function runs as the chest's item_display. Keep the per-open flag
# on that same entity because mol_chest.mcfunction and close_chest/chest
# read @s (the item_display), not the player.
scoreboard players add @s mol.chest_looted 1

# Generate loot for the player who opened this chest.
execute as @p[tag=mol.temp] run loot insert ~ ~ ~ loot $(LootTable)
