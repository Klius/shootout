import curses
import os
import time
key = ""
gameover = False
xout = False 
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
        time.sleep(0.03)         

def input_read(win):
    global key
    try:                 
        key = win.getkey()         
        if key == '\x1b':
           global xout
           xout = True           
    except Exception as e:
        key = ""

def update():
    global key
    global player
    global player2
    if player['hp']<=0 or player2['hp']<=0:
        gameover = True
        if key == 'x':
            xout(True)
        elif key == 'r':
            restart()
    else:
        if key == 'KEY_DOWN':
            player['cover']=True
        elif key == ' ' and not player['bullet']['moving']:
            player = shoot(player)
    if player['bullet']['moving']:
        player['bullet']['pos'] += 1
        if player['bullet']['pos'] >= 40:
            #TODO check if hit
            player['bullet']['pos'] = 0
            player['bullet']['moving'] = False

def shoot(player):
    player['bullet']['moving'] = True
    player['bullet']['pos'] = 0
    return player

def draw(win):
    global key
    global player
    global player2
    #Clear previous frame and draw next
    win.clear()                
    """win.addstr("Detected key:")
    win.addstr(str(key))"""
    if gameover == False :
        cover = "="
        field = "_"*40
        p1Sprite = getPlayerSprite(player)
        p2Sprite = getPlayerSprite(player2)
        if player['bullet']['moving']:
            field = field[:player['bullet']['pos']] + '-' + field[player['bullet']['pos'] + 1:]
    
        win.addstr(str(player['hp'])+'HP'+field+str(player2['hp'])+'HP\n')
        #print(str(player['currentaim'])+'%'+field+str(player2['currentaim'])+'%')
        win.addstr(p1Sprite+cover+field+cover+p2Sprite)
    else:
        if player['hp'] <=0:
            win.addstr("You Lose")
        else:
            win.addstr("You Win")


def getPlayerSprite(player):
    if player['cover']:
        return "n"
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
    'bullet':{'pos':0,'moving':False}
    }

player2 = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
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
    }
    player2 = {
    'cover':False,
    'shoot':False,
    'aim':False,
    'baseaim':10,
    'currentaim':10,
    'hp':100,
    'maxhp':100,
    }
curses.wrapper(main)