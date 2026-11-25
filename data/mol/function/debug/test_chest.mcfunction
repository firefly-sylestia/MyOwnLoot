## Spawn a fixed-loot MyOwnLoot test chest three blocks in front of the player.
## The test loot table deliberately gives identical contents to each player so isolation is easy to verify.
execute anchored eyes positioned ^ ^ ^3 align xyz run function mol:debug/test_chest/place
