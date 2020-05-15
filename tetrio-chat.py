from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import socketio
import requests
import math
import os

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
	os._exit(0)
headers = {'Authorization': 'Bearer ' + authToken}
getUsername = (requests.get(url="https://tetr.io/api/users/me", headers=headers)).json()
if(getUsername['success']==False):
	print("Invalid token!")
	os._exit(0)
else:
	myUsername = getUsername['user']['username']
	myXP = getUsername['user']['xp']
	myLevel = math.floor(((myXP/500)**0.6) + (myXP/5000) + 1)
	
tetrio_data = (requests.get(url="https://tetr.io/api/server/environment")).json()
TETRIO_ENV = tetrio_data['signature']
connectMessage = {"token": authToken,"handling": handling,"signature": TETRIO_ENV}
sio = socketio.Client(reconnection=False)
inRoom = False
currentRoom = ""
rooms = {}

@sio.event
def connect():
	print("Connected to websocket")
	
@sio.event
def connect_error():
	print("Something went wrong...")

@sio.event
def disconnect():
	print("Disconnected!")
	menuframe.grid_remove()
	gameframe.grid_remove()
	roomframe.grid_remove()
	mainframe.grid()
	
	
@sio.on('kick')
def on_message(data):
	print(f"The server has disconnected you. Reason: {data['reason']}")
	menuframe.grid_remove()
	gameframe.grid_remove()
	roomframe.grid_remove()
	mainframe.grid()
	
@sio.on('authorize')
def on_message(data):
	if(data=={"success": True, "maintenance": False}):
		print("Login successful!")
		mainframe.grid_remove()
		menuframe.grid()
	else:
		print("Login failed!", data)

@sio.on('gmupdate')
def on_message(data):
	global inRoom
	if(inRoom==False):
		inRoom=True
		currentRoom = data['id']
		chatbox.configure(state="normal")
		chatbox.delete("1.0",END)
		chatbox.configure(state="disabled")
		menuframe.grid_remove()
		roomframe.grid_remove()
		gameframe.grid()
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
	
def join(roomID):
	global inRoom
	global currentRoom
	if(inRoom==False):
		print("Joining room with ID:",roomID)
		sio.emit('joinroom',roomID)
	else:
		print("You are already in a room!\n")

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
		if(players[i]['username']==myUsername):
			if(players[i]['bracket']=="player"):
				print("Moving to spectators")
				sio.emit("switchbracket","spectator")
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

def showrooms():
	getrooms()
	menuframe.grid_remove()
	roomframe.grid()

def getrooms():
	global rooms
	rooms = {}
	roomlistbox.delete(0,END)
	roomlist = (requests.get(url="https://tetr.io/api/rooms", headers=headers)).json()
	for key, value in roomlist.items():
		if(key=="rooms"):
			rooms = value
		for i in range(len(rooms)):
			roomlistbox.insert(END, rooms[i]['meta']['name'])

def joinbylist():
	try:
		for i in range(len(rooms)):
			if((roomlistbox.get(roomlistbox.curselection()))==rooms[i]['meta']['name']):
				join(rooms[i]['id'])
				break
	except tk.TclError:
		print("Nothing is selected!")
		
def goBack():
	roomframe.grid_remove()
	menuframe.grid()

def joinbyid():
	roomID = roomidentry.get("0.0",'1.end')
	roomidentry.delete("0.0",END)
	if(((len(roomID))!=9)and(roomID!="X-QP")):
		print("Invalid room ID!")
	else:
		join(roomID)
	
def enterkeyjoin(event):
	joinbyid()
	return 'break'
	
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

# Prepare room join screen (custom rooms)
roomframe = ttk.Frame(gui, padding="4 4 4 4")
roomframe.grid(column=0, row=0, sticky=(N, W, E, S))
roomframe.grid_remove()


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
roomButton = ttk.Button(menuframe, text="Join room", command=showrooms).grid(column=1, row=3, sticky="N", padx=450, pady=8)
disconnectButton = ttk.Button(menuframe, text="Disconnect", command=dc).grid(column=1, row=4, sticky="N", padx=450, pady=8)

# Room lobby
exitButton = ttk.Button(gameframe, text="Exit", command=leave).grid(column=1, row=1, sticky=(N,W), padx=16)
roomLabel = ttk.Label(gameframe, text="#?????????", style='roomIDstyle.TLabel')
roomLabel.grid(column=2, row=1,padx=240,sticky="E")
selfLabel = ttk.Label(gameframe, text=f"{myUsername}\n[{myLevel}, {getUsername['user']['league']['rank'].upper()}]", style='roomIDstyle.TLabel').grid(column=3,row=1,sticky="E")

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

# Room join screen
separator = ttk.Frame(roomframe,padding="4 4 4 4").grid(column=1, row=1, padx=215)
roomPrefix = ttk.Label(roomframe, text="#").grid(column=1, row=8, sticky="E")
joinlabel = ttk.Label(roomframe, text="Join Room", style='subtitle.TLabel').grid(column=2, row=1, sticky="N")
roomlistbox = tk.Listbox(roomframe, height=10)
roomlistbox.grid(column=2, row=2, sticky="N", pady=8)
roomVscroll = ttk.Scrollbar(roomframe, orient=VERTICAL, command=roomlistbox.yview)
roomVscroll.grid(column=3, row=2, sticky="N, S, W")
roomlistbox['yscrollcommand']=roomVscroll.set
roomHscroll = ttk.Scrollbar(roomframe, orient=HORIZONTAL, command=roomlistbox.xview)
roomHscroll.grid(column=2, row=3, sticky="W, E")
roomlistbox['xscrollcommand']=roomHscroll.set
joinButton = ttk.Button(roomframe, text="Join", command=joinbylist).grid(column=2, row=4, sticky="N", pady=8)
refreshButton = ttk.Button(roomframe, text="Refresh", command=getrooms).grid(column=2, row=5, sticky="N", pady=8)
backButton = ttk.Button(roomframe, text="Back to Menu", command=goBack).grid(column=2, row=6, sticky="N", pady=8)
joinidlabel = ttk.Label(roomframe, text="Join by ID:").grid(column=2, row=7, sticky="N", pady=16)
roomidentry = tk.Text(roomframe, width=10, height=1)
roomidentry.grid(column=2, row=8, sticky="N")
roomidentry.bind('<Return>',enterkeyjoin)
joinidbutton = ttk.Button(roomframe, text="Join", command=joinbyid).grid(column=2, row=9, sticky="N", pady=8)

gui.mainloop()