import tkinter as tk
from tkinter import *  # Tk, Entry, OptionMenu, Canvas
from tkinter.ttk import Progressbar


class view:

	def __init__(self, view_controller):
		self.master = Tk()
		self.master.title("Genetic Algorithm")
		self.vc = view_controller
		self.vc.set_view(self)
		self.display_index = 1
		self.define_canvas_vars()
		self.set_canvas()
		self.set_input_fields_top()
		self.setup_loading_bar()
		self.fitness_displays()
		self.setup_input_display()
		self.chrom_num = 1
		tk.mainloop()

	# setting variables for the canvas displays
	def define_canvas_vars(self):
		self.canvas_size = 720
		self.canvas_bg = "#f9f9f9"
		self.loading_bar_length = 180
		self.loading_bar_bg = "#f9f9f9"
		self.loading_block_color = "#70b3c2"


	#set input fields and submit button to run file
	def set_input_fields_top(self):
		#title
		tk.Label(text="Genetic Base Structural Search", font=("Helvetica",  26, "bold")).grid(row=0, 
			columnspan=12, sticky="n",pady=10)
		#input fields
		tk.Label(text="File Name").grid(row=1, stick='nse')
		tk.Label(text="Custom Seq").grid(row=1, column=2, stick='nse')
		#file name input field
		self.file_name_entry = Entry(self.master, width=25)
		self.file_name_entry.insert(0,"input2.txt")
		self.file_name_entry.grid(row=1,column=1, columnspan=2,padx=10,pady=4,stick='nsw')
		#custom structure input field
		self.custom_struct_entry = Entry(self.master, width=68)
		self.custom_struct_entry.grid(row=1,column=3,columnspan=3,padx=20,pady=4,stick='nse')
		#submition buttons
		self.load_file_btn = tk.Button(self.master, text="Load File", width=28, 
			command=self.update_file_name)
		self.load_file_btn.grid(row=2,column=0, columnspan=2, padx=10,pady=1,stick='nse')
		self.load_custom_btn = tk.Button(self.master, text="Load Custom", width= 28, 
			command=self.update_custom_struct)
		self.load_custom_btn.grid(row=3, column=0, columnspan=2, padx=10,pady=1,stick='nse')

	#set up the graphics for the loading bar
	def setup_loading_bar(self):
		self.load_text = tk.StringVar()
		self.load_text.set("done")
		tk.Label(self.master, textvariable=self.load_text).grid(row=5,stick='nsw',padx=18,pady=4)
		self.loading_bar = Progressbar(self.master, orient=HORIZONTAL, length=self.loading_bar_length, 
			mode="determinate")
		self.loading_bar.grid(row=5, column=0, columnspan=2, stick='nse',padx=10,pady=4)
		self.load_location = 0

	# display the graphics for the output_display and control buttons
	#TODO: change text box to canvas
	def fitness_displays(self):
		#text box display
		self.output_display = tk.Text(self.master,height=11,width=32)
		self.output_display.grid(row=6, column=0, columnspan=2, stick='nse', padx=10,pady=4)
		#controling buttons
		next_btn = tk.Button(self.master, text="Next", width=12, command=self.next)
		next_btn.grid(row=7, column=1,stick='nsew', padx=10)
		previous_btn = tk.Button(self.master, text="Previous", width=12, command=self.prev)
		previous_btn.grid(row=7,column=0,stick='nse')

		#TODO: move run and write button to another method
		write_btn = tk.Button(self.master, text="Write Solutions to File",width=28,command=self.write_to_file)
		write_btn.grid(row=14, column=0, columnspan=2,padx=10,pady=2,stick='nse')
		solve_btn = tk.Button(self.master, text="Run Algorithm", width=28, command=self.find_fitness)
		solve_btn.grid(row=15, column=0,columnspan=2, padx=10, pady=15, sticky="nse")
		


	def setup_input_display(self):
		# Labels
		tk.Label(text="Population Size").grid(row=8, stick='nse')
		tk.Label(text="Elite Percent").grid(row=9, stick='nse')
		tk.Label(text="Random Percent").grid(row=10, stick='nse')
		tk.Label(text="Crossover Percent").grid(row=11, stick='nse')
		tk.Label(text="Mutation Percent").grid(row=12, sticky='nse')
		tk.Label(text="Fitness Plateau").grid(row=13, stick='nse')
		# dropdowns String vars
		self.eliteVar = tk.StringVar()
		self.eliteVar.set("10%")
		self.randVar = tk.StringVar()
		self.randVar.set("10%")
		self.plateauVar = tk.StringVar()
		self.plateauVar.set("100")
		self.popVar = tk.StringVar()
		self.popVar.set("200")
		self.crossVar = tk.StringVar()
		self.crossVar.set("80%")
		self.mutateVar = tk.StringVar()
		self.mutateVar.set("20%") 
		# dropdown choices
		elite_random = ["10%","5%","15%","20%"]
		cross = ["80%","60%","65%","70%","75%","80%","85%","90%"]
		plateau = ["100","10","25","50","200","400","1000","5000","15000"]
		pop = ["200","50","100","150","350","600","1000","5000"]
		mutate = ["5%","10%","15%","20%","25%", "30%", "40%", "50%"]
		# dropdown menus
		popMenu = OptionMenu(self.master, self.popVar,*pop)
		popMenu.grid(row=8,column=1,sticky="nsew",padx=10,pady=1)
		eliteMenu = OptionMenu(self.master, self.eliteVar, *elite_random)
		eliteMenu.grid(row=9,column=1,sticky="nsew",padx=10,pady=1)
		randomMenu = OptionMenu(self.master, self.randVar,*elite_random)
		randomMenu.grid(row=10,column=1,sticky="nsew",padx=10,pady=1)
		crossMenu = OptionMenu(self.master, self.crossVar, *cross)
		crossMenu.grid(row=11,column=1, sticky="nsew",padx=10,pady=1)
		mutateMenu = OptionMenu(self.master, self.mutateVar, *mutate)
		mutateMenu.grid(row=12,column=1,sticky='nsew',padx=10,pady=1)
		plateauMenu = OptionMenu(self.master, self.plateauVar,*plateau)
		plateauMenu.grid(row=13,column=1,sticky="nsew",padx=10,pady=1)

	# return a list of the custom settings for use in the model
	# form: ["200","10%",...]
	def get_settings(self):
		temp = [self.display_index, self.popVar.get(), 
				self.eliteVar.get(), self.randVar.get(), 
				self.crossVar.get(), self.mutateVar.get(),
				self.plateauVar.get()]
		return temp

	#calls to view_controller to load in data from a given file name
	def update_file_name(self):
		# get name from entry box
		name = self.file_name_entry.get()
		# clear the canvas for next input
		self.clear_canvas()
		# get data from view controller
		self.vc.load_file(name)
		# update the output display
		self.textbox_display(1)
		#update number of chromosomes ref
		self.chrom_num = self.vc.get_pop_size()
	
	# fill in loading bar based on chunk size
	def update_loading_bar(self, chunk, loc):
		self.loading_bar['value'] += chunk
		self.load_text.set("working...")
		self.master.update_idletasks()

	# clean the graphics for the loading bar
	def clear_load_bar(self):
		self.loading_bar["value"] = 0
		# self.load_text.set("done")
		self.master.update_idletasks()
		

	# increment the loading bar based on population size and finished chromosomes
	def load(self):
		if self.load_location == 0:
			self.load_text.set("working...")
		self.update_loading_bar(100/self.vc.pop_size,self.load_location)
		self.load_location += 1
		if self.load_location >= self.vc.pop_size:
			self.load_location = 0
			self.load_text.set("done")
			self.clear_load_bar()
			

	#set up the canvas that holds the visual for the protien structures
	def set_canvas(self):
		self.canvas = Canvas(self.master, width=self.canvas_size, height=self.canvas_size, bg=self.canvas_bg)
		self.canvas.grid(row=2, column=2, columnspan=4, rowspan=14, pady=15, padx=15)
		self.canvas.create_rectangle(0, 0,self.canvas_size,self.canvas_size,width=5.0)
		
	# clears the canvas for the next display
	def clear_canvas(self):
		self.canvas.delete("all")
		self.canvas.create_rectangle(0, 0,self.canvas_size,self.canvas_size,width=5.0)

	
	# display the data for the textbox display based on an index
	# index starts at 1 and should end at self.vc.pop_size
	def textbox_display(self, index):
		# clear textbox
		self.output_display.delete(1.0, END)
		# get data from the view controller
		string = self.vc.display_data_textbox(index)
		self.output_display.insert(tk.END, string)
		#draw the structure to lthe canvas
		temp = self.vc.get_structure(index)
		self.draw_protein_structure(temp)
		

	# limit the size of index to the number of chromosomes
	def check_index(self):
		if self.display_index > self.chrom_num:
			self.display_index = 1
		elif self.display_index < 1:
			self.display_index = self.chrom_num

	# next button logic: changes the textbox display into displaying
	# the next chromosome statistics in the  population
	def next(self):
		# global index;
		# move to the next index of data to display
		self.display_index+=1
		self.check_index()
		#clear canvas
		self.clear_canvas()
		# write to screen 
		self.textbox_display(self.display_index)

	# prev button logic: changes the textbox display into displaying
	# the previous chromosome statistics in the  population
	def prev(self):
		# move to the next index of data to display
		self.display_index -= 1
		self.check_index()
		#clear canvas
		self.clear_canvas()
		# write to screen 
		self.textbox_display(self.display_index)

	def find_fitness(self):
		# set loading text label to working
		self.load_text.set("working...")
		self.update_loading_bar(100,"0")
		# send parameters to the view controller
		self.vc.set_vars_from_view(self.get_settings())
		# solve for best fitness
		self.vc.find_fitness(self.display_index)
		# update display
		self.clear_canvas()
		self.textbox_display(self.display_index)
		self.load_text.set("done")
		self.clear_load_bar()
		
		

	def write_to_file(self):
		pass

	def update_custom_struct(self):
		pass

	#draws a protein structure in the canvas; the structure is a dictionary
	def draw_protein_structure(self, structure):
		# set up structure to draw near the center of the canvas
		structure = self.define_directions(structure)
		edges = self.draw_location_min_max(structure)
		
		font_size = 10 
		pixel = 20 

		#find center for x,y relative to the protein structure
		center_x = ( self.canvas_size/2 - (edges[4]*pixel)/2 )
		center_y = ( self.canvas_size/2 - (edges[5]*pixel)/2 )
		old_x = center_x
		old_y = center_y
		
		# self.canvas.create_text(self.canvas_size/2,self.canvas_size/2,text='+',font=("Helvetica", 9))
		#param: x1,y1,x2,y2
		for k,v in structure.items():
			nums = k.split(",")
			x = center_x + int(pixel*int(nums[0]))
			y = center_y + int(pixel*int(nums[1]))
				
			self.canvas.create_text(x,y,text=v,font=("Helvetica", font_size))
			self.canvas.create_line(old_x,old_y,x,y, fill="#a0a0a0")
			old_x = x
			old_y = y
		
	def define_directions(self, structure,x_offset=0, y_offset=0):
		count = 0
		temp = {}
		for k,v in structure.items():
			a = k.split(",")
			arr=[int(a[0]), int(a[1])]
			if count==0:
				x_offset += arr[0]
				y_offset += arr[1]
				temp[str(arr[0]-x_offset)+","+str(arr[1]-y_offset)] = v
			else:
				temp[str(arr[0]-x_offset)+","+str(arr[1]-y_offset)] = v
			count+=1
		return temp


	#find locations of proteins to center drawing on screen
	def draw_location_min_max(self, temp):
		count=1
		for k,v in temp.items():
			nums = k.split(",")		
			if count ==1:
				min_x = int(nums[0])	
				min_y = int(nums[1])
				max_x = int(nums[0])
				max_y = int(nums[1])
		
			if int(nums[0]) < min_x:
				min_x = int(nums[0])
			if int(nums[0])> max_x:
				max_x = int(nums[0])
			if int(nums[1]) < min_y:
				min_y = int(nums[1])
			if int(nums[1]) > max_y:
				max_y = int(nums[1])
			count+=1
		return [ min_x, max_x, min_y, max_y, abs(abs(max_x) - abs(min_x)), abs( abs(max_y)-abs(min_y) ) ]
