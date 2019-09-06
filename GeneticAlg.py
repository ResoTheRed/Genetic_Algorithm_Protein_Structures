import random as r;

START = 0;
NORTH= 1;
EAST = 2;
SOUTH = 3;
WEST = 4;
TOTAL = 10;
PREV_LEFT = 7;
PREV_RIGHT = 9;
PREV_DOWN = 6;
PREV_UP = 8;

class model:
	
	#constructor
	def __init__(self):
		self.data = None;
		

	#ge a reference to the view controller
	def set_view_controller(self, view_controller):
		self.vc = view_controller;

	# pull the population size 
	def set_pop_size(self, file_name):
		fh = open(file_name, "r");
		line = fh.readline();
		line.replace("\n","");
		arr = line.split(" ");
		self.vc.set_pop_size(int(arr[2]));
		fh.close();

	#gain a referance to the input data
	def setup_data(self, file_name):
		#check if data object has been create it
		self.set_pop_size(file_name);
		if self.data is None:
			self.data = data_input(self, file_name);
		else:
			self.data.clear();
			self.data.update_data_object(file_name);
		#set up fitness
		self.setup_fitness();

	# give data reference to fitness alg model 
	def setup_fitness(self):
		if self.data is None:
			return;
		self.fitness(self.data);

	# create a way for the model logic objects to communicate to the
	# view controller
	def signal_view_controller(self, type_):
		if type_ == "data_object":
			self.vc.loading_signal_from_data();

class data_input:

	"""
	location and sequence
	0[{"0,0,":'h', "0,1":"p", "1,1":'h'}] # chromosome seq style in dict
	1[{}]
	"""

	#data_input constructor
	def __init__(self, model, file_name):
		self.model = model;
		self.update_data_object(file_name);
		#self.separate_chromosomes(pop);

	def update_data_object(self, file_name):
		pop = self.unpack_from_file(file_name);
		self.chromosomes = self.separate_chromosomes(pop);
	
	#clear out population
	def clear(self):
		self.pop_size = 0;
		self.chromosomes = {};

	# pull the data from the file and return it in a dictionary
	# Seq1: {"0":"h", "1","p"}
	# Fitness1: -9
	# count starts at 1
	def unpack_from_file(self, file_name):
		#variables
		pop = {};
		count = 1;
		fh = open(file_name, 'r');
		line = fh.readline();
		self.chromosome_length = list();
		#parse each line
		while line:
			line = line.replace('\n','');
			arr = line.split(" ");
			if arr[0] == "TotalProtein":
				self.pop_size = int(arr[2]);
			elif arr[0] == "Seq":
				arr[2] = arr[2].replace("\n","");
				self.chromosome_length.append(len(arr[2]));
				pop[arr[0] + str(count)] = self.parse_seq(list(arr[2]));	
			elif arr[0] == "Fitness":
				pop[arr[0]+str(count)] = arr[2];
				count += 1;
			line = fh.readline();
		return pop;

	#create dictionary for locations of chromosome sequences
	def parse_seq(self, seq):
		temp ={};
		for i in range(len(seq)):
			temp[str(i)] = seq[i];
		return temp;

	#pass each chromosome sequence for location assignment
	def separate_chromosomes(self, pop):
		i = 1;
		tries = 0;
		#for each chromosome in the population, create initial structure
		#pass in a dictionary of locations
		while i<self.pop_size+1:
			temp = self.initial_directions( pop["Seq"+str(i)] );
			tries+=1;
			#keep chromosome structures that match the original size
			if len(temp) == self.chromosome_length[i-1]:
				pop["Seq"+str(i)] = temp;
				print("Random attemps: "+str(tries));
				self.model.signal_view_controller("data_object");
				i+=1;
				tries = 0;
		return pop;
			

	#set locations to each elements in a chromosome
	def initial_directions(self, seq_dict):
		location = "0,0";
		previous = "0,0";
		temp={};
		bad_layout = False;
		for k,v in seq_dict.items():
		 	#generate the random 4 directions
			dir_list = self.random_four();
			previous = location; 

			for i in range(len(dir_list)):
		 		#convert into string location based on randomly generated direction
				location = self.check_direction(dir_list[i], previous, k);
		 		#check if location is valid				
				if location in seq_dict:
					location = previous;
					if i == len(dir_list):
						bad_layout = True;
				else:
					# print("k: "+k+": "+str(dir_list[i])+" ("+location+")" );
					temp[location] = seq_dict[k];
					previous = location;
					break;

			#if a node cannot be placed, scrap order and start over
			if bad_layout:
				break;
		 	 
		#if everything checks out add to class variable
		#create fitness list with 0 and given fitness
		return temp;
		


	#return a location based on direction chosen
	#param prev as a string holds last location ["0,0"] 
	def check_direction(self, direction, prev, k):
		nums = prev.split(",");
		if k == '0':
			return ("0"+","+"0");
		elif direction == EAST:
			nums[0] = str(int(nums[0])+1); #East:   +0,+1
		elif direction == NORTH:
			nums[1] = str(int(nums[1])+1) #north:  +1,+0
		elif direction == WEST:
			nums[0] = str(int(nums[0])-1); #West:   +0,-1
		elif direction == SOUTH:
			nums[1] = str(int(nums[1])+1) #south:  -1,+0
		return (nums[0]+","+nums[1]);
	
	#generate unique numbers 1 through 4 in a random order
	#returns the numbers in a list
	def random_four(self):
		temp = list();
		counter = 0;
		while True:
			temp = [r.randint(1,4),r.randint(1,4),r.randint(1,4),r.randint(1,4)];
			if temp[1] == temp[2] or temp[1] == temp[3] or temp[1] == temp[0]:
				counter+=1;
			if temp[2] == temp[3] or temp[2] == temp[0]:
				counter+=1;
			if temp[3] == temp[0]:
				counter+=1;
			if counter == 0:
				break;
			counter = 0;
		return temp;


class fitness_generator:
	"""
		fitness_generator class is responsible for mutating the population
		gathered from the data_input class, in such a way to find the 
		patterns for lowest energy
	"""
	# def __init__(self, data):
	# 	#set a reference to the data object
	# 	self.data = data;
	# 	self.pop_size = self.data.pop_size;
	# 	self.old_pop = self.data.chromosomes;
	# 	self.new_pop = None;

	def __init__(self, pop):
		conn = self.track_connections(pop);
		fit = self.calculate_fitness(pop, conn);
		print("Fitness: "+str(fit));

	# create 100 mutations of sequence 
	def generate_initial_pop(self):
		pass;

	def track_connections(self, pop):
		connections = list();
		# establish connections using index as an order
		# this will be the same for each mutation
		for k,v in pop.items():
			connections.append(k);
		return connections;

	# calculate the fitness of the passed in poulation
	# if  value == p then check (+1,0), (-1,0), (0,+1), (0,-1) 
	# relative to the current location if the value at any of 
	# these == p and are not connected (connection list) then
	# add 1 to fitness.  Finally divide fitness by 2 to account 
	# for duplicate adjacencies
	def calculate_fitness(self, pop, conn):
		# pop uses one sequence from the original data
		count = 0;
		fit = 0;
		print(str(len(conn)));
		print(str(len(pop)));
		# check for connections
		for k,v in pop.items():
			if v == "p":
				arr = k.split(",");
				# check locations up down left right for adjacency
				fit += self.match_locations((str(int(arr[0]))+","+str(int(arr[1])+1)), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0]))+","+str(int(arr[1])-1)), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0])-1)+","+str(int(arr[1]))), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0])+1)+","+str(int(arr[1]))), pop, k, count, conn);
				print("Fit: "+str(fit)+" count: "+str(count))
			count+=1;
		#return fitness to compare to previous fitness 
		return int(fit/2);

	# directly index heap for O(1) look up
	def match_locations(self, direct, pop, k, count, connections):
		fitness = 0;

		try:
			# location exist in chromosome and == p
			if pop[direct] == "p": 
				# if the index+1 is in bounds and the direction is not directly connected
				if count != 0 and count < len(connections)-1 and connections[count+1] != direct:
					fitness+=1;
				# if the index-1 is in bounds and the direction is not directly connected
				elif count != len(connections)-1 and count>0 and connections[count-1] != direct:
					fitness+=1;
		except KeyError:
			pass;
		return fitness;

# should be fitness -9;  Example from slides
temp = {"0,0":"p", "1,0":"h", "1,1":"p", "1,2":"h", "0,2":"h", "0,1":"p", "-1,1":"p", "-1,2":"h", "-2,2":"p", "-3,2":"h", "-3,1":"h",
			"-2,1":"p", "-2,0":"h", "-1,0":"p", "-1,-1":"p", "-2,-1":"h", "-2,-2":"h", "-1,-2":"p", "0,-2":"h", "0,-1":"p"};

f = fitness_generator(temp);





