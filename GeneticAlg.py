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
		self.default_pop_size = 200;
		

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
		self.fitness = fitness_generator(self.data);

	# collection of methods to call to find the best fitness
	def find_fitness(self, index):
		#pass reference to the targeting fitness level
		self.fitness.set_target_fitness(self.data.target_fit[index]);
		self.set_init_pop(index);
		self.fitness.run_generations();


	def set_init_pop(self, index):
		if self.data != None:
			pop = self.data.generate_pop(index, self.default_pop_size);
			self.fitness.set_init_pop(pop);

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
		self.seeds = list();
		self.target_fit = list();
		self.model = model;
		self.update_data_object(file_name);
		#self.separate_chromosomes(pop);

	def update_data_object(self, file_name):
		pop = self.unpack_from_file(file_name);
		self.chromosomes = self.separate_chromosomes(pop, self.pop_size+1);
	
	#clear out population
	def clear(self):
		self.pop_size = 0;
		self.chromosomes = {};
		self.seeds = list();
		self.target_fit = list();

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
				self.seeds.append(pop[arr[0] + str(count)]);
			elif arr[0] == "Fitness":
				pop[arr[0]+str(count)] = arr[2];
				self.target_fit.append(int(arr[2]));
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
	def separate_chromosomes(self, pop, size):
		i = 1;
		tries = 0;
		#for each chromosome in the population, create initial structure
		#pass in a dictionary of locations
		while i<size:
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

	# create 200 randomly generated chromosomes from the same seed
	def generate_pop(self, index, size):
		seed = self.seeds[index];
		pop = list();
		tries = 0;
		i = 0;
		while i<size:
			temp = self.initial_directions(seed);
			tries+=1;

			if len(temp) == len(seed):
				temp = {**{"fit":"0"}, **temp }
				pop.append(temp);
				print("Member:"+str(i+1)+"Random attemps: "+str(tries));
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
			bad_neighborhood = {};
			dir_list = self.random_four();
			previous = location; 
			#check for bad areas that will cause dead ends
			bad_neighborhoods = self.check_neighbors(temp,location);
			for i in range(len(dir_list)):
		 		#convert into string location based on randomly generated direction
				location = self.check_direction(dir_list[i], previous, k);
		 		#check if location is valid				
				if location in seq_dict or location in bad_neighborhood:
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
		

	#help minimize bad layouts by checking area for dead ends
	def check_neighbors(self, pop, start):
		block = self.increment_directions(start);
		nb = list();
		bad_address = {};

		if pop is None:
			bad_address["0,0"]=0;
			return bad_adress;

		for i in range(4):
			nb = self.increment_directions(block[i]);
			if block[i] in pop:
				bad_address[block[i]] = 0;
			# check right, up and down
			elif i == 0 and self.check_neighborhood(pop,nb[0],nb[2],nb[3]):  #going right
				bad_address[block[i]] = 0;
			# check left, up, down
			elif i == 1 and self.check_neighborhood(pop,nb[1],nb[2],nb[3]):  #going left
				bad_address[block[i]] = 0;
			# check up, right, left
			elif i == 2 and self.check_neighborhood(pop,nb[0],nb[1],nb[2]):  #going up
				bad_address[block[i]] = 0;
			# check down, right, left
			elif i == 3 and self.check_neighborhood(pop,nb[0],nb[1],nb[3]):  #going down
				bad_address[block[i]] = 0;
		return bad_address;

	#check 2 spaces out for dead ends
	def check_neighborhood(self,pop,loc1,loc2,loc3):
		if loc1 in pop and loc2 in pop and loc3 in pop:
			return True;
		return False;

	#returns all four coords from given location as a list
	#order: right, left, up, down
	def increment_directions(self, loc):
		temp = list()
		a= loc.split(",");
		temp.append( str(int(a[0])+1)+","+str(a[1]));
		temp.append( str(int(a[0])-1)+","+str(a[1]));
		temp.append( str(a[0])+","+str(int(a[1])+1)); 
		temp.append( str(a[0])+","+str(int(a[1])-1));
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
		temp = [1,2,3,4];
		r.shuffle(temp);
		return temp;


class fitness_generator:
	"""
		fitness_generator class is responsible for mutating the population
		gathered from the data_input class, in such a way to find the 
		patterns for lowest energy
	"""
	def __init__(self, data_obj):
		#set a reference to the data object
		self.pinnacle = {};
		self.pop1 = None;
		self.pop2 = None;
		self.generation = 0;
		self.max_fit = 0;
		self.target_fit = 0;
		self.chrom_size = 0

	# reset variables for next use
	def reset(self):
		self.pop1 = None;
		self.pop2 = None;
		self.generation = 0;
		self.max_fit = 0;
		self.target_fit = 0;

	# get initial pop in form of list of dictionaries
	# pop[0] {"fit":"0","0,0":"h","0,1":"p"...}
	def set_init_pop(self, pop):
		self.pop1 = pop;
		self.chrom_size = len(pop);
		
	def set_target_fitness(self, fit):
		self.target_fit = fit;

	# create a given number of sequence randomly generated chromosomes from one seed 
	def write_initial_pop_to_file(self):
		pass;

	def run_generations(self):
		# find the fitness of each chromosome
		self.rank_generation();
		# Sort fitness from high to low
		self.sort_generation();
		# move pop1 into pop2
		# cross over 80% of pop (160)
		# self.crossover_generation();
		# fill 10% with elite pop and 10% random selection
		self.random_selection();
		# mutate random selection from 5%-50%
		# self.mutate_generation();
		# self.generation +=1;
		self.print_to_console();
		

	# rank each
	def rank_generation(self):
		for i in range(len(self.pop1)):
			conn = self.track_connections(self.pop1[i])
			fit =self.calculate_fitness(self.pop1[i],conn);
			self.pop1[i]["fit"] =fit;
			#examine exit fitness levels
			if fit > self.max_fit:
				self.max_fit = fit;
			if self.max_fit >= self.target_fit:
				# exit calculations and move target structure to top
				pass;

	# sort generation from highest to lowest fitness
	def sort_generation(self):
		count = 0;
		#bubble sort for ease of coding: refactor if needed
		for i in range(len(self.pop1)):
			if i != len(self.pop1)-1:
				if int(self.pop1[i]["fit"]) < int(self.pop1[i+1]["fit"]):
					temp = self.pop1[i+1]["fit"];
					self.pop1[i+1]["fit"] = self.pop1[i]["fit"]
					self.pop1[i]["fit"] = temp;
					count+=1;
		if count > 0:
			self.sort_generation();

	# direclty copy chromosomes from pop1 to pop2
	def random_selection(self):
		#insert top 10% of chromosomes into pop2
		for i in range(int(len(self.pop1)*0.1)):
			self.pop2.append(self.pop1[i]);
		# randomly insert 10% of chromosomes
		for j in range(int(len(self.pop1)*0.1)):
			ran = r.randint(0,len(self.pop1)-1);
			self.pop2.append(self.pop1[ran]);

	# crossover 80% of chromosomes
	def crossover_generation(self):
		for i in range(int(len(self.pop1)*0.8)):
			ran1 = r.randint(0,len(self.pop1)-1);
			ran2 = r.randint(0,len(self.pop1)-1);
			#gain 2 random unique indexes
			if ran1 != ran2:
				cross_index = r.randint(len(self.pop[ran2])-1);
				self.crossover(self.pop1[ran1], self.pop1[ran2], cross_index);

	# break each chromosome into parts for crossing over
	def crossover(self, chrom1, chrom2,cross_index):
		# seg_a = list(); #hold the moving segment for cross over
		# body_a = {};  #hold the static section for cross over
		# seg_b = list(); #hold the moving segmen for 2nd chrom
		# body_b ={}; #hold the static section for 2nd chrom
		seg_a, body_a, key_a = self.split_chormosome(chrom1, cross_index);
		seg_b, body_b, key_b = self.split_chormosome(chrom2, cross_index);
		chrom1 = self.combine_chrom_segments(seg_a, body_b, key_b);
		chrom2 = self.combine_chrom_segments(seg_b, body_a, key_a);

	#split a chromosome into 2 pieces
	#returns segment in form of 0 ["0,0,h","0,1,p"]
	def split_chormosome(self, chrom, cross_index):
		seg_temp = list();
		body_temp = {};
		key = "";
		count = 0;
		for k,v in chrom:
			# load the smaller sections exclude fit attribute
			if count <= cross_index and k != "fit":
				seg_temp.append(k+","+v):
			elif k != "fit":
				body_body[k] = v;
				if count == cross_index+1:
					key = k;
			count+=1;
		return seg_temp, body_temp, key;

	# join a chromosome segment and body together to create a new chromosome
	def combine_chrom_segments(self, seg, body, key):
		# set the connection to be a random direction
		merged = None;
		directions = [1,2,3,4];
		r.shuffle(directions);
		start = self.move_rand_loc(key, directions[0]);
		compatible = False;
		merged = {};
		x,y = self.find_seg_body_distance(seg, start);
		# update each location in segment by distance in new x,y coord
		temp_seg = self.set_seg_locations(seg, x, y);
		#check if new location overlaps a
		combined = self.check_overlap(temp_seg, body);
		if combined:
			merged = self.merge_sections(temp_seg, body);
		else:
			for i in range(1,4):
				#change to next direction in the list
				start = self.move_rand_loc(key, direction[i]);
				#find the new coordinate distance
				x,y = self.find_seg_body_distance(seg, start);
				#set temp to new coordinates 
				temp_seg = self.set_seg_locations(seg,x,y);
				#rotate coord 90 degrees right
				temp_seg_rotate = self.self.rotate_seg(temp_seg,rotate_dir[j]);
				#check if the new pair can combine without overlap
				combined = self.check_overlap(temp_seg_rotate, body);
				if combined:
					merged = self.merge_sections(temp_seg_rotate, body);
					break;
		return merged; 

	def rotate_seg(self, seg, degrees):
		pass;

	# find the distance to move each x,y in seg based on a starting position
	def find_seg_body_distance(self, seg, start):
		# Find the difference in x coord locations from seg to body as var x
		Ax = int(seg[len(seg)-1][0]);
		Bx = int(start[0]);
		x = Ax - Bx;
		# Find the difference in y coord locations from seg to body as var y
		Ay = int(seg[len(seg)-1][2]);
		By = int(start[2]);
		y = Ay - By;
		return x,y;
		
	# change the locations of a list segment by a distance x,y
	# seg int the form of ["0,0,p","0,1,h",...]	
	def set_seg_locations(self, seg, x, y):
		for i in range(len(seg)):
			arr = seg[i].split(",");
			seg[i] = str(int(arr[0])+x)+","+str(int(arr[1]+y)) + ","+ seg[i][-1:];

	# check if a segment's elements locations overlap the static body
	# return true if compatible
	# seg int the form of ["0,0,p","0,1,h",...]	
	# body in the form of {"0,0":"h","0,1":"p"...}
	def check_overlap(self,seg, body):
		compatible = True;
		for i in range(len(seg)):
			# omit the last 2 chars: ',h' or ',p'
			key = seg[i][:-2];
			if key in body:
				compatible = False;
				break;
		return compatible;


	# merge a compatible segment to a body to make a new chromosome
	# seg in form: ["0,0,p","0,1,h"...]
	# body in form: {"0,0":"h","1,0":"p"...}
	def merge_sections(self, seg, body):
		chromosome = {};
		# always insert segment first
		for i in range(len(seg)):
			# change to form: {"0,0":"h"}
			chromosome[seg[i][:-2]] = seg[i][-1:];
		for k,v in body.itmes():
			chromosome[k] = v;
		return chromosome;


	def crossover_mutation(self, top, bottom):
		pass;



	# returns a new random direction 1: right, 2: left, 3: up, 4: down
	# loc must be in the form: "0,0"
	# direction num 1 to 4
	def move_rand_loc(self, loc, direction=0):
		if direction == 0:
			temp = r.randint(4);
		else:
			temp = direction;
		arr = loc.split(",");
		if temp == 1:
			loc = str(int(arr[0])+1)+","+str(arr[1]);
		elif temp == 2:
			loc = str(int(arr[0])-1)+","+str(arr[1]);
		elif temp == 3;
			loc = str(arr[0])+","+str(int(arr[1]+1));
		else:
			loc = str(arr[0])+","+str(int(arr[1]-1));
		return loc;


	# used for debugging
	def print_to_console(self):
		for i in range(len(self.pop1)):
			print(self.pop1[i]);


	# create a temp list to house each chromosomes path
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
		# check for connections
		for k,v in pop.items():
			if v == "h":
				arr = k.split(",");
				# check locations up down left right for adjacency
				fit += self.match_locations((str(int(arr[0]))+","+str(int(arr[1])+1)), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0]))+","+str(int(arr[1])-1)), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0])-1)+","+str(int(arr[1]))), pop, k, count, conn);
				fit += self.match_locations((str(int(arr[0])+1)+","+str(int(arr[1]))), pop, k, count, conn);
				# print("Fit: "+str(fit)+" count: "+str(count))
			count+=1;
		#return fitness to compare to previous fitness 
		return int(fit/2);

	# directly index heap for O(1) look up
	def match_locations(self, direct, pop, k, count, connections):
		fitness = 0;

		try:
			# print("count: "+str(count)+" loc: "+direct+" v at loc: "+pop[direct])
			# location exist in chromosome and == p
			if pop[direct] == "h":
				if count == 0 and connections[count+1] != direct:
					fitness+=1;
					# if the index+1 is in bounds and the direction is not directly connected
				elif count == len(connections)-1 and connections[count-1] != direct:
					fitness+=1;
				elif connections[count+1] != direct and connections[count-1] != direct:
					fitness+=1;
		except KeyError:
			pass;
		print(str(fitness));
		return fitness;




# should be fitness -9;  Example from slides
temp = {"0,0":"h", "1,0":"p", "1,1":"h", "1,2":"p", "0,2":"p", "0,1":"h", "-1,1":"h", "-1,2":"p", "-2,2":"h", "-3,2":"p", "-3,1":"p",
			"-2,1":"h", "-2,0":"p", "-1,0":"h", "-1,-1":"h", "-2,-1":"p", "-2,-2":"p", "-1,-2":"h", "0,-2":"p", "0,-1":"h"};

f = fitness_generator(temp);





