import tkinter as tk
from PIL import ImageTk,Image
import os
from io import BytesIO
import BJplayer 
import BJdealer

class BlackJackGUI:
	
	def __init__(self):
		# core attributes
		self.WINDOW_WIDTH = 720
		self.WINDOW_HEIGHT = 600
		self.root = None
		self.dealer = BJdealer.Dealer()
		self.player = BJplayer.Player(self.dealer)
		self.dealer.add_player(self.player)
		# button attributes that are referenced multiple times across 
		# different methods (is that bad practice?)
		self.bankroll_display = None
		self.current_bet_display = None
		self.please_add_lable = None
		self.insufficient_funds = None


	"""Main GUI method"""
	def create_GUI(self):
		# window setup
		root = tk.Tk()
		root.title("BlackJack!")
		root.iconbitmap("used files/icon.ico")
		WINDOW_WIDTH = root.geometry(str(self.WINDOW_WIDTH)+ "x" + 
			str(self.WINDOW_HEIGHT))
		self.root = root
		# Create start screen
		root.configure(background='black')
		title_letters = self.sized_image(
			"used files/generatedtext.png", 
			600, 
			100)
		# Title letters
		title_label = tk.Label(image=title_letters, bg="#EA1616")
		title_xcoor = (720/2) - (600/2)
		title_ycoor = (600/2) - 240
		title_label.place(x=title_xcoor, y=title_ycoor)
		# Play button
		play_btn = tk.Button(text="PLAY", width=10, 
			bg="#EA1616", font=("arial", "30"), 
			command=self.setup_new_game)
		play_btn_x = (self.WINDOW_WIDTH/2) - 115
		play_btn_y = (self.WINDOW_HEIGHT/2) - (15/2)
		play_btn.place(x=play_btn_x, y=play_btn_y)
		# key bindings
		self.root.bind("q", self.display_mouse_coordinates)
		# Assign images to cards 
		self.assign_img_to_cards(self.dealer.deck)
		# End of the TK loop
		root.mainloop()


	"""set up for after the player selects 'play' from the start menu."""
	def setup_new_game(self):
		# clear widgets
		widgets = self.root.winfo_children()
		for w in widgets:
			w.destroy()
		# add game screen
		background_image = self.sized_image("C:/Users/Noah Caldwell/"
			"Documents/SourceCode/TestGUI - Blackjack/TestGUI/"
			"used files/greenfelt.png", 720, 600)
		self.background_label = tk.Label(self.root, image=background_image)
		self.background_label.photo = background_image
		self.background_label.place(x=0, y=0)
		# Player buys bankroll
		# Instruction text
		self.instr_text = tk.Label(self.root, 
			text=f"How much do you want\n  to play with?", 
			font=("arial", "40"), bg="black", fg="white")
		self.instr_text.place(x=75, y=80)
		#  buy five hundred button
		self.five_hun_btn = tk.Button(self.root, text="500", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.buy_chips(500))
		self.five_hun_btn.place(x=100, y=300)
		# buy one hundred button
		self.one_hun_btn = tk.Button(self.root, text="100", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.buy_chips(100))
		self.one_hun_btn.place(x=230, y=300)
		# buy fifty button
		self.fifty_btn = tk.Button(self.root, text="50", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.buy_chips(50))
		self.fifty_btn.place(x=360, y=300)
		# buy twenty five button
		self.twenty_five_btn = tk.Button(self.root, text="25", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.buy_chips(25))
		self.twenty_five_btn.place(x=490, y=300)
		# display total bankroll as you buy chips
		self.bankroll_display = tk.Label(self.root, 
			text=f"bankroll\n{self.player.bankroll}", 
			font=("arial", "40"), bg="black", fg="white")
		self.bankroll_display.place(x=265, y=430)
		# place 'ready to play' button
		self.ready_btn = tk.Button(self.root, text="READY!", bg="white", 
			fg="black", font=("arial", "20", "bold"), 
			command=self.start_game)
		self.ready_btn.place(x=570, y=530)


	"""Updates Bankroll display label every .3 seconds"""
	def update_bankroll(self):
		if type(self.bankroll_display) != type(None):
			self.bankroll_display.config(
				text=f"bankroll\n{self.player.bankroll}")


	"""Updates current bet every .3 seconds"""
	def update_current_bet(self):
		if self.player.current_bet != 0:
			self.current_bet_display.config(
				text=f"current bet\n{self.player.current_bet}")


	"""Clear the unneeded widgets and move the bankroll display to 
	prepare for the game
	- TODO: implement a purely random way to shuffle the cards. BE CREATIVE. 
	base it one the weather in chattanooga or something."""
	def start_game(self):
		if self.player.bankroll > 0:
			# remove widgets
			self.destroy_all_except(self.please_add_lable,
				self.background_label, self.bankroll_display)
			if self.please_add_lable is not None:
				self.please_add_lable.destroy()
			# move bankroll display to left corner
			self.move_bankroll_display()
			self.choose_bet()
		else:
			self.please_add_lable = tk.Label(self.root, 
				text="Please choose an amount of money\n to play with.", 
				font=("arial", "8","bold"), bg="black", fg="red")
			self.please_add_lable.place(x=500, y=480)
			self.warning_displayed = True
		# Dealer shuffles cards at the begining of the game
		self.dealer.shuffle()


	"""Player picks bet amount"""
	def choose_bet(self):
		# Instruction text
		self.instr_text = tk.Label(self.root, 
			text=f"How much do you want\n  to bet?", 
			font=("arial", "40"), bg="black", fg="white")
		self.instr_text.place(x=75, y=80)
		# bet one hundred button
		self.one_hun_btn = tk.Button(self.root, text="100", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.place_bet(100))
		self.one_hun_btn.place(x=169, y=250)
		# bet fifty button
		self.fifty_btn = tk.Button(self.root, text="50", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.place_bet(50))
		self.fifty_btn.place(x=294, y=330)
		# bet twenty five button
		self.twenty_five_btn = tk.Button(self.root, text="25", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.place_bet(25))
		self.twenty_five_btn.place(x=419, y=410)
		# current bet display
		self.current_bet_display = tk.Label(self.root, 
			text=f"current bet\n{self.player.current_bet}", 
			font=("arial", "15"), bg="black", fg="white")
		self.current_bet_display.place(x=24, y=442)
		# ready to deal round button
		self.deal_round_btn = tk.Button(self.root, text="Deal!", fg='black',
			bg='white', font=("arial", "29", "bold"), 
			command=self.deal_round)
		self.deal_round_btn.place(x=585, y=515)


	def deal_round(self):
		# Clear widgets
		self.destroy_all_except(self.background_label, 
			self.current_bet_display, self.bankroll_display)
		# deal hand on the backend
		self.dealer.deal_round()
		print(self.dealer.hand)
		print(self.player.hand)
		# Deal first card to player
		p1card = tk.Label(self.root, image=self.player.hand[0].image)
		p1card.place(x=250, y=300)
		# Deal face down card to dealer
		d1card = tk.Label(self.root, image=self.dealer.hand[0].image)
		d1card.place(x=250, y=50)
		# Deal second card to player
		p2card = tk.Label(self.root, image=self.player.hand[1].image)
		p2card.place(x=380, y=300)
		# Deal second face-up card to dealer
		d2card = tk.Label(self.root, image=self.dealer.hand[1].image)
		d2card.place(x=380, y=50)


	"""Destorys all the widget on the screen except for the widgets listed
	in the parameters"""
	def destroy_all_except(self, *args):
		widgets = self.root.winfo_children()
		for w in widgets:
			if w not in args:
				w.destroy()		


	"""Move the bankroll_display label to the left corner while making
	it smaller incrementally of the course of a second or so."""
	def move_bankroll_display(self):
		# The 40 comes from the font size I declared when I first
		# instantiated the bankroll_display label.
		font_size = 40
		for i in range(0,40):
			# Move to left corner.
			self.root.update_idletasks()
			x_coor = self.bankroll_display.winfo_x()
			y_coor = self.bankroll_display.winfo_y()
			self.root.after(30, 
			self.bankroll_display.place_configure(x=x_coor-6, 
				y=y_coor+2))
			# Make font smaller. The 'if' statement is so it executes 
			# every other loop because i couldn't reduced the font by 
			# .5 because tkinter only accepts an integer for font sizes
			if i % 2 == 0:
				font_size -= 1
				self.bankroll_display.config(font=("arial", 
					str(font_size)))

	"""Moves button to specififed x,y coordinates. The buttons still currently
	leave a tral behind them.
	- TODO: be able to specify movement speed as a parameter"""
	def move_button(self, widget, x_coor, y_coor):
		# get the widget's current location
		self.root.update_idletasks()
		current_x = widget.winfo_x()
		current_y = widget.winfo_y()

		# move widget towards specified location until it is reached
		while current_x != x_coor or current_y != y_coor:
			# get widgets current location
			self.root.update_idletasks()
			current_x = widget.winfo_x()
			current_y = widget.winfo_y()
			# move on x axis in the right direction
			if current_x > x_coor:
				self.root.after(15, widget.place_configure(x=current_x-1))
			elif current_x < x_coor:
				self.root.after(15, widget.place_configure(x=current_x+1))
			# move on y axis in the right direction
			if current_y > y_coor:
				self.root.after(30, widget.place_configure(y=current_y-1))
			elif current_y < y_coor:
				self.root.after(30, widget.place_configure(y=current_y+1))
			# update the widget's current location
			current_x = widget.winfo_x()
			current_y = widget.winfo_y()

	"""Used when player buys their starting bankroll. Function called when
	user presses the 500, 100, 50, 25 buttons."""
	def buy_chips(self, amount):
		self.player.buy_chips(amount)
		self.update_bankroll()

	"""Used when the player bets on each round. Function called when the player 
	presses a button with a numerical amount of how much they want to bet."""
	def place_bet(self, amount):
		if amount <= self.player.bankroll:
			if type(self.insufficient_funds) is not type(None):
				self.insufficient_funds.destroy()
			self.player.place_bet(amount)
			self.update_bankroll()
			self.update_current_bet()
		else:
			self.insufficient_funds = tk.Label(self.root, text="insufficient"
				" funds!", bg='black', fg='red')
			self.insufficient_funds.place(x=140, y=540)




	"""Attach images to each card's image attribute."""
	def assign_img_to_cards(self, deck):
		directory = os.fsencode("used files/Cards")	
		deck_index = 0
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			img_path = "used files/Cards/" + filename
			img = self.sized_image(img_path, 107, 150)
			deck[deck_index].assign_image(img)
			deck_index += 1

	"""Print cursor coordinate to consol. Just a developer tool I can
	use instead of guessing coordinate when moving buttons and whatnot
	around."""
	def display_mouse_coordinates(self, event):
		x, y = event.x, event.y
		print('{}, {}'.format(x, y))


	"""Creates a Tkinter PhotoImage with dimensions specified in the 
	parameters using a image's file path. Can cause distorted images if 
	the dimesions are not proportional to the orginal 
	photo's dimesions. Accepts .png files."""
	def sized_image(self, img_path, w, h):
		img = Image.open(img_path)  # PIL solution
		img = img.resize((w, h), Image.ANTIALIAS) # (width, height)
		img = ImageTk.PhotoImage(image=img) # convert to PhotoImage
		return img


gui = BlackJackGUI()
gui.create_GUI()