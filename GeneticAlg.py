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
		pass;

	#gain a referance to the input data
	def setup_data(self, file_name):
		self.data = data_input(file_name);


class data_input:

	#data_input constructor
	def __init__(self, file_name):
		pop = self.unpack_from_file(file_name);
		self.chromosomes = self.separate_chromosomes(pop);
		#self.separate_chromosomes(pop);



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
			
			if len(temp) == self.chromosome_length[i-1]:
				pop["Seq"+str(i)] = temp;
				print("Random attemps: "+str(tries));
				# print(str(temp));
				i+=1;
				tries = 0;
		print(str(pop));
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


#di = data_input("Input.txt");

"""
location and sequence
0[{"0,0,":'h', "0,1":"p", "1,1":'h'}]
1[{}]
"""