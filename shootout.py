import sys
import time
import math
import random
#this is the main loop
def loop():
	global key
	global player
	global player2
	global gameover
	update(key)
	draw()
	if gameover :
		key=raw_input('\n(R)einiciar|(S)alir: ')
	else:
		key=raw_input('\n(A)puntar|(D)isparar|(C)ubrirse: ')
	player = resetActions(player)
	player2 = resetActions(player2)

def update(key):
	global player
	global player2
	global gameover
	if player['hp']<=0 or player2['hp']<=0:
		gameover = True
		if key == 's':
			exit()
		elif key == 'r':
			restart()
	else:
		if key == 'c':
			player['cover']=True
			player['currentaim']= player['baseaim']
		elif key == 'd':
			player['shoot']=True
		elif key == 'a':
			player['aim'] = True
			player=increaseAim(player)
		else:
			return #do nothing
		
		AI()
		if player['shoot']:
			player,player2 = shoot(player,player2)

def AI():
	global player
	global player2#AI
	rng = random.randint(0,100)
	if rng > 0 and rng< 15:
		player2['cover']=True
		player2['currentaim']=player2['baseaim']
	elif rng >15 and rng < 66:
		player2['shoot'] = True
		player2,player = shoot(player2,player)
	else:
		player2['aim'] = True
		player2 = increaseAim(player2)

def draw():
	print("\n" * 100) #clear screen
	global player
	global player2
	if gameover == False :
		cover = "="
		field = "_"*40
		p1Sprite = getPlayerSprite(player)
		p2Sprite = getPlayerSprite(player2)
		if player['shoot']:
			shootAnimation(0,field,p1Sprite,p2Sprite,cover)
		
		if player2['shoot']:
			shootAnimation(1,field,p1Sprite,p2Sprite,cover)
		
		if player['shoot'] or player2['shoot']:
			print("\n"*100)#clear screen

		print(str(player['hp'])+'HP'+field+str(player2['hp'])+'HP')
		print(str(player['currentaim'])+'%'+field+str(player2['currentaim'])+'%')
		sys.stdout.write(p1Sprite+cover+field+cover+p2Sprite)
		sys.stdout.flush()
	else:
		if player['hp'] <=0:
			print("You Lose")
		else:
			print("You Win")


def shootAnimation(direction,field,p1Sprite,p2Sprite,cover):
	bullet ='>'
	lastpos = 0
	if direction ==0  : #left to right
		for i,tile in enumerate(field):
			l = list(field)
			l[lastpos]='_'
			l[i] = bullet
			lastpos = i
			field = "".join(l)
			sys.stdout.write('\r'+p1Sprite+cover+field+cover+p2Sprite)
			sys.stdout.flush()
			time.sleep(0.03)
	else:
		for i in range(len(field)-1,-1,-1):
			l=list(field)
			l[lastpos]='_'
			l[i] = '<'
			lastpos = i
			field="".join(l)
			sys.stdout.write('\r'+p1Sprite+cover+field+cover+p2Sprite)
			sys.stdout.flush()
			time.sleep(0.03)

def resetActions(player):
	player['cover'] = False
	player['shoot'] = False
	player['aim'] = False
	return player

def getPlayerSprite(player):
	if player['cover']:
		return "n"
	else:
		return "T"

def shoot(player,target):
	if target['cover'] == False:
		damage = target['maxhp']*player['currentaim']/100
		target['hp'] -= math.ceil(damage)
		player['currentaim'] = player['baseaim']
		return player,target
	else:
		return player,target
	
def increaseAim(player):
	increase = random.randint(5, 15)
	player['currentaim'] += increase
	return player



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
key = ""
gameover = False
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


#Beggining of program
while(True):
	loop()
