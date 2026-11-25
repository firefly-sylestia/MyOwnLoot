## function mol:action/open_chest/mol_chest

# The caller already set mol.chest_looted to 0 when this player has no
# saved inventory, or 1 when a saved inventory exists. Do not change that
# flag here: close_chest uses it to decide whether to create an owner entry.

# Generate this chest's original loot into the temporary barrel inventory.
$execute as @p[tag=mol.temp] run loot insert ~ ~ ~ loot $(LootTable)
