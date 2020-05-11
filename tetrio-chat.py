from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import socketio
import requests
import os

#test_gmupdate = {'id': 'X-QP', 'type': 'system', 'auto': {'status': 'ingame', 'time': 30, 'maxtime': 30}, 'players': [{'_id': '5ea2a686d4cd05328d2f9190', 'username': 'iii', 'anon': False, 'xp': 126992, 'record': {'games': 25, 'wins': 13, 'streak': 4}, 'bracket': 'player', 'supporter': False}, {'_id': '5eadd7c86a0210711521d1f1', 'username': 'btmcsniper', 'anon': False, 'xp': 11881, 'record': {'games': 16, 'wins': 1, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5eab40990a3f8035f3649df5', 'username': 'benderprime', 'anon': False, 'xp': 95606, 'record': {'games': 13, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5ea8afe7774f3a6e56d16067', 'username': 'jujube', 'anon': False, 'xp': 84977, 'record': {'games': 10, 'wins': 1, 'streak': 0}, 'bracket': 'player', 'supporter': True}, {'_id': '5e9f869283e2a23fbb017765', 'username': 'connection', 'anon': False, 'xp': 149679, 'record': {'games': 3, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5ea43bfdaf3d4614a0d6947a', 'username': 'thechilledlemon', 'anon': False, 'xp': 95773, 'record': {'games': 1, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5e8b693133e7875e3ffe4118', 'username': 'darko', 'anon': False, 'xp': 264421, 'record': {'games': 0, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5eadda641f8158710c060538', 'username': 'pepocheer', 'anon': False, 'xp': 1235, 'record': {'games': 0, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5e471da5b77d7f0d4be53684', 'username': 'kimchi', 'anon': False, 'xp': 325735, 'record': {'games': 0, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5e9a95529652df7e441cb9d8', 'username': 'jaypal', 'anon': False, 'xp': 189505, 'record': {'games': 0, 'wins': 0, 'streak': 0}, 'bracket': 'player', 'supporter': False}, {'_id': '5e3f8acc2521796f629aa89b', 'username': 'gizmo4487', 'anon': False, 'xp': 692662, 'record': {'games': 0, 'wins': 0, 'streak': 0}, 'bracket': 'spectator', 'supporter': False}], 'game': {'state': 'ingame', 'options': {'version': 14, 'seed_random': False, 'seed': 187156, 'g': 0.05, 'stock': 0, 'countdown': True, 'countdown_count': 3, 'countdown_interval': 1000, 'precountdown': 5000, 'prestart': 1000, 'mission': 'MULTIPLEX TEST', 'mission_type': 'mission_versus', 'zoominto': 'slow', 'display_lines': False, 'display_attack': True, 'display_pieces': True, 'display_impending': True, 'display_kills': True, 'display_placement': True, 'hasgarbage': True, 'neverstopbgm': True, 'display_next': True, 'display_hold': True, 'gmargin': 0, 'gincrease': 0.0025, 'garbagemultiplier': 1, 'garbagemargin': 10800, 'garbageincrease': 0.008, 'garbagecap': 4, 'garbagecapincrease': 0.033, 'garbagecapmax': 10, 'bagtype': '7bag', 'spinbonuses': 'T-spins', 'kickset': 'SRS', 'nextcount': 5, 'allow_harddrop': True, 'display_shadow': True, 'locktime': 30, 'garbagespeed': 20, 'forfeit_time': 150, 'are': 0, 'lineclear_are': 0, 'infinitemovement': False, 'lockresets': 15, 'allow180': True, 'objective': {'type': 'none'}, 'room_handling': False, 'room_handling_arr': 2, 'room_handling_das': 10, 'room_handling_sdf': 6, 'manual_allowed': False, 'b2bchaining': True}, 'match': {'type': 'versus', 'ft': 1, 'gamemode': 'VERSUS', 'winningKey': 'STAY_ALIVE', 'keys': {'primary': 'TIME', 'primaryLabel': 'ALIVE', 'primaryLabelSingle': 'ALIVE', 'primaryIsAvg': False, 'secondary': 'stats.garbage.sent', 'secondaryLabel': 'LINES SENT', 'secondaryLabelSingle': 'LINE SENT', 'secondaryIsAvg': False, 'tertiary': 'stats.garbage.received', 'tertiaryLabel': 'LINES RECEIVED', 'tertiaryLabelSingle': 'LINE RECEIVED', 'tertiaryIsAvg': False}, 'extra': {}}}, 'owner': None, 'meta': {'name': 'QUICK PLAY', 'userlimit': 0, 'allowAnonymous': True, 'bgm': 'RANDOM', 'match': {'type': 'versus', 'ft': 1}}}
handling = {"arr":"0","das":"5.4","sdf":"21"}
authToken = ""
try:
	tokenFile = open("token.txt","r")
	authToken = tokenFile.read()
	tokenFile.close()
except FileNotFoundError:
	print("token.txt is missing! Creating it now.")
	newTokenFile = open("token.txt","w")
	newTokenFile.write("Replace this line with your TETR.IO token")
	newTokenFile.close()
	print("Add your TETR.IO token to the newly created file and run the program again.")
	exit(0)
headers = {'Authorization': 'Bearer ' + authToken}
getUsername = (requests.get(url="https://tetr.io/api/users/me", headers=headers)).json()
if(getUsername['success']==False):
	print("Invalid token!")
	quit()
else:
	myUsername = getUsername['user']['username']
	
tetrio_data = (requests.get(url="https://tetr.io/api/server/environment")).json()
TETRIO_ENV = tetrio_data['signature']
connectMessage = {"token": authToken,"handling": handling,"signature": TETRIO_ENV}
sio = socketio.Client()
inRoom = False
currentRoom = ""

@sio.event
def connect():
	print("Connected to websocket")
	
@sio.event
def on_message(sio, message):
	print(message)
	
@sio.event
def connect_error():
	print("Something went wrong...")

@sio.event
def disconnect():
	print("Disconnected!")
	menuframe.grid_remove()
	gameframe.grid_remove()
	mainframe.grid()
	
	
@sio.on('kick')
def on_message(data):
	print("The server has disconnected you.",data)
	menuframe.grid_remove()
	gameframe.grid_remove()
	mainframe.grid()
	
@sio.on('authorize')
def on_message(data):
	if(data=={"success": True, "maintenance": False}):
		print("Login successful!")
		mainframe.grid_remove()
		menuframe.grid()
		#commands()
	else:
		print("Login failed!", data)

@sio.on('gmupdate')
def on_message(data):
	global inRoom
	if(inRoom==False):
		inRoom=True
		sio.emit("switchbracket","spectator")	# Enter spectator mode
		chatbox.configure(state="normal")
		chatbox.delete("1.0",END)
		chatbox.configure(state="disabled")
		menuframe.grid_remove()
		gameframe.grid()
	#print(data)
	update(data)

@sio.on('chat')
def on_message(data):
	chatbox.configure(state="normal")
	chatbox.insert(INSERT,"{0}: {1}\n\n".format(data['user']['username'],data['content']))
	chatbox.see("end")
	chatbox.configure(state="disabled")
	
def dc():
		print("Disconnecting")
		sio.disconnect()
		menuframe.grid_remove()
		mainframe.grid()
		
def spec():
	global inRoom
	if(inRoom==True):
		print("Spectating!\n")
		sio.emit('switchbracket','spectator')
	else:
		print("You are not in a room!\n")
	#commands()
	
def join(roomID):
	global inRoom
	global currentRoom
	if(inRoom==False):
		print("Joining room with ID:",roomID)
		sio.emit('joinroom',roomID)
	else:
		print("You are already in a room!\n")
	#commands()

def leave():
	global inRoom
	global currentRoom
	if(inRoom==True):
		print("Leaving room\n")
		sio.emit('leaveroom',currentRoom)
		currentRoom = ""
		inRoom=False
		gameframe.grid_remove()
		menuframe.grid()
		roomLabel.configure(text="#?????????")
		roomnameLabel.configure(text="??????????")
		playerlistbox.delete(0,END)
		playerlabel.configure(text="Players (0)")
	else:
		print("You are not in a room!\n")
	#commands()

def chat(msg):
	global inRoom
	if(inRoom==True):
		if((msg=="\n")or(msg=="")):
			print("Hey! You can't send an empty message! Try again.")
		else:
			print(f"Sending message: {msg}")
			sio.emit('chat',msg)
		chatinput.delete("0.0",END)
	else:
		print("You are not in a room!")
	#commands()

def socketConnect():
	print("Connecting...")
	sio.connect('https://tetr.io/socket.io')
	print('Socket ID:', sio.sid)
	sio.emit('authorize', connectMessage)

def qp():
	join("X-QP")
	
def update(message):
	playerlistbox.delete(0, END)
	players = {}
	for key, value in message.items():
		if(key=="players"):
			players = value
		if(key=="id"):
			roomLabel.configure(text=f"#{value}")
			currentRoom=value
			roomnameLabel.configure(text=(message['meta']['name']))
	playerlabel.configure(text=f"Players ({len(players)})")
	for i in range(len(players)):
		playerlistbox.insert(END, players[i]['username'])
		
def enterkeychat(event):
	msg = chatinput.get("0.0",'1.end')
	chat(msg)
	return 'break'
	
def sendchat():
	msg = chatinput.get("0.0",'1.end')
	chat(msg)

def quit():
	os._exit(0)

	
versionString = f"TETR.IO version: {tetrio_data['signature']['version']}"
userString = f"Username: {myUsername}"
gui = Tk()
gui.geometry("1024x768")
gui.title("TETR.IO Chat")
gui.iconbitmap('resources/icon.ico')

# Prepare main menu
mainframe = ttk.Frame(gui, padding="4 4 4 4")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
gui.columnconfigure(0, weight=1)
gui.rowconfigure(0, weight=1)

# Prepare multiplayer menu
menuframe = ttk.Frame(gui, padding="4 4 4 4")
menuframe.grid(column=0, row=0, sticky=(N, W, E, S))
menuframe.grid_remove()	# Hide multiplayer menu until connected

# Prepare game lobby screen (when joining a room)
gameframe = ttk.Frame(gui, padding="4 4 4 4")
gameframe.grid(column=0, row=0, sticky=(N, W, E, S))
gameframe.grid_remove()	# Hide game lobby screen until a room is joined


logo = Image.open("resources/logo.png")
tkimage = ImageTk.PhotoImage(logo)

s = ttk.Style()
s.configure('subtitle.TLabel', font=('Helvetica', 24))
s.configure('roomIDstyle.TLabel', font=('Helvetica', 18))

# Main menu
tk.Label(mainframe, image=tkimage).grid(column=1, row=1, sticky="N", padx=360)
ttk.Label(mainframe, text="Chat", style='subtitle.TLabel').grid(column=1, row=2, sticky="N", padx=400)
ttk.Label(mainframe, text=versionString).grid(column=1, row=3, sticky="N", padx=410)
ttk.Label(mainframe, text=userString).grid(column=1, row=4, sticky="N", padx=400)
connectButton = ttk.Button(mainframe, text="Connect", command=socketConnect).grid(column=1, row=5, sticky="N", padx=410, pady=50)
quitButton = ttk.Button(mainframe, text="Quit", command=quit).grid(column=1, row=6, sticky="N", padx=410)

# Multiplayer menu
ttk.Label(menuframe, text="Main Menu", style='subtitle.TLabel').grid(column=1, row=1, sticky="N", padx=430, pady=32)
quickPlayButton = ttk.Button(menuframe, text="Quick Play", command=qp).grid(column=1, row=2, sticky="N", padx=450, pady=8)
disconnectButton = ttk.Button(menuframe, text="Disconnect", command=dc).grid(column=1, row=3, sticky="N", padx=450, pady=8)

# Room lobby
exitButton = ttk.Button(gameframe, text="Exit", command=leave).grid(column=1, row=1, sticky=(N,W), padx=16)
roomLabel = ttk.Label(gameframe, text="#?????????", style='roomIDstyle.TLabel')
roomLabel.grid(column=2, row=1,padx=240,sticky="E")
selfLabel = ttk.Label(gameframe, text=myUsername, style='roomIDstyle.TLabel').grid(column=3,row=1,sticky="E")

playerlabel = ttk.Label(gameframe, text="Players (0)", style='roomIDstyle.TLabel')
playerlabel.grid(column=1,row=2,sticky="W",padx=8,pady=16)
roomnameLabel = ttk.Label(gameframe, text="??????????",style='roomIDstyle.TLabel')
roomnameLabel.grid(column=2,row=2,sticky="N")
chatheader = ttk.Label(gameframe, text="Chat", style='roomIDstyle.TLabel').grid(column=3,row=2,sticky="W",pady=16)

playerlistbox = tk.Listbox(gameframe, height=30)
playerlistbox.grid(column=1, row=3,sticky="N")
chatbox = tk.Text(gameframe, width=30, height=35)
chatbox.grid(column=3, row=3, sticky="W", pady=5)
chatbox.configure(state="disabled")
chatscroll = ttk.Scrollbar(gameframe, orient=VERTICAL, command=chatbox.yview)
chatscroll.grid(column=4, row=3, sticky="N, S")
chatbox['yscrollcommand']=chatscroll.set
chatinput = tk.Text(gameframe, width=30, height=1)
chatinput.grid(column=3, row=4, sticky="W")
chatinput.bind('<Return>', enterkeychat)
chatSendButton = ttk.Button(gameframe, text="Send", command=sendchat)
chatSendButton.grid(column=3, row=5, sticky="N")

#debugPlayerButton = ttk.Button(gameframe, text="DEBUG: Perform gmupdate", command=update).grid(column=2, row=3, sticky="N")
#debugChatButton = ttk.Button(gameframe, text="DEBUG: New message", command=newchat).grid(column=2, row=4, sticky="N")

gui.mainloop()