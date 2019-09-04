import tkinter as tk;
from tkinter import *;


class view:

	def __init__(self, view_controller):
		self.master = Tk();
		self.master.title("Genetic Algorithm");
		self.vc = view_controller;
		self.set_canvas()
		self.set_input_fields();
		self.fitness_displays();
		tk.mainloop();


	#set input fields and submit button to run file
	def set_input_fields(self):
		#input fields
		tk.Label(text="File Name").grid(row=0, stick='w');
		tk.Label(text="Protein Structure").grid(row=1, stick='w');
		#file name input field
		self.file_name_entry = Entry(self.master, width=20);
		self.file_name_entry.insert(0,"Input.txt");
		self.file_name_entry.grid(row=0,column=1);
		#custom structure input field
		self.custom_struct_entry = Entry(self.master, width=20);
		self.custom_struct_entry.grid(row=1,column=1);
		#submition buttons
		self.load_file_btn = tk.Button(self.master, text="Load File Data", width=18, command=self.update_file_name)
		self.load_file_btn.grid(row=0,column=3);
		self.load_custom_btn = tk.Button(self.master, text="Load Custom", width= 18, command=self.update_custom_struct);
		self.load_custom_btn.grid(row=1, column=3);

	#calls to view_controller to load in data from a given file name
	def update_file_name(self):
		name = self.file_name_entry.get();
		self.vc.load_file(name);
		#update the output display
		self.vc.
	
	#calls to to load in a custom protein structure based on inputs
	def update_custom_struct(self):
		return self.custom_struct.get();

	#set up the canvas that holds the visual for the protien structures
	def set_canvas(self):
		self.canvas_size = 896;
		self.canvas = Canvas(self.master, width=self.canvas_size, height=self.canvas_size);
		self.canvas.grid(row=5, column=0, columnspan=10, rowspan=10);
		self.canvas.create_rectangle(0, 0,self.canvas_size,self.canvas_size,width=5.0);
		temp = {'0,0': 'h', '0,1': 'h', '0,2': 'h', '0,3': 'h', '-1,3': 'h', '-1,4': 'h', '-1,5': 'h', 
		'0,5': 'h', '0,6': 'h', '0,7': 'h', '-1,7': 'h', '-1,8': 'h', '-2,8': 'p', '-2,9': 'h', '-2,10': 'p', 
		'-3,10': 'h', '-4,10': 'p', '-4,11': 'p', '-4,12': 'h', '-4,13': 'h', '-4,14': 'p', '-5,14': 'p', 
		'-6,14': 'h', '-7,14': 'h', '-7,15': 'p', '-7,16': 'p', '-7,17': 'h', '-7,18': 'p', '-6,18': 'p', '-6,19': 'h', 
		'-6,20': 'h', '-6,21': 'p', '-7,21': 'p', '-8,21': 'h', '-9,21': 'h', '-10,21': 'p', '-11,21': 'p', '-12,21': 'h', 
		'-12,22': 'p', '-13,22': 'p', '-13,23': 'h', '-13,24': 'h', '-13,25': 'p', '-12,25': 'p', '-11,25': 'h', 
		'-11,26': 'h', '-11,27': 'p', '-10,27': 'p', '-10,28': 'h', '-11,28': 'p', '-11,29': 'h', '-11,30': 'p', 
		'-11,31': 'h', '-12,31': 'h', '-13,31': 'h', '-13,32': 'h', '-12,32': 'h', '-11,32': 'h', '-11,33': 'h', '-12,33': 'h', 
		'-12,34': 'h', '-12,35': 'h', '-12,36': 'h', '-12,37': 'h'}
		self.draw_protein_structure(temp)

	# display the graphics for the output_display and control buttons
	def fitness_displays(self):
		#text box display
		self.output_display = tk.Text(self.master,height=4,width=25);
		self.output_display.grid(row=0, column=4, rowspan=5, stick="nw");
		scroll = tk.Scrollbar(self.master);
		#controling buttons
		solve_btn = tk.Button(self.master, text="Run Algorithm", width=18, command=self.test);
		solve_btn.grid(row=0, column=5);
		next_btn = tk.Button(self.master, text="Next", width=18, command=self.test);
		next_btn.grid(row=1, column=5);
		previous_btn = tk.Button(self.master, text="Previous", width=18, command=self.test);
		previous_btn.grid(row=2,column=5); 

	# next and previous button logic
	def next_prev(self, dir):
		if

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

