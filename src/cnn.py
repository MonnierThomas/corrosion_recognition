import os
from tensorflow.keras import optimizers, layers
from tensorflow.keras.models import Sequential, model_from_json
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

train_dir = "" # Chemin des images d'entraînement
valid_dir = "" # Chemin des images de validation
test_dir = ""  # Chemin des images de test
test_dir2 = "" # Chemin des images de test 2
save_dir = "26"

# Forme et propriétés du modèle utilisé
batch_size = 20
IMG_HEIGHT, IMG_WIDTH = 256, 256
total_val = 166
epochs = 20
total_train = 699

def data_preparation(train_dir = train_dir, valid_dir = valid_dir):
	"""Formate l'image en tenseurs à virgule flottante pré-traités de manière appropriée avant de les alimenter sur le réseau de neurones"""
	train_image_generator = ImageDataGenerator(rescale=1)
	train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															   directory=train_dir,
															   shuffle=True,
															   target_size=(IMG_HEIGHT, IMG_WIDTH),
															   class_mode='categorical')
	valid_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															   directory=valid_dir,
															   shuffle=True,
															   target_size=(IMG_HEIGHT, IMG_WIDTH),
															   class_mode='categorical')
	print()
	return train_data_gen, valid_data_gen


def model_creation():
    """Calcule le modèle à l'aide du CNN de Keras"""
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
	"""Entraîne le modèle"""

	history = model.fit_generator(train_data_gen,
								steps_per_epoch=total_train // batch_size,
								epochs=epochs,
								validation_data=valid_data_gen,
								validation_steps=total_val // batch_size)
	accu = model.evaluate_generator(train_data_gen)
	print(accu)

	return history

def model_saving(model, save_dir = save_dir):
	"""Sauvegarde le modèle"""

	model_json = model.to_json() # serialize model to JSON
	with open("model.json", "w") as json_file:
		json_file.write(model_json)
	
	model.save_weights(save_dir+"model.h5") # serialize weights to HDF5
	print("Saved model to disk")
	return 0


def model_loading(save_dir = save_dir):
	"""Charge le modèle"""

	json_file = open('model.json', 'r') # load json and create model
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	
	loaded_model.load_weights("model.h5") # load weights into new model
	print("Loaded model from disk")
	return loaded_model

def prediction(model, test_dir = test_dir):
	"""Test le précédent modèle entraîné et retourne les prédictions en probabilités"""
	test_image_generator = ImageDataGenerator(rescale=1)
	test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
														  directory=test_dir,
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
	"""Retourne la matrice de confusion"""
	pred = [np.argmax(i) for i in predic]
	cm = confusion_matrix(classes, pred)
	return cm


def info_plotting(cm, history):
	"""Trace la précision du modèle et la matrice de confusion"""
	fig, ax = plt.subplots()
	print(cm)
	im = ax.imshow(cm, interpolation='nearest', cmap = plt.cm.Blues)
	ax.figure.colorbar(im, ax=ax)
	plt.show()
	
	# Trace les valeurs de précision d'entraînement et de validation
	plt.plot(history.history['accuracy'])
	plt.plot(history.history['val_accuracy'])
	plt.title('Model accuracy')
	plt.ylabel('Accuracy')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Validate'], loc='lower right')
	plt.show()


	# Trace les valeurs de perte d'entraînement et de validation
	plt.plot(history.history['loss'])
	plt.plot(history.history['val_loss'])
	plt.title('Model loss')
	plt.ylabel('Loss')
	plt.xlabel('Epoch')
	plt.legend(['Train', 'Validate'], loc='lower right')
	plt.show()

	return 0


def main ():
    global history
    train_data_gen, valid_data_gen = data_preparation()
    model = model_creation()
    history = model_training(model, train_data_gen, valid_data_gen)
    model.summary()
    model_saving(model)
    predic, test_data_gen = prediction(model)
    cm = conf_matrix(predic, test_data_gen.classes)
    info_plotting(cm, history)
    return (predic)


def predic_test(test_path=test_dir):
    """Prédiction d'un batch de test et retourne la matrice de confusion"""
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
    return(0)


def predic_non_test(test_path = test_dir2):
    """Prédiction d'un batch inconnu"""
    l = model_loading()
    train_image_generator = ImageDataGenerator(rescale=1)
    test_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
															 directory=test_dir2,
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
    return(predic)


