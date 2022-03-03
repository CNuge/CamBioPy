from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def make_dnn_regressor(in_shape = 10, 
						hidden_sizes = [24,48,96,192,96,48,24,12], 
						dropout = 0.2):

	#initiate the model
	model = Sequential()
	#specify the in layer, denoting size
	model.add(layers.Dense(in_shape, input_shape=(in_shape,) , activation = 'relu'))

	n_hidden = len(hidden_sizes)

	for i in range(0,n_hidden):
		model.add(layers.Dense(hidden_sizes[i], activation = 'relu'))
		if dropout != 0:
			model.add(layers.Dropout(dropout))

	model.add(layers.Dense(1, kernel_initializer='normal',activation='linear'))

	# Compile the network :
	model.compile(loss='mean_absolute_error', 
					optimizer='adam', 
					metrics=['mean_absolute_error'])

	return model
	


def make_dnn_classifier(hidden_sizes = [24,48,96,192,96,48,24,12], dropout = 0.2,
						in_shape = 310, n_classes = 2, load_weights = False):
	"""

	Arguments
	---------
	hidden_sizes - neuron sizes for the hidden layers
				n_hidden is implict param - equal to the length of hidden layers list
	dropout : float, fraction of dropout applied after each hidden layer, for no dropout pass 0.
		Default is 0.3. 
	in_shape : int, the number of predictor variables, assumes 1d inputs. 
		Default is 256 (4mer size).
	n_classes - int, the number of output classes. Default is 5 (kingdoms).

	Returns
	---------
	out : a tensorflow sequential neural network.

	"""

	#initiate the model
	model = Sequential()
	#specify the in layer, denoting size
	model.add(layers.Dense(100, input_shape=(in_shape,) , activation = 'relu'))

	n_hidden = len(hidden_sizes)

	for i in range(0,n_hidden):
		model.add(layers.Dense(hidden_sizes[i], activation = 'relu'))
		if dropout != 0:
			model.add(layers.Dropout(dropout))


	model.add(layers.Dense(n_classes, activation = 'softmax'))

	model.compile(loss = 'sparse_categorical_crossentropy', 
						optimizer = 'adam', 
						metrics = ['accuracy'] )

	if load_weights != False:
		model.load_weights(load_weights)

	return model
