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
			bg="#EA1616", font=("arial", "30"), command=self.brand_new_game)
		play_btn_x = (self.win_width/2) - 115
		play_btn_y = (self.win_height/2) - (15/2)
		play_btn.place(x=play_btn_x, y=play_btn_y)

		self.update_bankroll()

		root.mainloop()

	"""set up for after the play selects 'play' from the start menu."""
	def brand_new_game(self):
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
		five_hun_btn = tk.Button(self.root, text="500", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(500))
		five_hun_btn.place(x=0, y=0)

		one_hun_btn = tk.Button(self.root, text="100", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(100))
		one_hun_btn.place(x=0, y=100)

		fifty_btn = tk.Button(self.root, text="50", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(50))
		fifty_btn.place(x=0, y=200)

		twenty_five_btn = tk.Button(self.root, text="25", width=5, 
			bg="black", fg="white", font=("arial", "30"), 
			command=lambda: self.player.buy_chips(25))
		twenty_five_btn.place(x=0, y=300)

		self.bankroll_display = tk.Label(self.root, 
			text=f"bankroll = {self.player.bankroll}")
		self.bankroll_display.place(x=50, y=50)
		self.update_bankroll()

	def update_bankroll(self):
		if type(self.bankroll_display) != type(None):
			self.bankroll_display.config(text=f"bankroll = {self.player.bankroll}")
			self.root.after(300, self.update_bankroll)
			print(self.player.bankroll)


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

