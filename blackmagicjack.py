# todo:
# - fix abilities not working if its the first card (havent seen it as second card yet but probably still not working)
# - ideas for abilities:
#   - increase limit of value (going past 33)
#   - negate abilities ability
#   - return to sender
#   - 50/50 chance of putting you at a better number or worse number (from bryson)
# - joker choosing ability OR random ability + 50/50 to lose card or gain card (2 in 100)
# - debug mode breaks if the card isnt in the deck
# - make it not like balatro

from datetime import datetime
import os
import random
import time

# open/create player save file
try:
    savefile = open("blackmagicjack save.txt","r")
except:
    savefile = open("blackmagicjack save.txt","w")
    savefile.write('0\n')
    savefile.close()
    savefile = open("blackmagicjack save.txt","r")
savecontent=[]
txt = '!'
while txt !='':
    txt = savefile.readline()
    savecontent=savecontent+[txt.strip('\n')]
savecontent.pop()

# clear terminal function from https://www.geeksforgeeks.org/clear-screen-python/
# this clears the screen for windows (uses cls) and linux/mac (uses clear)
def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
        
# exit function for when user types exit
def exitcheck(txt):
    if txt.upper() == "EXIT":
        savefile = open("blackmagicjack save.txt","w")
        for i in range(len(savecontent)):
            savefile.write(str(savecontent[i])+'\n')
        savefile.close()
        exit()

# menu
timelol=datetime.now().year*(10**17)+datetime.now().month*(10**15)+datetime.now().day*(10**13)+datetime.now().hour*(10**11)+datetime.now().minute*(10**9)+datetime.now().second*(10**7)+datetime.now().microsecond
random.seed(timelol)
# random messages
messagelist = ['hi','welcome','you got this!','lol','wowie','thanks for playing','version idk','woohoo!!','reference','made by me','insertinsidejokehere','insert joke here','congratulations','come to school tomorrow']
if datetime.now().month == 10 and datetime.now().day == 31:
    messagelist = messagelist + ['merry halloween','spooky','trick or treat!','happy halloween!!','stay safe tonight!!','https://media.tenor.com/fRCjDJ91UZcAAAAM/hallowen.gif']
elif datetime.now().month == 12 and datetime.now().day == 24:
    messagelist = messagelist + ['happy christmas eve','merry christmas eve!!','santa is watching you','https://media.tenor.com/fFYh_8ZVmzcAAAAM/christmas.gif']
elif datetime.now().month == 12 and datetime.now().day == 25:
    messagelist = messagelist + ['merry christmas!!','happy christmas eve','https://media.tenor.com/T117LNVFu_MAAAAM/merry-christmas.gif']
elif datetime.now().month == 12 and datetime.now().day == 31:
    messagelist = messagelist + ['merry new years eve!!','happy new years eve','https://tenor.com/view/happy-new-year-advance-2021-gif-12690358435444997226']
elif datetime.now().month == 1 and datetime.now().day == 1:
    messagelist = messagelist + ['merry new year!!','happy new years','https://tenor.com/view/happy-new-year-advance-2021-gif-12690358435444997226']
message = random.choice(messagelist)
# get highscore from save file, or show message saying save file was messed with
try:
    highscore = int(savecontent[0])
except:
    highscore = "you messing with the save file or something?"
# get settings from save file, or make settings and write settings to save file
settingname = ['show card value','show seed','debug','dealer turn wait','dealer waiting time','dealer 2 cards up']
try:
    settingtypes = []
    for i in range(6):
        try:
            settingtypes = settingtypes + [eval(savecontent[i+1])]
        except:
            settingtypes = settingtypes + [int(savecontent[i+1])]
except:
    settingtypes = [True,False,False,True,2,True]
    savefile = open("blackmagicjack save.txt","a+")
    for i in range(len(settingtypes)):
        savefile.write(str(settingtypes[i])+'\n')
        savecontent=savecontent+[settingtypes[i]]
    savefile = open("blackmagicjack save.txt","r")
# get unlocked abilities from save file (doesn't add abilities) and then set description
abilities = savecontent[len(settingtypes)+1:len(savecontent)]
abilitynames = ['spades king','diamonds queen','spades jack']
descriptions = ['give your hand (cards) to the other person','remove a random card from your hand (you don\'t get to pick)','shows next card']
shopitems = ['nothing yet lol']

def abilitiesfunc():
    abilitiesscreen = True
    while abilitiesscreen:
        clear_screen()
        print("black magic jack [{0}]\nunlocked abilities: {1}\nenter an ability name for a description, or enter back/home".format(message,abilities))
        plr = input("> ")
        if plr.upper() == "BACK" or plr.upper() == "HOME":
            abilitiesscreen = False
        for i in range(len(abilities)):
            if plr.lower() == abilities[i]:
                clear_screen()
                print("black magic jack [{0}]\nability: {1}\ndescription: {2}\npress enter to go back".format(message,abilities[i],descriptions[i]))
                input()

def settingsfunc():
    settings = True
    while settings:
        clear_screen()
        print("black magic jack [{0}]\nseed: {1}\nsettings: {2}\nenter a setting name for options, or enter back/home".format(message,timelol,settingname))
        # in settings, check if user types specific setting & option for setting or if user types "back/home"
        plr = input("> ")
        if plr.upper() == "BACK" or plr.upper() == "HOME":
            settings = False
            for i in range(len(settingtypes)):
                savecontent[i+1]=settingtypes[i]
            return
        # check what type of setting it is
        for i in range(len(settingname)):
            settingedited = ''
            if plr.upper() == settingname[i].upper():
                settingedited = plr.upper()
                if type(settingtypes[i]) == bool:
                    settype=['boolean\noptions: true or false',bool]
                elif type(settingtypes[i]) == int:
                    settype=['integer\noptions: positive number, numbers under 1 will count as 1\ndefault: 2',int]
                else:
                    settype='huh'
                # while loop so the user types right setting
                idklol = True
                while idklol:
                    try:
                        clear_screen()
                        print("black magic jack [{0}]\nsetting: {1}\ntype: {2}\nenter the correct option type for the setting".format(message,settingname[i],settype[0]))
                        plr = input("> ")
                        if settype[1] == bool:
                            settingtypes[i] = eval(plr.capitalize())
                            idklol = False
                        elif settype[1] == int:
                            if int(plr) < 1:
                                plr = 1
                            settingtypes[i] = int(plr)
                            idklol = False
                    except:
                        print('Fail!')
            # only activates if debug mode is enabled
            if settingedited == 'DEBUG' and plr.lower() == 'true':
                if settingtypes[2]:
                    clear_screen()
                    print("debug mode enabled!\n\ndebug mode lets you add a card to your hand after you hit.\nthis is mainly for testing purposes, but you can have fun!\nto use, type debug when in-game and then type a card name\n\npress enter to continue")
                    input()

# menu function + while not loop until user says start
def menu():
    start = False
    while not start:
        clear_screen()
        # display title and then random text in square brackets
        print("black magic jack [{0}]\nhighscore: {1}\nenter start, shop, settings, abilities, or exit.".format(message,highscore))
        # print(savecontent, settingtypes) # for debug
        # wait for input for start, shop, settings, abilities, or exit
        plr = input("> ")
        exitcheck(plr)

        # if user types "abilities" then show unlocked abilities (different pages)
        if plr.upper() == "ABILITIES":
            abilitiesfunc()

        # if user types "settings" show available settings
        if plr.upper() == "SETTINGS":
            settingsfunc()
                
        # if user types "shop" show available items/cards
        if plr.upper() == "SHOP":
            shop = True
            while shop:
                clear_screen()
                print("black magic jack [{0}]\nitems available: {1}\nenter an item name, or enter back/home".format(message,shopitems))
                plr = input("> ")
                if plr.upper() == "BACK" or plr.upper() == "HOME":
                    shop = False

        # if user types "start" start game by changing start value to true
        if plr.upper() == "START":
            start = True
            for i in range(len(settingtypes)):
                # print(savecontent,settingtypes)
                savecontent[i+1]=settingtypes[i]
            game()

# pause function + while not loop until user says resume
def pause():
    start = False
    while not start:
        if highscore>int(savecontent[0]):
            savecontent[0]=str(highscore)
        clear_screen()
        # display title and then random text in square brackets
        print("black magic jack [{0}]\nhighscore: {1}\nenter return, settings, abilities or exit.".format(message,highscore))
        # print(savecontent, settingtypes) # for debug
        # wait for input for return, settings or abilities
        plr = input("> ")
        # if user types "exit" then save the progress of the game and exit
        if plr.upper() == "EXIT":
            if highscore>int(savecontent[0]):
                savecontent[0]=str(highscore)
            clear_screen()
            print("black magic jack [{0}]\nthanks for playing!\nhighscore: {1}".format(message,int(savecontent[0])))
            exitcheck(plr)

        # if user types "abilities" then show unlocked abilities (different pages)
        if plr.upper() == "ABILITIES":
            abilitiesfunc()

        # if user types "settings" show available settings
        if plr.upper() == "SETTINGS":
            settingsfunc()

        # if user types "return" return to the game
        if plr.upper() == "RETURN":
            start = True
            for i in range(len(settingtypes)):
                # print(savecontent,settingtypes)
                savecontent[i+1]=settingtypes[i]
            return
        
# define variables for the abilities
limit = 33; lives = 3
plrhand = []; plrhandvalue = 0; plrhandval = []
dealhand = []; dealhandvalue = 0; dealhandval = []
plrhanddisplay = ''; dealhanddisplay = ''; ability = ''; usedcards = []    

# game
def game():
    highscore = 0
    plrfirst = True
    showvalue = settingtypes[0]
    showseed = settingtypes[1]
    debug = settingtypes[2]
    dealturnwait = settingtypes[3]
    dealwaittime = settingtypes[4]
    dealcardup = settingtypes[5]
    limit = 33
    lives = 3
    livessave = lives
    options=['hit, stand or pause','hit, stand, use or pause']
    # show game rules
    clear_screen()
    print('rules: closest to 33 wins, you have 3 lives\naces here work differently, it counts as only 1\nthere are card abilities you can encounter or buy in the shop\njoker card is a 1/100 chance, giving you a random ability but a 50/50 chance of losing or gaining a card\npress enter to continue')
    input()
    for i in range(3):
        print(abs(i-3))
        time.sleep(1)
    # function for random card from deck
    def randomcard():
        decknum = random.randint(0,len(deck)-1)
        card = deck[decknum]
        cardnum = deckvalue[decknum]
        deck.pop(decknum)
        deckvalue.pop(decknum)
        if random.randint(1,100) == 1:
            return card,cardnum,True
        else:
            return card,cardnum,False

    # player game function
    # while not loop until lives is 0
    while lives>0:
        deck = ['spades ace','spades 2','spades 3','spades 4','spades 5','spades 6','spades 7','spades 8','spades 9','spades 10','spades jack','spades queen','spades king','hearts ace','hearts 2','hearts 3','hearts 4','hearts 5','hearts 6','hearts 7','hearts 8','hearts 9','hearts 10','hearts jack','hearts queen','hearts king','diamonds ace','diamonds 2','diamonds 3','diamonds 4','diamonds 5','diamonds 6','diamonds 7','diamonds 8','diamonds 9','diamonds 10','diamonds jack','diamonds queen','diamonds king','clubs ace','clubs 2','clubs 3','clubs 4','clubs 5','clubs 6','clubs 7','clubs 8','clubs 9','clubs 10','clubs jack','clubs queen','clubs king']
        deckvalue = [1,2,3,4,5,6,7,8,9,10,10,10,10,1,2,3,4,5,6,7,8,9,10,10,10,10,1,2,3,4,5,6,7,8,9,10,10,10,10,1,2,3,4,5,6,7,8,9,10,10,10,10]
        if lives>livessave:
            highscore=highscore+1
            if highscore>int(savecontent[0]):
                savecontent[0]=str(highscore)
        livessave = lives
        plrturn = True; plrfirst = False; plrhand = []; plrhandvalue = 0; plrhandval = []
        dealfirst = True; dealhand = []; dealhandvalue = 0; dealhandval = []
        plrhanddisplay = ''; dealhanddisplay = ''; ability = ''; usedcards = []; nextcard = []; showcard = False
        turn = 0
        # gets first card dealer has
        while dealfirst:
            randcard = randomcard()
            # add card to dealer’s hands
            dealhanddisplay = ''
            dealhand=dealhand+[randcard[0]]
            dealhandvalue=dealhandvalue+randcard[1]
            dealhandval=dealhandval+[randcard[1]]
            for i in range(len(dealhand)):
                dealhanddisplay = dealhanddisplay + ', ' + dealhand[i]
            dealhanddisplay=dealhanddisplay.removeprefix(', ')
            # check if card is special
            option = options[0]
            for i in range(len(dealhand)):
                for a in range(len(abilities)):
                    if dealhand[i] == abilities[a]:
                        try:
                            if dealhand[i] != usedcards[len(usedcards)]:
                                ability = abilities[a]
                                option = options[1]
                            break
                        except:
                            if dealhand[i] != ability:
                                ability = abilities[a]
                                option = options[1]
                                if len(usedcards) == 0:
                                    ability = abilities[a]
                                    option = options[1]
            if randcard[2]:
                if option != options[1]:
                    option = options[1]
                    ability = abilities[random.randint(0,len(abilities)-1)]
                else:
                    option = options[1]
                    randcard[2] = False
            turn = turn + 1
            if dealcardup:
                if turn == 2:
                    dealfirst = False
                    plrfirst = True
                    turn = 0
            else:
                dealfirst = False
                plrfirst = True
                turn = 0
            
        while plrturn:
            # run random card function and show player the card
            if showcard:
                randcard = nextcard
                showcard = False
            else:
                randcard = randomcard()
            # add card to player’s hands
            plrhanddisplay = ''
            plrhand=plrhand+[randcard[0]]
            plrhandvalue=plrhandvalue+randcard[1]
            plrhandval=plrhandval+[randcard[1]]
            for i in range(len(plrhand)):
                plrhanddisplay = plrhanddisplay + ', ' + plrhand[i]
            plrhanddisplay=plrhanddisplay.removeprefix(', ')
            # check if player hand is over 33 (remove one life)
            if plrhandvalue>limit:
                lives=lives-1
                plrturn = False
                break
            # check if card is special
            option = options[0]
            for i in range(len(plrhand)):
                for a in range(len(abilities)):
                    if plrhand[i] == abilities[a]:
                        try:
                            if plrhand[i] != usedcards[len(usedcards)]:
                                ability = abilities[a]
                                option = options[1]
                            break
                        except:
                            if plrhand[i] != ability:
                                ability = abilities[a]
                                option = options[1]
                                if len(usedcards) == 0:
                                    ability = abilities[a]
                                    option = options[1]
            if randcard[2]:
                if option != options[1]:
                    option = options[1]
                    ability = abilities[random.randint(0,len(abilities)-1)]
                else:
                    option = options[1]
            # check to see if this is the player's first card, else show available options
            if not plrfirst:
                start = False
                while not start:
                    clear_screen()
                    # print(usedcards,ability,len(usedcards))
                    if debug:
                        print('debug mode enabled!')
                    if showseed:
                        print('seed:',timelol)
                    if showvalue:
                        print('lives: {0}\nyour cards: {1}\ncard value: {2}\ndealer\'s cards: {3}\n{4}'.format(lives,plrhanddisplay,plrhandvalue,dealhanddisplay,option))
                    else:
                        print('lives: {0}\nyour cards: {1}\ndealer\'s cards: {2}\n{3}'.format(lives,plrhanddisplay,dealhanddisplay,option))
                    if option == option[1]:
                        print('ability card:',ability)
                    plr = input("> ")
                    # if hit, run function for random card and show the player the card
                    if plr.lower() == 'hit':
                        start = True
                    # if stand, start dealer turn (run random card function and add to dealer hand)
                    if plr.lower() == 'stand':
                        plrturn = False
                        start = True
                    # if pause, pause game and wait for resume
                    if plr.lower() == 'pause':
                        pause()
                    # if debug, give card (debug purposes)
                    if plr.lower() == 'debug':
                        if debug:
                            plr = input()
                            decknum = deck.index(plr.lower())
                            card = deck[decknum]
                            cardnum = deckvalue[decknum]
                            deck.pop(decknum)
                            deckvalue.pop(decknum)
                            plrhand=plrhand+[card]
                            plrhandvalue=plrhandvalue+randcard[1]
                            plrhandval=plrhandval+[cardnum]
                            for i in range(len(plrhand)):
                                plrhanddisplay = plrhanddisplay + ', ' + plrhand[i]
                            plrhanddisplay=plrhanddisplay.removeprefix(', ')
                    # if use, use function of card
                    if option == options[1]:
                        if plr.lower() == 'use':
                            if ability == 'spades king':
                                # temp is here so dealer hand doesnt get itself
                                temp = plrhand; plrhand = dealhand; dealhand = temp
                                temp = plrhanddisplay; plrhanddisplay = dealhanddisplay; dealhanddisplay = temp
                                temp = plrhandvalue; plrhandvalue = dealhandvalue; dealhandvalue = temp
                                temp = plrhandval; plrhandval = dealhandval; dealhandval = temp
                            if ability == 'diamonds queen':
                                carddis = random.randint(0,len(plrhand)-1)
                                remove = plrhand[carddis]
                                plrhanddisplay=plrhanddisplay.strip(remove)
                                plrhand.pop(carddis)
                                plrhandvalue=plrhandvalue-plrhandval[carddis]
                                plrhandval.pop(carddis)
                            if ability == 'spades jack':
                                nextcard = randomcard()
                                showcard = True
                                clear_screen()
                                if showvalue:
                                    print('lives: {0}\nyour cards: {1}\ncard value: {2}\nnext card: {3}'.format(lives,plrhanddisplay,plrhandvalue,nextcard[0]))
                                else:
                                    print('lives: {0}\nyour cards: {1}\nnext card: {2}'.format(lives,plrhanddisplay,nextcard[0]))
                                print('hit, stand or pause')
                                plr = input()
                                if plr.lower() == 'stand':
                                    plrturn = False
                                    start = True
                                if plr.lower() == 'hit':
                                    start = True
                            usedcards = usedcards+[ability]
                            if randcard[2]:
                                if random.randint(1,100) % 2 == 0:
                                    chance = 'lose a card'
                                else:
                                    chance = 'gain a card'
                                clear_screen()
                                print("black magic jack [{0}]\njoker card! your ability: {1}\nchance has made you {2}".format(message,ability,chance))
                                if chance == 'lose a card':
                                    carddis = random.randint(0,len(dealhand)-1)
                                    remove = dealhand[carddis]
                                    dealhanddisplay=dealhanddisplay.strip(remove)
                                    dealhand.pop(carddis)
                                    dealhandvalue=dealhandvalue-dealhandval[carddis]
                                    dealhandval.pop(carddis)
                                else:
                                    plrhand=plrhand+[randcard[0]]
                                    plrhandvalue=plrhandvalue+randcard[1]
                                    plrhandval=plrhandval+[randcard[1]]
                                time.sleep(7)
                            start = True
            turn = turn+1
            if turn == 2:
                plrfirst = False
        dealturn = True
        while dealturn:
            if plrhandvalue>limit:
                dealturn = False
                plrturn = True
            # run random card function
            if showcard:
                randcard = nextcard
                showcard = False
            else:
                randcard = randomcard()
            # add card to dealer’s hands
            dealhanddisplay = ''
            if dealhandvalue<limit:
                dealhand=dealhand+[randcard[0]]
                dealhandvalue=dealhandvalue+randcard[1]
                dealhandval=dealhandval+[randcard[1]]
            for i in range(len(dealhand)):
                dealhanddisplay = dealhanddisplay + ', ' + dealhand[i]
            dealhanddisplay=dealhanddisplay.removeprefix(', ')
            # check if dealer hand is over 33 (add one life)
            if dealhandvalue>limit:
                lives=lives+1
                if plrhandvalue>limit:
                    lives=lives-1
                dealturn = False
                plrturn = True
            if dealhandvalue>=plrhandvalue and dealhandvalue<(limit+1):
                lives=lives-1
                dealturn = False
                plrturn = True
            clear_screen()
            if showseed:
                print('seed:',timelol)
            if showvalue:
                print('lives: {0}\nyour cards: {1}\ncard value: {2}\ndealer\'s cards: {3}\ndealer\'s value: {4}'.format(lives,plrhanddisplay,plrhandvalue,dealhanddisplay,dealhandvalue))
            else:
                print('lives: {0}\nyour cards: {1}\ndealer\'s cards: {2}'.format(lives,plrhanddisplay,dealhanddisplay))
            # check if card is special
            option = options[0]
            for i in range(len(dealhand)):
                for a in range(len(abilities)):
                    if dealhand[i] == abilities[a]:
                        try:
                            if dealhand[i] != usedcards[len(usedcards)]:
                                ability = abilities[a]
                                option = options[1]
                            break
                        except:
                            if dealhand[i] != ability:
                                ability = abilities[a]
                                option = options[1]
                                if len(usedcards) == 0:
                                    ability = abilities[a]
                                    option = options[1]
            if randcard[2]:
                if option != options[1]:
                    option = options[1]
                    ability = abilities[random.randint(0,len(abilities)-1)]
                else:
                    option = options[1]
            # if card is special, give chance to use
            temp = random.randint(1,3)
            if temp == 3:
                if ability == 'spades king':
                    # temp is here so player hand doesnt get itself
                    temp = dealhand; dealhand = plrhand; plrhand = temp
                    temp = dealhanddisplay; dealhanddisplay = dealhanddisplay; plrhanddisplay = temp
                    temp = dealhandvalue; dealhandvalue = dealhandvalue; plrhandvalue = temp
                    temp = dealhandval; dealhandval = dealhandval; plrhandval = temp
                if ability == 'diamonds queen':
                    carddis = random.randint(0,len(dealhand)-1)
                    remove = dealhand[carddis]
                    dealhanddisplay=dealhanddisplay.strip(remove)
                    dealhand.pop(carddis)
                    dealhandvalue=dealhandvalue-dealhandval[carddis]
                    dealhandval.pop(carddis)
                if ability == 'spades jack':
                    nextcard = randomcard()
                    showcard = True
                usedcards = usedcards+[ability]
                if randcard[2]:
                    if random.randint(1,100) % 2 == 0:
                        chance = 'lose a card'
                    else:
                        chance = 'gain a card'
                    if chance == 'lose a card':
                        carddis = random.randint(0,len(dealhand)-1)
                        remove = dealhand[carddis]
                        dealhanddisplay=dealhanddisplay.strip(remove)
                        dealhand.pop(carddis)
                        dealhandvalue=dealhandvalue-dealhandval[carddis]
                        dealhandval.pop(carddis)
                    else:
                        plrhand=plrhand+[randcard[0]]
                        plrhandvalue=plrhandvalue+randcard[1]
                        plrhandval=plrhandval+[randcard[1]]
                    time.sleep(3)
            
            if dealturnwait:
                time.sleep(dealwaittime)

        # when lives is 0, show death screen and wait for input for retry, menu, or exit (because i made it a function)
    if highscore>int(savecontent[0]):
        savecontent[0]=str(highscore)
    start = False
    while not start:
        clear_screen()
        print("black magic jack [{0}]\noof, you died! nice try. thanks for playing!\nscore: {1}\nhighscore: {2}\nenter retry, menu, or exit".format(message,highscore,int(savecontent[0])))
        plr = input("> ")
        exitcheck(plr)
        if plr.lower() == 'retry':
            start = True
            game()
        if plr.lower() == 'menu':
            menu()

# actually start the game lol
menu()