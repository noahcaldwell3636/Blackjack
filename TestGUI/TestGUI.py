import inspect
from tkinter import *
import os
from PIL import ImageTk,Image
import __main__ as main
from win32 import win32api

class testGUI:

	def __init__(self):
		self.testCases = []

		#fonts
		self.title_font = ("Helvetica", 24, "bold")
		self.column_header_font = ("Helvetica", 14, "normal")
		self.method_font = ("system", 12, "normal")


	# Run all methods that start with 'test'
	def main(self):
		self.update_cases()
		self.create_GUI()


	def setup(self):
		pass


	def assertEquals(self, inspect_method, test_value, expected_value):
		"""_summary_

		Args:
			inspect_method (_type_): _description_
			test_value (_type_): _description_
			expected_value (_type_): _description_
		"""
		method = self._reduce_to_method(inspect_method)
		assertion = self._reduce_to_method(inspect.currentframe())
		# Check is the assertion is correct, currently casts values to strings. May want to 
		# give the user information on if the values are of the same type in the future.
		result = ""
		if str(test_value) == str(expected_value):
			result = "SUCCESS!"
		else:
			result = "FAILURE!"
		
		test_case = {
			'method': method,
			'assertion_type': assertion,
			'result': result, 
			'test_value': test_value, 
			'expected_value': expected_value
			}
		self.testCases.append(test_case)


	def assertNotEqual(self, inspect_method, test_value, expected_value):
		method = self._reduce_to_method(inspect_method)
		assertion = self._reduce_to_method(inspect.currentframe())
		result = ""
		if str(test_value) != str(expected_value):
			result = "SUCCESS!"
		else:
			result = "FAILURE!"

		print(f"||| {method}... {result} ||| expected_not_equal={expected_value}, was={test_value}")
		
		test_case = {
			'method': method,
			'assertion_type': assertion,
			'result': result, 
			'test_value': test_value, 
			'expected_value': expected_value
			}
		self.testCases.append(test_case)


	def assertTrue(self, inspect_method, test_value):
		method = self._reduce_to_method(inspect_method)
		assertion = self._reduce_to_method(inspect.currentframe())
		result = ""
		if test_value == True:
			result = "SUCCESS!"
		else:
			result = "FAILURE!"

		print(f"||| {method}... {result} ||| expected=True, was={test_value}")
		
		test_case = {
			'method': method,
			'assertion_type': assertion,
			'result': result, 
			'test_value': test_value, 
			'expected_value': True
			}
		self.testCases.append(test_case)


	def assertFalse(self, inspect_method, test_value):
		method = self._reduce_to_method(inspect_method)
		assertion = self._reduce_to_method(inspect.currentframe())
		result = ""
		if test_value == False:
			result = "SUCCESS!"
		else:
			result = "FAILURE!"

		print(f"||| {method}... {result} ||| expected=False, was={test_value}")
		
		test_case = {
			'method': method,
			'assertion_type': assertion,
			'result': result, 
			'test_value': test_value, 
			'expected_value': True
			}
		self.testCases.append(test_case)		


	def _reduce_to_method(self, inspected_method):
		string = str(inspected_method)
		l = string.split(', ')
		method = l[-1]
		method = method.replace('code ', '')
		method = method.replace('>', '')
		return method


	"""Creates a Tkinter PhotoImage with dimensions specified in the parameters using a image's
	file path. Can cause distorted images if the dimesions are not proportional to the orginal 
	photo's dimesions. Accepts .png files."""
	def sized_image(self, img_path, w, h):
		img = Image.open(img_path)  # PIL solution
		img = img.resize((w, h), Image.Resampling.LANCZOS) # (height, width)
		img = ImageTk.PhotoImage(img) # convert to PhotoImage
		return img


	"""Creates the Graphical User Interface that will display all the testing Information"""
	def create_GUI(self):
		# Create window
		root = Tk()
		root.title("Test GUI")
		current_directory = os.path.dirname(__file__)
		used_files_path = os.path.join(current_directory, "used files")
		root.iconbitmap(os.path.join(used_files_path,"checkbox.ico"))
		# Display the user's test script as the main title/header of the window
		global title_font
		path = main.__file__ # will show the actual test file thats using this module
		main_scriptname = path.split("\\")[-1]
		title_label = Label(root, text=f"{main_scriptname}", font=self.title_font)
		title_label.grid(row=0, column=0, columnspan=5, sticky="WENS")
		# create column headings
		test_case_header = Label(root, text="Test Case", font=self.column_header_font)
		test_case_header.grid(row=1, column=0, padx=10)
		result_header = Label(root, text="Result", font=self.column_header_font)
		result_header.grid(row=1, column=1, padx=10)
		assertion_header = Label(root, text="Assert Type", font=self.column_header_font)
		assertion_header.grid(row=1, column=2)
		exp_value_header = Label(root, text="Expected Value", font=self.column_header_font)
		exp_value_header.grid(row=1, column=3, padx=10)
		return_value_header = Label(root, text="Returned Value", font=self.column_header_font)
		return_value_header.grid(row=1, column=4, padx=10)

		# Add information for each test case
		row_index = 2
		success_img = self.sized_image(
			os.path.join(used_files_path, "Check.png"), 30, 30)
		fail_img = self.sized_image(
			os.path.join(used_files_path, "cross.png"), 30, 30)
		for test_case in self.testCases:
			# Display Method Name
			method = test_case.get('method', 'Method couldnt be found );')
			method_label = Label(root, text=method)
			method_label.grid(row=row_index, column=0, sticky=W+E)
			# Display Result Icon
			result = test_case.get('result', 'result couldnt be found );')
			canvas = Canvas(root) 
			if result == "SUCCESS!":
				img_label = Label(root, image=success_img)
				img_label.grid(row=row_index, column=1, padx=10)
			elif result == "FAILURE!":
				img_label = Label(root, image=fail_img)
				img_label.grid(row=row_index, column=1, padx=10)
			else:
				raise ValueError("test case result variable has invalid string value")
			# Display assertion type
			assertion_type = test_case.get('assertion_type', 'assertion type couldnt be found')
			ass_label = Label(root, text=f"{assertion_type}")
			ass_label.grid(row=row_index, column=2, padx=10)
			# Display Expected Values
			expected_value = test_case.get('expected_value', 'expected_value couldnt be found );')
			exp_label = Label(root, text=f"{expected_value}")
			exp_label.grid(row=row_index, column=3, padx=10)
			# Display Test Values	
			test_value = test_case.get('test_value', 'test_value couldnt be found );')
			test_label = Label(root, text=f"{test_value}")
			test_label.grid(row=row_index, column=4, padx=10)
			# next row
			row_index += 1

		update_button = Button(root, text="Update", command=self.update_cases)
		update_button.grid(row=row_index, column=0, columnspan=5)

		# Move monitor to bottom right corner
		# BUG - window appears in the top left corner for a fraction of a second before
		# appearing in the bottom right corner
		root.update_idletasks()
		self.position_monitor(root)
		# Complete Tkinter loop
		root.mainloop()


	"""Moves a tkinter window to the bottom right corner"""
	def position_monitor(self, window):
		# Get main monitor inofrmation 
		for monitor in win32api.EnumDisplayMonitors():
			monitor_info = win32api.GetMonitorInfo(monitor[0])
			if monitor_info['Flags'] == 1:
				break
		# Calculate where the window should be placed on the screen so that it appears
		# in the bottom right corner
		work_area = list(monitor_info['Work'])
		screen_width = work_area[-2]
		screen_height = work_area[-1]
		window_width = window.winfo_width()
		window_height = window.winfo_height()
		width_adjustment = 11
		height_adjustment = 35
		x_coordinate = screen_width - window_width - width_adjustment
		y_coordinate = screen_height - window_height - height_adjustment
		# Place the window on the screen 
		geom = f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}'
		window.geometry(geom)

	"""
	Update test cases
	"""
	def update_cases(self):
		attributes = (getattr(self, name) for name in dir(self))
		for method in attributes:
			if inspect.ismethod(method) and method.__name__[0:4] == "test":
				method()
    
# test = testGUI()
# test.main()
