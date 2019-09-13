"""
	This class is designed to pull the data from the Model and package it in such a way 
	that it can easily be uploaded into the view.  It is also responsible for pulling 
	request/data from the view and submitting it to the Model.

	Model --> View
		1. Initial protien structure to canvas (data to model to view)
			form of a dictionary {"0,0":"h",...}
		2. Best protein structure to canvas (fitness_generator to model to view)
			form of a dictionary {"0,0":"h",...}
		3. monomer length, fitness, pop_size, random%, elite%, crossover% and Chromosome number to display text box
			Form of a string
	View --> Model
		1. Elite %
		2. Random %
		3. Crossover %
		4. Plateau range
		5. Population size
		6. current index 

"""

from GeneticAlg import model

class view_controller:

	def __init__(self):
		self.model = model()
		self.pop_size = 1
		self.model.set_view_controller(self)
		self.display_string = ""


	def set_view(self, view):
		self.view = view

	def set_pop_size(self, size):
		self.pop_size = size

	def get_pop_size(self):
		return self.pop_size

	#invoke data processing logic and set up initial states
	def load_file(self, file_name):
		try:
			# load in the input file and generate initial stats
			self.model.setup_data(file_name)
			# find the number of chromosomes 
			self.pop_size = self.model.data.pop_size
			self.setup_variables()
		except IOError:
			pass

	# create all of the lists that will hold each chromosomes data
	def setup_variables(self):
		# used to hold the fitness given by the user for each chrom
		self.target_fitness = []
		for i in range(self.pop_size):
			self.target_fitness.append(str(self.model.data.chromosomes["Fitness"+str(i+1)])) 
		# used to hold the fitness of each chromosome by the alg
		self.found_fitness = ["--" for i in range(self.pop_size)]
		# used to store the original sequence from input
		# for k,v in self.model.data.get_seeds().items():
		# self.seeds = self.model.data.get_seeds()
		# used to hold the number of nodes in each chromosome
		self.length = []
		for i in range(self.pop_size):
			self.length.append("19")
		# used to hold the population size used for alg
		self.pop = ["1" for i in range(self.pop_size)]
		# used to hold the % elite picked for each gen of each chromosome
		self.elite = ["10" for i in range(self.pop_size)]
		# used to hold the random picked for each gen of each chromosome
		self.rand = ["10" for i in range(self.pop_size)]
		# used to hold crossover/mutation rate for each chromosome
		self.crossover = ["80" for i in range(self.pop_size)]
		# used to hold the number of generations it took to 
		self.generations = ["1" for i in range(self.pop_size)]
		# used to hold the platfitness plateau for each chromosome
		self.plateau = ["10" for i in range(self.pop_size)]
		# used to hold all of the protein structures for each chromosome
		# initially will be the default structure and replaced by the new
		self.structure = []
		for i in range(self.pop_size):
			try:
				temp = self.model.data.chromosomes["Seq"+str(i+1)]
				self.structure.append(temp)
			except KeyError:
				self.structure.append({"0,0":"n"})

	# package data from a series of lists to send to view as a string
	def display_data_textbox(self, index):
		string ="Error loading data"
		dst = 20
		try:
			s1 = "~Chromosome Stats~\n"
			s2 = "Monomers: "+ self.length[index-1]
			s2 = s2.ljust((dst - len(s2))+len(s2)) 
			s2 +="Elite: "+ self.elite[index-1]+"\n"
			s3 = "Fitness: "+ self.found_fitness[index-1]+"/"+self.target_fitness[index-1]
			s3 = s3.ljust((dst - len(s3))+len(s3))
			s3 += "Random: "+ self.rand[index-1]+"\n"
			s4 = "Population: "+self.pop[index-1] 
			s4 = s4.ljust((dst - len(s4))+len(s4))
			s4 += "Crossover: " +self.crossover[index-1]+"\n"
			s5 = "Generation: "+self.generations[index-1]
			s5 = s5.ljust((dst - len(s5))+len(s5))
			s5 += "Plateau: "+ self.plateau[index-1]+"\n"
			s6 = "Chromosome: "+str(index)+" of "+str(self.pop_size)
			# string += "Seq: " + str(self.seeds[index-1])
			string = s1+s2+s3+s4+s5+s6
		except IndexError:
			pass
		self.display_string = string

	def update(self, index):
		self.display_data_textbox(index)
	
	# returns the dictionary of data for a specific index
	def get_structure(self, index):
		# needs exception handling here
		try:
			# return the best chromosome if found else the default
			# indexes should be one less for array access
			if self.model.check_for_struct(str(index-1)):
				chromo = self.model.get_fit_chrom(str(index-1))
				temp = {}
				for k,v in chromo.items():
					# record the fitness found by the alg
					if k == "fit":
						self.found_fitness[index-1] = "-"+str(v)
					else:
						temp[k] = v
				# update generations to reflect run
				self.generations[index-1] =  str(self.model.fitness.get_generations())
				self.structure[index-1] = temp  
		except KeyError:
			pass

	

	def loading_signal_from_data(self):
		pass
		#self.view.load()

	def find_fitness(self, index):
		self.model.find_fitness(index-1)


vc = view_controller()
vc.load_file("input2.txt")
print("Inside the vc")
vc.display_data_textbox(1)
print(vc.display_string)
print(str(vc.structure[0]))
vc.find_fitness(1)
vc.get_structure(1)
print(str(vc.structure[0]))
vc.update(1)
vc.display_data_textbox(1)
print(vc.display_string)