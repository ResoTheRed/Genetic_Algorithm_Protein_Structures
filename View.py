import tkinter as tk;
from tkinter import *;


class view:

	def __init__(self, view_controller):
		self.master = Tk();
		self.master.title("Genetic Algorithm");
		self.vc = view_controller;
		self.display_index = 1;
		self.define_canvas_vars();
		self.set_canvas()
		self.set_input_fields();
		self.setup_loading_bar();
		self.fitness_displays();
		tk.mainloop();

	# setting variables for the canvas displays
	def define_canvas_vars(self):
		self.canvas_size = 750;
		self.canvas_bg = "#f9f9f9";
		self.loading_bar_width = 330;
		self.loading_bar_height = 30;
		self.loading_bar_bg = "#f9f9f9";
		self.loading_block_color = "#70b3c2";


	#set input fields and submit button to run file
	def set_input_fields(self):
		#title
		tk.Label(text="Genetic Base Structural Search", font=("Helvetica",  26, "bold")).grid(row=0, 
			columnspan=6, sticky="n",pady=10);
		#input fields
		tk.Label(text="File Name").grid(row=1, stick='nsew');
		tk.Label(text="Protein Structure").grid(row=2, stick='nsew');
		#file name input field
		self.file_name_entry = Entry(self.master, width=20);
		self.file_name_entry.insert(0,"input2.txt");
		self.file_name_entry.grid(row=1,column=1);
		#custom structure input field
		self.custom_struct_entry = Entry(self.master, width=20);
		self.custom_struct_entry.grid(row=2,column=1);
		#submition buttons
		self.load_file_btn = tk.Button(self.master, text="Load File Data", width=15, 
			command=self.update_file_name)
		self.load_file_btn.grid(row=1,column=3, padx=15);
		self.load_custom_btn = tk.Button(self.master, text="Load Custom", width= 15, 
			command=self.update_custom_struct);
		self.load_custom_btn.grid(row=2, column=3, padx=15);

	#set up the graphics for the loading bar
	def setup_loading_bar(self):
		tk.Label(text="Done").grid(row=3,stick='nsew');
		self.loading_canvas = Canvas(self.master, width=self.loading_bar_width, 
			height=self.loading_bar_height, bg=self.loading_bar_bg);
		self.loading_canvas.grid(row=3, column=1, columnspan=3, sticky='w');
		self.loading_canvas.create_rectangle(0,0,self.loading_bar_width,
			self.loading_bar_height,width=5.0)
		

	#calls to view_controller to load in data from a given file name
	def update_file_name(self):
		#get name from entry box
		name = self.file_name_entry.get();
		#clear the canvas for next input
		self.clear_canvas();
		# get data from view controller
		self.vc.load_file(name);
		#update the output display
		self.textbox_display(1)
	
	#calls to to load in a custom protein structure based on inputs
	def update_custom_struct(self):
		return self.custom_struct.get();

	#set up the canvas that holds the visual for the protien structures
	def set_canvas(self):
		self.canvas = Canvas(self.master, width=self.canvas_size, height=self.canvas_size, bg=self.canvas_bg);
		self.canvas.grid(row=4, column=0, columnspan=6, rowspan=6, pady=15);
		self.canvas.create_rectangle(0, 0,self.canvas_size,self.canvas_size,width=5.0);
		
	# clears the canvas for the next display
	def clear_canvas(self):
		self.canvas.delete("all");
		self.canvas.create_rectangle(0, 0,self.canvas_size,self.canvas_size,width=5.0);

	# display the graphics for the output_display and control buttons
	def fitness_displays(self):
		#text box display
		self.output_display = tk.Text(self.master,height=4,width=25);
		self.output_display.grid(row=1, column=4, rowspan=2, stick="nw");
		scroll = tk.Scrollbar(self.master);
		#controling buttons
		solve_btn = tk.Button(self.master, text="Run Algorithm", width=14, command=self.test);
		solve_btn.grid(row=1, column=5, padx=15,);
		next_btn = tk.Button(self.master, text="Next", width=14, command=self.next);
		next_btn.grid(row=2, column=5, padx=15,);
		previous_btn = tk.Button(self.master, text="Previous", width=14, command=self.prev);
		previous_btn.grid(row=3,column=5, padx=15,);

	# display the data for the textbox display based on an index
	# index starts at 1 and should end at self.vc.pop_size
	def textbox_display(self, index):
		# clear textbox
		self.output_display.delete(1.0, END);
		# get data from the view controller
		string = self.vc.display_data(index-1);
		self.output_display.insert(tk.END, string);
		#draw the structure to lthe canvas
		temp = self.vc.get_structure(index);
		self.draw_protein_structure(temp);
		

	# next button logic: changes the textbox display into displaying
	# the next chromosome statistics in the  population
	def next(self):
		# global index;
		# move to the next index of data to display
		self.display_index+=1;
		#clear canvas
		self.clear_canvas();
		# write to screen 
		self.textbox_display(self.display_index);

	# prev button logic: changes the textbox display into displaying
	# the previous chromosome statistics in the  population
	def prev(self):
		# move to the next index of data to display
		self.display_index -= 1;
		#clear canvas
		self.clear_canvas();
		# write to screen 
		self.textbox_display(self.display_index);



	def test(self):
		print("Push the button.");



	#draws a protein structure in the canvas; the structure is a dictionary
	def draw_protein_structure(self, structure):
		edges = self.draw_location_min_max(structure);
		#find center for x,y relative to the protein structure
		center_x = ( abs( self.canvas_size - (edges[4]*15) ) /2 ) + abs(edges[0]*15);
		center_y = ( abs( self.canvas_size - (edges[5]*15) ) /2 ) + abs(edges[2]*15);
		old_x = center_x;
		old_y = center_y;
		#param: x1,y1,x2,y2
		for k,v in structure.items():
			nums = k.split(",");
			x = center_x + (15*int(nums[0]));
			y = center_y + (15*int(nums[1]));
			self.canvas.create_text(x,y,text=v,font=("Helvetica", 9));
			self.canvas.create_line(old_x,old_y,x,y, fill="#a0a0a0", dash=(4,4));
			old_x = x;
			old_y = y;

	#find locations of proteins to center drawing on screen
	def draw_location_min_max(self, temp):
		min_x = 0;	
		min_y = 0;
		max_x = 0;
		max_y = 0;
		for k,v in temp.items():
			nums = k.split(",");
			if int(nums[0]) < min_x:
				min_x = int(nums[0]);
			if int(nums[0])> max_x:
				max_x = int(nums[0]);
			if int(nums[1]) < min_y:
				min_y = int(nums[1]);
			if int(nums[1]) > max_y:
				max_y = int(nums[1]);
		return [ min_x, max_x, min_y, max_y, (abs(min_x) + abs(max_x)), (abs(min_y) + abs(max_y))];

