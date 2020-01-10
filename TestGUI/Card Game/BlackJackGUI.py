import tkinter as tk
from PIL import ImageTk,Image
import player, dealer

class BlackJackGUI:
	def __init__(self):
		self.win_width = 720
		self.win_height = 600
		self.root = None
		self.dealer = dealer.Dealer()
		self.player = player.Player(dealer)

		self.bankroll_display = None

		# used in newgame method, logic may want to be handled in a less
		# messy way when refactoring
		self.please_add_lable = None

	def create_GUI(self):
		# window setup
		root = tk.Tk()
		root.title("BlackJack!")
		root.iconbitmap("C:/Users/Noah Caldwell/Documents/SourceCode/"
			"TestGUI - Blackjack/TestGUI/Card Game/used files/"
			"cardgames_tarjet_6241.ico")
		root.geometry(str(self.win_width)+"x"+str(self.win_height))
		self.root = root

		# Create start screen
		root.configure(background='black')
		title_letters = self.sized_image("C:/Users/Noah Caldwell/Docume"
			"nts/SourceCode/TestGUI - Blackjack/TestGUI/Card Game/used "
			"files/generatedtext.png", 
			600, 
			100)
		title_label = tk.Label(image=title_letters, bg="#EA1616")
		title_xcoor = (720/2) - (600/2)
		title_ycoor = (600/2) - 240
		title_label.place(x=title_xcoor, y=title_ycoor)

		play_btn = tk.Button(text="PLAY", width=10, 
			bg="#EA1616", font=("arial", "30"), command=self.setup_new_game)
		play_btn_x = (self.win_width/2) - 115
		play_btn_y = (self.win_height/2) - (15/2)
		play_btn.place(x=play_btn_x, y=play_btn_y)

		self.update_bankroll()

		root.mainloop()

	"""set up for after the play selects 'play' from the start menu."""
	def setup_new_game(self):
		# clear widgets
		widgets = self.root.winfo_children()
		for w in widgets:
			w.destroy()

		# add game screen
		background_image = self.sized_image("C:/Users/Noah Caldwell/Doc"
			"uments/SourceCode/TestGUI - Blackjack/TestGUI/Card Game/us"
			"ed files/greenfelt.png", 720, 600)
		background_label = tk.Label(self.root, image=background_image)
		background_label.photo = background_image
		background_label.place(x=0, y=0)

		# Player buys bankroll
		# Instruction text
		self.instr_text = tk.Label(self.root, 
			text=f"How much do you want\n  to play with?", 
			font=("arial", "40"), bg="black", fg="white")
		self.instr_text.place(x=75, y=80)

		#  buy five hundred 
		self.five_hun_btn = tk.Button(self.root, text="500", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(500))
		self.five_hun_btn.place(x=100, y=300)
		# buy one hundred 
		self.one_hun_btn = tk.Button(self.root, text="100", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(100))
		self.one_hun_btn.place(x=230, y=300)
		# buy fifty
		self.fifty_btn = tk.Button(self.root, text="50", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(50))
		self.fifty_btn.place(x=360, y=300)
		# buy twenty five
		self.twenty_five_btn = tk.Button(self.root, text="25", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(25))
		self.twenty_five_btn.place(x=490, y=300)

		# display total bankroll as you buy chips
		self.bankroll_display = tk.Label(self.root, 
			text=f"bankroll = {self.player.bankroll}", 
			font=("arial", "40"), bg="black", fg="white")
		self.bankroll_display.place(x=265, y=430)
		self.update_bankroll()

		# place 'ready to play' button
		self.ready_btn = tk.Button(self.root, text="READY!", bg="white", 
			fg="black", font=("arial", "20", "bold"), 
			command=self.start_game)
		self.ready_btn.place(x=570, y=530)



	"""Updates Bankroll display label every .3 seconds"""
	def update_bankroll(self):
		if type(self.bankroll_display) != type(None):
			self.bankroll_display.config(text=f"bankroll\n{self.player.bankroll}")
			self.root.after(300, self.update_bankroll)

	"""Clear the unneeded widgets and move the bankroll display to 
	prepare for the game"""
	def start_game(self):
		if self.player.bankroll > 0:
			# remove widgets
			self.instr_text.destroy()
			self.five_hun_btn.destroy()
			self.one_hun_btn.destroy()
			self.fifty_btn.destroy()
			self.twenty_five_btn.destroy()
			self.ready_btn.destroy()
			if self.please_add_lable is not None:
				self.please_add_lable.destroy()
			# move bankroll display to left corner
			self.move_display()
			self.choose_bet()
		else:
			self.please_add_lable = tk.Label(self.root, 
				text="Please choose an amount of money\n to play with.", 
				font=("arial", "8","bold"), bg="black", fg="red")
			self.please_add_lable.place(x=500, y=480)
			self.warning_displayed = True


	"""Player picks bet amount"""
	def choose_bet(self):
		# Instruction text
		self.instr_text = tk.Label(self.root, 
			text=f"How much do you want\n  to bet?", 
			font=("arial", "40"), bg="black", fg="white")
		self.instr_text.place(x=75, y=80)

		# bet one hundred 
		self.one_hun_btn = tk.Button(self.root, text="100", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.place_bet(100))
		self.one_hun_btn.place(x=230, y=300)
		# bet fifty
		self.fifty_btn = tk.Button(self.root, text="50", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.place_bet(50))
		self.fifty_btn.place(x=360, y=300)
		# bet twenty five
		self.twenty_five_btn = tk.Button(self.root, text="25", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.place_bet(25))
		self.twenty_five_btn.place(x=490, y=300)

		# current bet display
		self.bet_display = tk.Label(self.root, 
			text=f"current bet\n{self.player.current_bet}", 
			font=("arial", "15"), bg="black", fg="white")
		self.bet_display.place(x=24, y=442)
		self.update_bankroll()



	"""Move the bankroll_display label to the left corner while making
	it smaller incrementally of the course of a second or so."""
	def move_display(self):
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


	"""Creates a Tkinter PhotoImage with dimensions specified in the 
	parameters using a image's file path. Can cause distorted images if 
	the dimesions are not proportional to the orginal 
	photo's dimesions. Accepts .png files."""
	def sized_image(self, img_path, w, h):
		img = Image.open(img_path)  # PIL solution
		img = img.resize((w, h), Image.ANTIALIAS) # (height, width)
		img = ImageTk.PhotoImage(img) # convert to PhotoImage
		return img


gui = BlackJackGUI()
gui.create_GUI()

