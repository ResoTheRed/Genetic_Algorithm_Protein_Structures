from GeneticAlg import model;

class view_controller:

	def __init__(self):
		self.model = model();

	#invoke data processing logic
	def load_file(self, file_name):
		#need to include some exception handling here
		self.model.setup_data(file_name);
		