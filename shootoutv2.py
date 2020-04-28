import curses
import os
import time
import random
key = ""
gameover = False
xout = False

ai = {
    'name':'Borntodie Martinez',
    'default':{'shoot':True,'cover':False},
    'rare':{'shoot':False,'cover':True}
    }
    
def main(win):
    delay = 60
    win.nodelay(True)
    global xout
    while not xout:
        input_read(win)
        update()
        draw(win)
        global player
        global player2
        resetActions(player)
        resetActions(player2)
        time.sleep(0.03)         

def input_read(win):
    global key
    try:                 
        key = win.getkey()         
        if key == '\x1b':
           global xout
           xout = True           
    except Exception as e:
        pass#key = ""

def update():
    global key
    global player
    global player2
    global xout
    global gameover
    if player['hp']<=0 or player2['hp']<=0:
        gameover = True
        if key == 'x':
            xout=True
            return
        elif key == 'r':
            restart()
    else:
        if key == 'KEY_DOWN':
            player['cover']=True
        elif key == ' ' and not player['bullet']['moving']:
            player = shoot(player)
        
        AI(player2)
        if player2["shoot"] and not player2['bullet']['moving']:
            player2 = shoot(player2)

        if player['bullet']['moving']:
            move_bullet(player['bullet'],player2,1)
        if player2['bullet']['moving']:
            move_bullet(player2['bullet'],player,-1)

def AI(player):
    global ai
    rng = random.randint(0,100)
    if rng > 0 and rng < 20:
        player['shoot'] = ai['rare']['shoot']
        player['cover'] = ai['rare']['cover']
    else:
        player['shoot'] = ai['default']['shoot']
        player['cover'] = ai['default']['cover']
            

def check_hit(player):
    if not player['cover']:
        player['hp'] -= 100

def move_bullet(bullet,rival_player,speed):
    bullet['pos'] += speed
    if bullet['pos'] >= 40 or bullet['pos']<=0:
   #TODO check if hit
        check_hit(rival_player)
        bullet['pos'] = bullet['ogpos']
        bullet['moving'] = False

def shoot(player):
    player['bullet']['moving'] = True
    return player

def draw(win):
    global key
    global player
    global player2
    sky = "☁   ☁  ☁   ☁    ☁    ☁    ☁    ☁  ☁   ☁   ☁  ☁\n\n                    ☀"
    #Clear previous frame and draw next
    win.clear()                
    """win.addstr("Detected key:")
    win.addstr(str(key))"""
    if gameover == False :
        cover = "□"
        field = "_"*40
        instructions = " [↓] - Cover\t\t[space] - Shoot"
        p1Sprite = getPlayerSprite(player)
        p2Sprite = getPlayerSprite(player2)

        win.addstr(sky+"\n\n\n")
        if player['bullet']['moving']:
            field = field[:player['bullet']['pos']] + '▸' + field[player['bullet']['pos'] + 1:]
        if player2['bullet']['moving']:
            field = field[:player2['bullet']['pos']] + '◂' + field[player2['bullet']['pos'] + 1:]
        #win.addstr(str(player['hp'])+'HP'+field+str(player2['hp'])+'HP\n')
        #print(str(player['currentaim'])+'%'+field+str(player2['currentaim'])+'%')
        if not player["cover"]:
            win.addstr('●')
        else:
            win.addstr('  ')
        win.addstr(' '*42)
        if not player2["cover"]:
            win.addstr('●')
        else:
            win.addstr(' ')
        win.addstr("\n"+p1Sprite+cover+field+cover+p2Sprite)
        win.addstr("\n"+instructions)
    else:
        win.addstr(sky+"\n\n\n")
        if player['hp'] <=0:
            win.addstr("\t\tYou Lose")
        else:
            win.addstr("\t\tYou Win")
        
        win.addstr("\n\nPress [r] to [r]estart or [x] to e[x]it")


def getPlayerSprite(player):
    if player['cover']:
        return "●n"
    else:
        return "T"

def resetActions(player):
    player['cover'] = False
    player['shoot'] = False
    return player

player = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
    'bullet':{'pos':0,'moving':False,'ogpos':0}
    }

player2 = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
    'bullet':{'pos':40,'moving':False,'ogpos':40}
    }

def restart():
    global gameover
    global player
    global player2
    global key
    key=""
    gameover=False
    player = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
    'bullet':{'pos':0,'moving':False,'ogpos':0}
    }
    player2 = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
    'bullet':{'pos':40,'moving':False,'ogpos':40}
    }

curses.wrapper(main)