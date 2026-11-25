# MyOwnLoot

This datapack is inspired by the [Lootr](https://modrinth.com/mod/lootr) mod.

MyOwnLoot gives each player a separate inventory for supported loot chests. A chest is locked while one player has it open. When the chest closes, that player's contents are saved and the shared block inventory is cleared. The next player receives their own generated loot; returning players get their previously saved contents.

## Minecraft 1.21.1

The current block adapter supports vanilla chests, trapped chests, and vanilla barrels used by the datapack. Modded storage is intentionally not included in the container tags yet. A modded chest needs a safe adapter before it can be transformed; treating arbitrary modded inventories as vanilla barrels can break or remove their storage.

## Multiplayer isolation test

Run these commands as an operator:

- `/function mol:debug/toggle` — toggle ownership diagnostics on/off.
- `/function mol:debug/status` — show whether diagnostics are enabled.
- `/function mol:debug/test_chest` — spawn a fixed-loot test chest about three blocks in front of you, provided the target block is air.

With two players:

1. Enable debug mode.
2. Spawn one test chest.
3. Player A opens it, takes one diamond, then closes it.
4. Player B opens the same chest. B should still receive 5 diamonds, 12 gold ingots, and 3 emeralds.
5. B takes one item and closes it. Player A reopens it and should see A's own remaining items, not B's inventory.
6. Reopen as each player again. Each player's remaining inventory should persist.

Expected debug messages:
- First visit by a player: `No saved inventory for you yet; generated your personal loot copy.`
- On close: `Saved your personal inventory for this chest.`
- Returning visit: `Restored your saved personal inventory for this chest.`

If the test chest does not appear, stand where the block three blocks ahead is air and run the spawn command again. The test loot is intentionally fixed so both players' inventories can be compared reliably.

## Important

Do not use an ordinary manually placed chest for this test. The datapack tracks loot chests that have been discovered and transformed by its world-generation system, plus the dedicated test chest created by the command above. A regular player-placed chest is not automatically converted into a personal-loot chest.
