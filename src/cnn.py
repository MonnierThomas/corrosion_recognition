import os
from tensorflow.keras import optimizers, layers
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

train = "" # training path
valid = "" # validation path
test = ""  # test path 1
test2 = "" # test path 2
save = "26"

# Model's parameters
batch_size = 20
IMG_HEIGHT, IMG_WIDTH = 256, 256
total_val = 166
epochs = 20
total_train = 699

def data_preparation(train = train, valid = valid):
	"""Formats the image into appropriately pre-processed floating point tensors before feeding them to the neural network"""

	train_image_generator = ImageDataGenerator(rescale=1)
	train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															   directory=train,
															   shuffle=True,
															   target_size=(IMG_HEIGHT, IMG_WIDTH),
															   class_mode='categorical')
	valid_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															   directory=valid,
															   shuffle=True,
															   target_size=(IMG_HEIGHT, IMG_WIDTH),
															   class_mode='categorical')
	print()
	return train_data_gen, valid_data_gen


def model_creation():
    """Calculates the model using Keras' CNN"""

    model = Sequential()
    
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))
    model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())

    model.add(Dense(64, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(2, activation='softmax'))


    EDCE = optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)

    model.compile(optimizer=EDCE,
				  loss='categorical_crossentropy',
				  metrics=['accuracy'])
    return model


def model_training(model, train_data_gen, valid_data_gen):
	"""Trains the model"""

	history = model.fit_generator(train_data_gen,
								steps_per_epoch=total_train // batch_size,
								epochs=epochs,
								validation_data=valid_data_gen,
								validation_steps=total_val // batch_size)
	accu = model.evaluate_generator(train_data_gen)
	print(accu)

	return history

def model_saving(model, save = save):
	"""Saves the model"""

	model_json = model.to_json() # serialize model to JSON
	with open("model.json", "w") as json_file:
		json_file.write(model_json)
	
	model.save_weights(save+"model.h5") # serialize weights to HDF5
	print("Saved model to disk")


def model_loading(save = save):
	"""Loads the model"""

	json_file = open('model.json', 'r') # load json and create model
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	
	loaded_model.load_weights("model.h5") # load weights into new model
	print("Loaded model from disk")
	return loaded_model

def prediction(model, test = test):
	"""Outputs predictions after testing the trained model"""
	test_image_generator = ImageDataGenerator(rescale=1)
	test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
														  directory=test,
														  shuffle=False,
                                                          target_size=(IMG_HEIGHT, IMG_WIDTH),
														  class_mode='categorical')
	predic = model.predict_generator(test_data_gen, 
									 steps=None, 
									 callbacks=None, 
									 max_queue_size=10, 
									 workers=1, 
									 use_multiprocessing=False, 
									 verbose=1)
	accu = model.evaluate_generator(test_data_gen)
	print(accu)
	return predic, test_data_gen


def conf_matrix(predic, classes):
	"""Returns the confusion matrix"""
	pred = [np.argmax(i) for i in predic]
	cm = confusion_matrix(classes, pred)
	return cm


def info_plotting(cm, history):
	"""Plots model's accuracy and loss, as well as the confusion matrix"""
	fig, ax = plt.subplots()
	print(cm)
	im = ax.imshow(cm, interpolation='nearest', cmap = plt.cm.Blues)
	ax.figure.colorbar(im, ax=ax)
	plt.show()
	
	# Plots training and validation accuracies
	plt.plot(history.history['accuracy'])
	plt.plot(history.history['val_accuracy'])
	plt.title('Model accuracy')
	plt.ylabel('Accuracy')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Validate'], loc='lower right')
	plt.show()


	# Plots training and validation losses
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('Model loss')
	plt.ylabel('Loss')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Validate'], loc='lower right')
	plt.show()


def predict_test(test_path=test):
    """Predicts a test batch and returns the confusion matrix"""
    test_image_generator = ImageDataGenerator(rescale=1)
    model = model_loading()
    test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
														  directory=test_path,													  
														  class_mode='categorical',
                                                          target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                          shuffle=False)
    predic = model.predict(test_data_gen, 
									 steps=None, 
									 callbacks=None, 
									 max_queue_size=10, 
									 workers=1, 
									 use_multiprocessing=False, 
									 verbose=1)
    cm = conf_matrix(predic, test_data_gen.classes)
    fig, ax = plt.subplots()
    print(cm)
    im = ax.imshow(cm, interpolation='nearest', cmap = plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    plt.show()
    return 0


def predict_non_test(test_path = test2):
    """Predicts an unknown test"""
    l = model_loading()
    train_image_generator = ImageDataGenerator(rescale=1)
    test_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															 directory=test2,
															 shuffle=True,
															 target_size=(IMG_HEIGHT, IMG_WIDTH),
															 class_mode='categorical')
    predic = l.predict_generator(test_data_gen, 
									 steps=None, 
									 callbacks=None, 
									 max_queue_size=10, 
									 workers=1, 
									 use_multiprocessing=False, 
									 verbose=1)
    return predic


if __name__ == '__main__' :
    global history
    train_data_gen, valid_data_gen = data_preparation()
    model = model_creation()
    history = model_training(model, train_data_gen, valid_data_gen)
    model.summary()
    model_saving(model)
    predic, test_data_gen = prediction(model)
    cm = conf_matrix(predic, test_data_gen.classes)
    info_plotting(cm, history)
    print(predic)