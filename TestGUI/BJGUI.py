import tkinter as tk
from PIL import ImageTk,Image
import os
import time
from io import BytesIO
import BJplayer 
import BJdealer

class BlackJackGUI:
	
	def __init__(self):
		# constants
		self.WINDOW_WIDTH = 720
		self.WINDOW_HEIGHT = 600
		self.PLAYER_CARDS_Y_COOR = 270
		self.DEALER_CARDS_Y_COOR = 50
		# core attributes
		self.root = None
		self.dealer = BJdealer.Dealer()
		self.player = BJplayer.Player(self.dealer)
		self.dealer.add_player(self.player)
		self.face_down_card = None
		self.player_card_widgets = []
		self.dealer_card_widgets = []
		# button attributes that are referenced multiple times across 
		# different methods (is that bad practice?)
		self.bankroll_display = None
		self.current_bet_display = None
		self.hand_total_display = None
		self.please_add_lable = None
		self.insufficient_funds = None
		self.hit_btn = None
		self.stand_btn = None
		# Developer tools
		self.is_shuffling_deck = False



	def create_GUI(self):
		"""Main GUI method
		"""
		# window setup
		root = tk.Tk()
		root.title("BlackJack!")
		root.iconbitmap("used files/icon.ico")
		root.geometry(str(self.WINDOW_WIDTH)+ "x" + 
			str(self.WINDOW_HEIGHT))
		self.root = root
		# Create start screen
		root.configure(background='black')
		title_letters = self.sized_image(
			"used files/generatedtext.png", 
			600, 
			100)
		self.root.update_idletasks()
		# Loading display
		loading_display = tk.Label(self.root, text="Loading...",
		bg='black', fg='white', font=("arial", '30'))
		loading_display.place(x=275, y=270)
		self.root.update_idletasks()
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
		# Destroy loading display
		loading_display.destroy()
		# End of the TK loop
		root.mainloop()


	def setup_new_game(self):
		"""set up for after the player selects 'play' from the start menu."""
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


	def update_bankroll(self):
		"""Updates Bankroll display number
		"""
		if type(self.bankroll_display) != type(None):
			self.bankroll_display.config(
				text=f"bankroll\n{self.player.bankroll}")


	def update_current_bet(self):
		"""Updates current bet.
		"""
		self.current_bet_display.config(
			text=f"current bet\n{self.player.current_bet}")


	def start_game(self):
		"""Clear the unneeded widgets and move the bankroll display to the side 
		to prepare for the game.
		
		- TODO: implement a purely random way to shuffle the cards. BE CREATIVE. 
		base it one the weather in chattanooga or something.
		"""		
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
		if self.is_shuffling_deck:
			self.dealer.shuffle()


	def choose_bet(self):
		"""Sets up the interface where the user can choose
		how much money to play with.
		"""		
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
			command=self.deal_first_round)
		self.deal_round_btn.place(x=585, y=515)


	def deal_first_round(self):
		"""Deal the first round of cards. Subsequent rounds will be invoked using
		the deal_round method.
		
		- TODO: Get the fucking buttons to destroy/exit the screen before the cards 
		are dealt out.
		"""		
		# Clear widgets
		self.destroy_all_except(
			self.background_label, 
			self.current_bet_display, 
			self.bankroll_display)
		self.root.update_idletasks()
		# Create a display for players hand total
		self.hand_total_display = tk.Label(self.root, text=f"Hand Total\n {self.player.total}",
			font=("arial", 18), bg='black', fg='white')
		self.hand_total_display.place(x=575, y=530)
		# if player still has money to play with, deal cards for the round
		if self.player.bankroll > 0:
			# deal hand on the backend
			self.dealer.deal_round()
			print("dealer's hand " + str(self.dealer.hand))
			print("Player's hand " + str(self.player.hand))
			# Deal first card to player
			p1card = tk.Label(self.root, image=self.player.hand[0].image)
			p1card.place(x=250, y=self.PLAYER_CARDS_Y_COOR)
			self.player_card_widgets.append(p1card)
			self.root.after(1000, self.root.update_idletasks())
			# Deal face down card to dealer
			d1card = tk.Label(self.root, 
				image=self.dealer.hand[0].face_down_image)
			d1card.place(x=250, y=self.DEALER_CARDS_Y_COOR)
			self.dealer_card_widgets.append(d1card)
			self.face_down_card = d1card
			self.root.after(1000, self.root.update_idletasks())
			# Deal second card to player
			p2card = tk.Label(self.root, image=self.player.hand[1].image)
			p2card.place(x=380, y=self.PLAYER_CARDS_Y_COOR)
			self.player_card_widgets.append(p2card)
			self.root.after(1000, self.root.update_idletasks())
			# Deal second face-up card to dealer
			d2card = tk.Label(self.root, image=self.dealer.hand[1].image)
			d2card.place(x=380, y=self.DEALER_CARDS_Y_COOR)
			self.dealer_card_widgets.append(d2card)
			self.root.after(1000, self.root.update_idletasks())
			if self.player.get_hand_total == 21:
				self.win_round()
			else:
				# place player option buttons
				self.hit_btn = tk.Button(self.root, text="HIT", fg="black", 
					bg="white", font=("arial", "19", "bold"), padx=22,
					borderwidth=5, command=self.player_hit)
				self.hit_btn.place(x=253, y=490)
				self.stand_btn = tk.Button(self.root, text="STAND", fg="black", 
					bg="white", font=("arial", "19", "bold"),
					borderwidth=5, command=self.player_stand)
				self.stand_btn.place(x=385, y=490)
				self.update_player_status()
		# if player does not have money to play with, end the game
		else:
			self.end_game()


	
	def destroy_all_except(self, *args):
		"""Destorys all the widget on the screen except for the widgets listed
		in the parameters
		"""		
		[widget.destroy() for widget in self.root.winfo_children() if widget not in args]


	
	def move_bankroll_display(self):
		"""Move the bankroll_display label to the left corner while making
		it smaller incrementally of the course of a second or so.
		"""	
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


	
	def move_button(self, widget, x_coor, y_coor):
		"""Moves button to specififed x,y coordinates. The buttons still currently
		leave a tral behind them.

		- TODO: be able to specify movement speed as a parameter
		
		Arguments:
			- widget {tk widget} -- The widget that will be moved
			- x_coor {integer} -- the x coordinate of where the widget will be
			after this function is called
			- y_coor {integer} -- the y coordinate of where the widget will be 
			after this function is called
		"""		
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


	
	def buy_chips(self, amount):
		"""Used when player buys their starting bankroll. Function called when
		user presses the 500, 100, 50, 25 buttons.
		
		Arguments:
			amount {integer} -- the amount of money the player selects to buy
		"""		
		self.player.buy_chips(amount)
		self.update_bankroll()


	def place_bet(self, amount):
		"""Used when the player bets on each round. Function called when the player 
		presses a button with a numerical amount of how much they want to bet.
				
		Arguments:
			amount {integer} -- the amount of money the player wants to bet
		"""		
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


	def player_hit(self):
		"""Player chooses to get another card.

		- BUG: extra cards and wrong cards are sometimes dealt. fix it! maybe just rewrite 
		the whole thing, you fucktwit.
		"""		
		# Not 100% sure this update is necessary
		self.player.update_total()
		# If it is still the player's turn, let him hit for another card
		if self.player.status == "playing":
			# Player is dealt another card on the backend
			self.player.hit()
			# Deal the player cards in the GUI
			movement_amount = 30 - len(self.player.hand)
			last_card = None
			second_to_last_card = None
			# Move the cards that are already displayed to make room for 
			# the new card.
			for card in self.player_card_widgets:
				x_coor = card.winfo_x()
				# if the card widget is the player's firstcard, move to the
				# left of it's current position
				if card is self.player_card_widgets[0]:
					card.place_configure(x=x_coor-movement_amount)
				# move all the other cards to the right of the previous
				# card's position
				else:
					card.place_configure(x=last_card.winfo_x() + 
						movement_amount)
				# assign card to variable if it is the second to last card in
				# the player's hans
				if card is self.player_card_widgets[-2]:
					second_to_last_card = card
				# assign previous card to reference in the next loop	
				last_card = card
				self.root.update_idletasks()
			# calculate the placement of the new card
			spacing_between_cards = (last_card.winfo_x() - 
				second_to_last_card.winfo_x())
			new_card_x_coor = last_card.winfo_x() + spacing_between_cards
			# create the new card's widget
			new_card_img = self.player.hand[-1].image
			new_card_widget = tk.Label(self.root, image=new_card_img)
			new_card_widget.place(x=new_card_x_coor, 
				y=self.PLAYER_CARDS_Y_COOR)
			self.player_card_widgets.append(new_card_widget)
			self.hand_total_display.configure(text=f"Hand Total\n {self.player.total}")
			self.update_player_status()


	"""Player elects to stand"""
	def player_stand(self):
		self.player.stand()
		self.update_player_status()


	"""React to the player's current status in the game."""
	def update_player_status(self):
		# Player can continue to play out his turn
		if self.player.status == "playing":
			# This is an intentional 'pass', the player should be able
			# to continue to have the ability to click on options in the
			# case they are still 'playing'.
			pass
		# End of player's turn, commence dealer's actions, tally up
		# winner
		elif self.player.status == "stand" or self.player.status == "21":
			# dealer follow's his turn's protocal
			self.prompt_dealers_turn()
			# wait 2s, allocate pot to calculated winner
			self.root.after(2000, self.calculate_winner())
		elif self.player.status == "busted":
			self.player_bust()
			self.root.after(4000, self.calculate_winner())
			print("Fix the deal_round method to continue")
			# self.deal_round()
		else:
			print("player is experiencing a status that is not yet handled")


	def prompt_dealers_turn(self):
		self.flip_face_down_card()
		while self.dealer.get_hand_total() < 17:
			# Deal the player cards in the GUI
			movement_amount = 30 - len(self.dealer.hand)
			last_card = None
			second_to_last_card = None
			# Move the cards that are already displayed to make room for 
			# the new card.
			for card in self.dealer_card_widgets:
				x_coor = card.winfo_x()
				# if the card widget is the player's firstcard, move to the
				# left of it's current position
				if card is self.dealer_card_widgets[0]:
					card.place_configure(x=x_coor-movement_amount)
				# move all the other cards to the right of the previous
				# card's position
				else:
					card.place_configure(x=last_card.winfo_x() + 
						movement_amount)
				# assign card to variable if it is the second to last card in
				# the player's hans
				if card is self.dealer_card_widgets[-2]:
					second_to_last_card = card
				# assign previous card to reference in the next loop	
				last_card = card
				self.root.update_idletasks()
			# Dealer hits on the backend
			self.dealer.hit()
			# calculate the placement of the new card
			spacing_between_cards = (last_card.winfo_x() - 
				second_to_last_card.winfo_x())
			new_card_x_coor = last_card.winfo_x() + spacing_between_cards
			# create the new card's widget
			new_card_img = self.dealer.hand[-1].image
			new_card_widget = tk.Label(self.root, image=new_card_img)
			new_card_widget.place(x=new_card_x_coor, 
				y=self.DEALER_CARDS_Y_COOR)
			self.dealer_card_widgets.append(new_card_widget)
			self.dealer.update_hand_total()
			self.root.update_idletasks()
			

	"""See who wins at the end of the round"""
	def calculate_winner(self):
		# Player loses if he/she busted
		if self.player.status == "busted":
			print("Player busted, dealer collects pot")
			self.player.current_bet = 0
			self.update_current_bet()
		# dealer busted, player winds
		elif self.dealer.status == "busted":
			print("dealer buster, player collects pot")
			self.player.bankroll += self.player.current_bet * 2
			self.player.current_bet = 0
			self.update_current_bet()
			self.update_bankroll()
		# Compare hands if player is still in the round and his turn is
		# over 
		elif (self.player.status == "stand" 
			or self.player.status == "21"):
			# Player has bigger hand, player wins
			if self.player.get_hand_total() > self.dealer.get_hand_total():
				print("player has a bigger hand, player collects pot")
				# remove 'hit' and 'stand' button, show Player wins' display
				self.hit_btn.destroy()
				self.stand_btn.destroy()
				player_wins_display = tk.Label(self.root, text="Player wins",
					font=("arial", "30")) 
				player_wins_display.place(x=240, y=480)
				#player_wins_display.place(x=)
				# allocate pot to player
				self.player.bankroll += self.player.current_bet * 2
				self.player.current_bet = 0
				self.update_current_bet()
				self.update_bankroll()
			# Player has smaller hand, player loses
			elif self.player.get_hand_total() < self.dealer.get_hand_total():
				print("player has smaller hand, dealer collects pot")
				self.player.current_bet = 0
				self.update_current_bet()
			# The player and the dealer have the same count
			else:
				print("Tie! New round!")
				# Display Tie banner to user
				tie_banner = tk.Label(self.root, text="Tie!", font=("arial", "200"),
				fg='yellow', bg='black')
				tie_banner.place(x=200, y=250)
				# give bet back to player
				self.player.bankroll += self.player.current_bet
				self.player.current_bet = 0
				self.update_bankroll()
				self.update_current_bet()


	"""Give dealer a card."""
	def dealer_hit(self):
		print("implement the dealer hitting")


	"""player loses round"""
	def player_bust(self):
		if self.hit_btn != None and self.stand_btn != None:
			self.hit_btn.destroy()
			self.stand_btn.destroy()
			busted_display = tk.Label(self.root, text="BUSTED!", 
				font=("arial", "50"))
			busted_display.place(x=240, y=480)
			self.root.update_idletasks()
		else:
			raise NameError("The hit-btn or the stand-btn have not been"
				+ "assigned")

	"""Creates a new round after the first round has been played, the 
	first round is set up using deal_first_round()."""
	def deal_round(self):
		# Clear widgets
		self.destroy_all_except(self.background_label, 
			self.current_bet_display, self.bankroll_display)
		# if player still has money to play with
		if self.player.bankroll > 0:
			# deal hand on the backend
			time.sleep(2)
			self.root.update_idletasks()
			self.dealer.deal_round()
			print("dealer's hand " + str(self.dealer.hand))
			print("Player's hand " + str(self.player.hand))
			# Deal first card to player
			self.root.update_idletasks()
			p1card = tk.Label(self.root, image=self.player.hand[0].image)
			p1card.place(x=250, y=self.PLAYER_CARDS_Y_COOR)
			self.player_card_widgets.append(p1card)
			self.root.update_idletasks()
			# # Deal face down card to dealer
			# d1card = tk.Label(self.root, 
			# 	image=self.dealer.hand[0].face_down_image)
			# d1card.place(x=250, y=50)
			# self.face_down_card = d1card
			# self.root.update_idletasks()
		# 	# Deal second card to player
		# 	p2card = tk.Label(self.root, image=self.player.hand[1].image)
		# 	p2card.place(x=380, y=self.PLAYER_CARDS_Y_COOR)
		# 	self.player_card_widgets.append(p2card)
		# 	# Deal second face-up card to dealer
		# 	d2card = tk.Label(self.root, image=self.dealer.hand[1].image)
		# 	d2card.place(x=380, y=50)
		# 	# Present player options
		# 	if self.player.get_hand_total == 21:
		# 		self.win_round()
		# 	else:
		# 		# place player option buttons
		# 		self.hit_btn = tk.Button(self.root, text="HIT", fg="black", 
		# 			bg="white", font=("arial", "19", "bold"), padx=22,
		# 			borderwidth=5, command=self.player_hit)
		# 		self.hit_btn.place(x=253, y=490)
		# 		self.stand_btn = tk.Button(self.root, text="STAND", fg="black", 
		# 			bg="white", font=("arial", "19", "bold"),
		# 			borderwidth=5, command=self.player_stand)
		# 		self.stand_btn.place(x=385, y=490)
		# 		self.update_player_status()
		# else:
		# 	self.end_game()


	"""Player elects to stand."""
	def player_stand(self):
		self.player.stand()
		self.update_player_status()


	"""Display end of game screen."""
	def end_game(self):
		print("Implement the 'end_game' method!")
		pass


	""""""


	"""Player wins round"""
	def player_wins_round(self):
		print("Implement 'player_wins_round' method!")


	"""Attach images to each card's image attribute.
	- ALERT: this function is likely the reason for the delayed load time on 
	startup. Consider finding a more efficient method."""
	def assign_img_to_cards(self, deck):
		directory = os.fsencode("used files/Cards")	
		deck_index = 0
		for file in os.listdir(directory):
			# Assign card img
			filename = os.fsdecode(file)
			img_path = "used files/Cards/" + filename
			img = self.sized_image(img_path, 107, 150)
			deck[deck_index].assign_image(img)
			deck_index += 1
		# assign face down image to cards
		for card in deck:
			img_name = "used files/back_of_card.png"
			img = self.sized_image(img_name, 107, 150)
			card.assign_face_down_image(img)


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

	"""Expose the dealer's face down card"""
	def flip_face_down_card(self):
		self.face_down_card.configure(image=self.dealer.hand[0].image)


gui = BlackJackGUI()
gui.create_GUI()