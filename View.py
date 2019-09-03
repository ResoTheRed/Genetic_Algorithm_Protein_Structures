import tkinter as tk;
from tkinter import *;


class view:

	def __init__(self, view_controller):
		self.master = Tk();
		self.master.title("Genetic Algorithm");
		self.vc = view_controller;
		self.set_canvas()
		self.set_input_fields();
		tk.mainloop();


	#set input fields and submit button to run file
	def set_input_fields(self):
		#input fields
		tk.Label(text=" File Name ").grid(row=0);
		tk.Label(text=" Custom Protein Structure ").grid(row=1);
		self.file_name_entry = Entry(self.master);
		self.file_name_entry.insert(0,"Input.txt");
		self.custom_struct_entry = Entry(self.master);
		self.file_name_entry.grid(row=0,column=1);
		self.custom_struct_entry.grid(row=1,column=1);
		#submition buttons
		self.load_file_btn = tk.Button(self.master, text="Load File Data", width=25, command=self.update_file_name)
		self.load_file_btn.grid(row=3,column=0);
		self.load_custom_btn = tk.Button(self.master, text="Load Custom Structure", width= 25, command=self.update_custom_struct);
		self.load_custom_btn.grid(row=4, column=0);

	#calls to vieww_controller to load in data from a given file name
	def update_file_name(self):
		name = self.file_name_entry.get();
		print(name);
		self.vc.load_file(name);
	

	def update_custom_struct(self):
		return self.custom_struct.get();

	def set_canvas(self):
		self.canvas = Canvas(self.master, width=1024, height=1024);
		self.canvas.grid(row=5, column=0);
		self.draw_protein_structure()

	def draw_protein_structure(self):
		temp = {'0,0': 'h', '0,1': 'h', '0,2': 'h', '0,3': 'h', '1,3': 'h', '1,4': 'h', '0,4': 'h', 
			'0,5': 'h', '1,5': 'h', '1,6': 'h', '1,7': 'h', '0,7': 'h', '-1,7': 'p', '-1,8': 'h', 
			'-1,9': 'p', '0,9': 'h', '1,9': 'p', '1,10': 'p', '2,10': 'h', '2,11': 'h', '2,12': 'p', 
			'3,12': 'p', '3,13': 'h', '3,14': 'h', '3,15': 'p', '3,16': 'p', '3,17': 'h', '3,18': 'p', 
			'4,18': 'p', '4,19': 'h', '4,20': 'h', '5,20': 'p', '5,21': 'p', '5,22': 'h', '6,22': 'h', 
			'6,23': 'p', '5,23': 'p', '5,24': 'h', '5,25': 'p', '5,26': 'p', '5,27': 'h', '6,27': 'h', 
			'6,28': 'p', '6,29': 'p', '6,30': 'h', '5,30': 'h', '4,30': 'p', '4,31': 'p', '3,31': 'h', 
			'3,32': 'p', '3,33': 'h', '3,34': 'p', '2,34': 'h', '2,35': 'h', '2,36': 'h', '2,37': 'h', 
			'2,38': 'h', '3,38': 'h', '4,38': 'h', '4,39': 'h', '4,40': 'h', '4,41': 'h', '3,41': 'h', 
			'3,42': 'h'};
		edges = self.draw_location_min_max(temp);
		center = 1024/2;
		old_x = center;
		old_y = old_x;
		#param: x1,y1,x2,y2
		self.canvas.create_rectangle(10, 10,1014,1014,width=5.0);
		for k,v in temp.items():
			nums = k.split(",");
			x = center + (15*int(nums[0]));
			y = center + (15*int(nums[1]));
			self.canvas.create_text(x,y,text=v,font=("Purisa", 7));
			self.canvas.create_line(old_x,old_y,x,y, fill="#a0a0a0", dash=(4,4));
			old_x = x;
			old_y = y;

	#find locations to center drawing on screet
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
				min_x = int(nums[1]);
			if int(nums[1])> max_y:
				max_x = int(nums[1]);
		return [ min_x, max_x, min_y, max_y, (abs(min_x) + abs(max_x)), (abs(min_y) + abs(max_y))];
