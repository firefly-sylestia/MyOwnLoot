## function #load:load

#load custom items
function mol:items

#scoreboard
scoreboard objectives add mol.id dummy
scoreboard objectives add mol.data dummy
scoreboard objectives add mol.chest_looted dummy

scoreboard players set #area_size mol.data 16

##settings
# 0 = no chest drop, 1 = drop mc chest, 2 = drop custom chest
scoreboard players set #chest_drop mol.data 0

#start chest detection loop
schedule function mol:schedule/ 2s

#broadcast only after the core MOL initialization function has run
tellraw @a [{"text":"[MyOwnLoot] ","color":"dark_aqua"},{"text":"Datapack loaded. Chest and barrel tracking initialized.","color":"green"}]

#write a visible confirmation to the dedicated server log and player chat
say [MyOwnLoot] LOAD OK - initialization function completed; chest detection scheduler was started.

#define
#define entity @a[tag=convention.debug]
#define score_holder #temp
#define storage mol:items
#define storage mol:data
