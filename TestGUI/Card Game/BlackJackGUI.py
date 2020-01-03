import tkinter as tk

class BlackJackGUI:
	def __init__(self):
		pass

	def create_GUI(self):
		root = tk.Tk()
		root.title("BlackJack!")
		root.iconbitmap("C:/Users/Noah Caldwell/Documents/SourceCode/"
			"TestGUI - Blackjack/TestGUI/Card Game/used files/"
			"cardgames_tarjet_6241.ico")

		


		root.mainloop()


gui = BlackJackGUI()
gui.create_GUI()

