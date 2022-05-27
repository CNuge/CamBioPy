import pickle
import numpy as np
import tensorflow as tf

#these ones for the Autoencoder class
from tensorflow.keras import layers, losses
from tensorflow.keras.models import Model

class Autoencoder(Model):
	def __init__(self, latent_dim, in_shape = (28, 28),):
		super(Autoencoder, self).__init__()
		self.latent_dim = latent_dim	 
		self.dense_shape = 1 
		for x in in_shape:
			self.dense_shape = self.dense_shape * x
		print(f"dense_shape: {self.dense_shape}")
		
		self.encoder = tf.keras.Sequential([
			layers.Flatten(),
			layers.Dense(latent_dim, activation='relu'),
		])
		
		self.decoder = tf.keras.Sequential([
			layers.Dense(self.dense_shape, activation='sigmoid'),
			layers.Reshape(in_shape)
		])

	def call(self, x):
		encoded = self.encoder(x)
		decoded = self.decoder(encoded)
		return decoded


if __name__ == '__main__':
	
	#pickle allows for complex data in columns
	# pandas.read_csv otherwise fine
	data = pickle.load(open('data_in.pkl', 'rb'))

	#shuffle the data,
	data = data.sample(frac=1).reset_index(drop=True)

	#simplified data split, 30% for autoencoder, 50% for model training, 20% for testing
	# could use sklearn to do this more elegantly, or in stratified fashion.
	auto, train, test = (data[:int(len(data)*.3)], 
										data[int(len(data)*.3):int(len(data)*.8)], 
										data[int(len(data)*.8):])

	"""
	## if large, may want to save here.
	pickle.dump(auto, open("auto_inputs.pkl", "wb"))
	pickle.dump(train, open("train_inputs.pkl", "wb"))
	pickle.dump(test, open("test_inputs.pkl", "wb"))
	"""


	###################
	#get the autoencoder data split
	auto_train, auto_test = auto[:int(len(auto)*0.8)], auto[int(len(auto)*0.8):]

	#make data floating point!
	print("if data from across several columns, not nested in one, then change this list comprehension")
	x_auto_train = np.array([x for x in auto_train.data_column.values])
	x_auto_train = x_auto_train.astype('float32') 

	x_auto_test = np.array([x for x in auto_test.data_column.values])
	x_auto_test = x_auto_test.astype('float32') 

	##################
	#train the autoencoder

	print("4000bp window example")
	in_shape = (4 , 4000, 1)

	print("distilling down to 200 numbers")
	latent_dim = 200

	autoencoder = Autoencoder(latent_dim = latent_dim, in_shape = in_shape)

	autoencoder.compile(optimizer='adam', loss=losses.MeanSquaredError())

	autoencoder.fit(x_auto_train, x_auto_train,
					epochs=1000,
					shuffle=True,
					validation_data=(x_auto_test, x_auto_test))

	autoencoder.save("autoencoder_model")
	###################


	###################
	print("autoencode data for predicitve model")

	X_train_raw = np.array([x for x in train.data_column.values])
	X_train_raw = X_train_raw.astype('float32') / 255.
	X_train = autoencoder.encoder(X_train_raw).numpy()

	X_test_raw = np.array([x for x in test.data_column.values])
	X_test_raw = X_test_raw.astype('float32') / 255.
	X_test = autoencoder.encoder(X_test_raw).numpy()
	###################


	## can then dump those for use in a model 
	## y values undefined, would work for classifier or regressor.
	#pickle.dump(X_train, open("X_train.pkl", "wb"))
	#pickle.dump(X_test, open("X_test.pkl", "wb"))
