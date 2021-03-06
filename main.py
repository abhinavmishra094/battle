from classes.game import Person, bcolors
from classes.magic import Spell
from classes.Inventory import Item
import random

fire = Spell("Fire", 25, 600, "black")
thunder = Spell("Thunder", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member ", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP ", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage ", 500)

player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5}, {"item": potion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 5}, {"item": grenade, "quantity": 5}]


player1 = Person("Valos", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Nick ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_spells, player_items)
enemy = Person("Magus", 11200, 701, 525, 25, [], [])

players = [player1, player2, player3]

i = 0
running = True

print(bcolors.FAIL+bcolors.BOLD+"An Enemy Attacks!"+bcolors.ENDC)

while running:
    print("======================")

    print("\n\n")
    for player in players:
        player.get_stats()
    print("\n")

    enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print("You attacked for ", dmg, " points of damage. Enemy Hp:  ", enemy.get_hp())
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    choose magic: "))-1
            if magic_choice == -1:
                continue
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage(magic_choice)
            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL+"\n not enough mp\n"+bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE+"\n"+spell.name+"heals for", str(magic_dmg)+" HP"+bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE+"\n"+spell.name+" deals ", str(magic_dmg), " points of damage, Enemy HP: ",
                      enemy.get_hp())
        elif index == 2:
            player.choose_items()
            item_choice = int(input("    Choose Items: "))-1

            if item_choice == -1:
                continue
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL+"\n"+"None left ....."+bcolors.ENDC)
                continue

            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN+"\n"+item.name+" heals for "+str(item.prop), "HP"+bcolors.ENDC)

            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN+"\n"+item.name+"fully restores HP/MP"+bcolors.ENDC)

            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL+"\n" + item.name+" deals ", str(item.prop), "points of daamage"+bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, 3)
    enemy_dmg = enemy.generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacked for ", enemy_dmg)

    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN+"You Win!"+bcolors.ENDC)
        running = False

    elif player1.get_hp() == 0:
        print(bcolors.FAIL+"Your enemy has defeated you"+bcolors.ENDC)
        running = False
