from GeneticAlg import model;

class view_controller:

	def __init__(self):
		self.model = model();
		self.pop_size = 0;

	#invoke data processing logic
	def load_file(self, file_name):
		#need to include some exception handling here
		self.model.setup_data(file_name);
		self.prep_data_for_view();

	# package data to send to view
	def prep_data_for_view(self):
		self.pop_size += model.pop_size;
		self.fitness = list();
		self.length = list();
		for i in range(self.pop_size):
			# package fitness of each chromosome for display
			self.fitness.append("Fitness:  --/"+str(model.chromosomes["fitness"+str(i+1)]));
			# package chromosome length for display
			self.length.append("Monomers: "+str(model.chromosome_length[i]));

	# package data to send to view
	def display_data(self, index):
		string =" ";
		try:
			string = self.length[index]+"\n";
			string += self.fitness[index]+"\n";
			string += "Chromosome: "+str(index+1)+":"+str(self.pop_size)
		except IndexError:
			pass;
		return string;


		