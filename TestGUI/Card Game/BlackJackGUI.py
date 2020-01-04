import tkinter as tk
from PIL import ImageTk,Image

class BlackJackGUI:
	def __init__(self):
		self.win_width = 720
		self.win_height = 600

	def create_GUI(self):
		# window setup
		root = tk.Tk()
		root.title("BlackJack!")
		root.iconbitmap("C:/Users/Noah Caldwell/Documents/SourceCode/"
			"TestGUI - Blackjack/TestGUI/Card Game/used files/"
			"cardgames_tarjet_6241.ico")
		root.geometry(str(self.win_width)+"x"+str(self.win_height))

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

		play_btn = tk.Button(text="PLAY", width=30, height=15)
		play_btn_x = (self.win_width/2) - (30/2)
		play_btn_y = (self.win_height/2) - (15/2)
		play_btn.place(x=play_btn_x, y=play_btn_y)


		root.mainloop()


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

