from tkinter import *
import time

root = Tk()

busted_display = Label(root, text="My Label Widget", 
	font=("arial", "15"))
busted_display.place(x=0, y=0)
print("it ran")
root.update_idletasks()
root.after(3000, busted_display.destroy())
print("and then this ran")

root.mainloop()