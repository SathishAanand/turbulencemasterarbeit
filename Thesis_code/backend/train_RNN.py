#!/usr/bin/env python3
# =====================================================================================
# LES Turbulence Modelling (31.3.2020)
#
# Description:
#
#
# =====================================================================================
 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Reduce annoying tf output (default: 0)
import sys
import glob
import h5py
import time
import numpy as np
from sklearn.cluster import KMeans
import tensorflow as tf
from shutil import copyfile
import json
from keras import backend as K
#import umap

import matplotlib.pyplot as plt
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
#import plotly
#import plotly.express as px 
#import shap
#tf.compat.v1.disable_v2_behavior()

#from ann_visualizer.visualize import ann_viz;

from sklearn.inspection import permutation_importance


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Model

from tensorflow.keras.utils import plot_model
from tensorflow.keras.layers import Input, Dense, BatchNormalization
#from IPython.core.display import Image

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.manifold import MDS

# Read-In
from tools import *
from output import *
from metrics import weighted_mse_loss, correlation_coefficient_metric
from read_flexi import getDataset
import datamanipulation.jsonexport as dtm 
from randomvalues import setSeeds

import random
random.seed(101)

randomStatePCA=99
randomStateTSNE = 42
randomseed=101
perplexityTSNE = 100
print("Random seed: {}".format(randomseed))
#setSeeds(randomseed)
dtm.setExportDir("rnn_" + str(randomseed))
# =====================================================================================
# User input
# =====================================================================================
print("tensorflow:{}".format(tf.__version__))
#print("SHAP version is:", shap.__version__)
#print("keras:{}".format(keras.__version_))
# Input files
#for 3 timesteps random e-3
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-4]0[0-2][0]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.40[0-2][0]0*.h5")
#for 3 timesteps e-4
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-4]00[0-2]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.400[0-2]0*.h5")
#for 5 timesteps random
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-4]0[0-1][0-1]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.40[0-2][0-1]0*.h5")
#for 5 timesteps
trainFiles = glob.glob("/home/balasush/scratch/users/sathish/turbulence/train/DG_data/*run10[1-5]*State*1.[0-5]00[0-4]0*.h5")
testFiles  = glob.glob("/home/balasush/scratch/users/sathish/turbulence/train/DG_data/*run100*State*1.400[0-4]0*.h5")

#for 10 timesteps random
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-4]0[0-1][0-4]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.40[0-1][0-4]0*.h5")

#for 10 timesteps
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-4]00[0-9]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.400[0-9]0*.h5")
#for 21 timesteps
#trainFiles = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run10[1-4]*State*1.[0-1]0[0-1][0-9]0*.h5")
#testFiles  = glob.glob("/content/drive/MyDrive/Colab Notebooks/MA-Aanand-Turbulence-master/train/21_timesteps/*run100*State*1.40[0-1][0-9]0*.h5")

#f = open('/content/drive/MyDrive/user.json',"r")
#data = (json.loads(f.read()))

# Debug Output
debug = 2              # [0,1,2] Amount of debug output written to console
writePredFile = True   # Write prediction on test set to hdf5 file

# Information on input sequence
# for 3 timesteps previous data +random
#dt          = 1.e-3 # time increment between files
#seqLength   = 3     # total number of files per sequence
# for 3 timesteps new data
#dt          = 1.e-4 # time increment between files
#seqLength   = 3     # total number of files per 
# for 5 timesteps random data
#dt          = 1.e-3 # time incfilesrement between 
#seqLength   = 5     # total number of files per sequence
# for 5 timesteps new data
dt          = 1.e-4 # time incfilesrement between 
seqLength   = 5     # total number of files per sequence
# for 10 timesteps random
#dt          = 1.e-3 # time increment between files
#seqLength   = 10     # total number of files per sequence
# for 10 timesteps
#dt          = 1.e-4 # time increment between files
#seqLength   = 10     # total number of files per sequence
# for 20 timesteps
#dt          = 1.e-4 # time increment between files
#seqLength   = 20     # total number of files per sequence#
CellPoints  = 6     # poly. degree of training data

inputseqinfo=[seqLength,dt]
inputseq=np.array(inputseqinfo)
dtm.addForExport( inputseq[0], "seqlength")
dtm.addForExport( inputseq[1], "time_increment")


# Model name
modelName = 'res0'  # Used for generated output files
modelNumb = 1       # Will be attached to modelName for output

# Model restart
doRestart   = False                        # restart from already trained model
restartPath = os.path.abspath('./model/')  # path to model to restart from
initial_epochs = 0   # Epoch number at which the model is restarted (needed for e.g. lr)

# Model saving
doSave   = True                            # save model
savePath = os.path.abspath('./model/')     # folder for model saving

# Model parameters
n_hidden_1 = 32      # number of hidden neurons 1
n_hidden_2 = 64      # number of hidden neurons 2
n_hidden_3 = 48      # number of hidden neurons 3
n_hidden_4 = 24      # number of hidden neurons 4

#data["Batch Size"]=int((data["Batch Size"]))

# Learning parameters
#batch_size  = data["Batch Size"]
batch_size  = 128   # batch_size used during training

#print("batch size:{}".format(batch_size))
#print("data type of batch size:{}".format(type(batch_size)))
#f.close()
num_epochs  = 10     # number of training epochs
val_split   = 0.01  # percentage of training data used as validation data, between [0,1]
valFromTest = False # True:  use test set as validation set
                    # False: take validation set from training set with val_split

# Learning rate
initialLearningRate = 0.01   # initial learning rate
decayRate           = 0.5     # exponential decay rate
decayEpochs         = 10      # decay steps
doStairCase         = True    # Use stepwise instead of continuous exp. decay
activationfn=1
# =====================================================================================
# Init
# =====================================================================================
# Start timer
start_time = time.time()

# Print Header
printHeader()

# Check if placed on GPU and avoid unnecessarily allocating all available memory
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    printNotice('Found '+str(len(gpus))+' physical GPU(s) on system.')
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True) # Allocate only neccessary memory
    if (len(gpus) > 1):
      printWarning('More than one GPU on system may cause unexpected behaviour')
  except RuntimeError as e:
    printWarning(e) # Memory growth must be set before GPUs have been initialized
else:
  printWarning('No GPU found on system, Tensorflow will probably run on CPU')


# =====================================================================================
# Input pipeline
# =====================================================================================
printBanner('Starting input pipeline')

# Get Training and Test Dataset
train_dataset,train_labels,test_dataset,test_labels = getDataset(  trainFiles
                                                                  ,testFiles
                                                                  ,dt,seqLength
                                                                  ,debug=debug
                                                                  ,doSqueeze=True
                                                                  ,doShuffle=True
                                                                  ,doDataAug=True
                                                                  )
# Get dimensions of data
Ninput      = train_dataset.shape[-1] # number of input features
NinputLabel =  train_labels.shape[-1] # number of labels
print("\ntraining-dataset shape:{}".format(train_dataset.shape))
print("\n data type of training dataset:{}".format(type(train_dataset)))
print("\n dtype of training dataset:{}".format(train_dataset.dtype))
print("\ntrain_labels shape:{}".format(train_labels.shape))
#print("\ntrain_labels column:{}".format(train_labels.column))
print("\nNinput shape:{}".format(Ninput))
print("\nNinputLabel shape:{}".format(NinputLabel))
print("\ntest-dataset shape:{}".format(test_dataset.shape))
print("\ntest_labels shape:{}".format(test_labels.shape))

print("\n train dataset array:{}".format(train_dataset))
print("\n train label array:{}".format(train_labels))
#dtm.addForExport(test_dataset, "testinputs")


# =====================================================================================
# Keras model
# =====================================================================================
printBanner('Building model')

# Either restart
if (doRestart):
  printNotice('Load model from: ' + restartPath)
  try:
    rnn = tf.keras.models.load_model(restartPath, custom_objects={
                                                  "correlation_coefficient_metric":
                                                   correlation_coefficient_metric
                                                   }) # Add custom metric here
  except:
    printWarning('ERROR: Model could not be loaded')
    sys.exit(1)

# Or create new model
else:
  printNotice('Build new model from scratch')

  # Use proper normalization with mean and std of training set
  input_norm = tf.keras.layers.experimental.preprocessing.Normalization()
  input_norm.adapt(train_dataset)
  # Input
  rnn_inputs = tf.keras.Input(shape=(seqLength,Ninput),name='input_rnn')
  x = input_norm(rnn_inputs)
  x = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_hidden_1,activation='relu',kernel_initializer='he_uniform'))(x)
  x = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_hidden_2,activation='relu',kernel_initializer='he_uniform'))(x)
  #copy_time_distributed_output = x

  x = tf.keras.layers.GRU(n_hidden_2, activation='tanh', return_sequences=False, stateful=False)(x)
  #copy_gru_output = x
  x = tf.keras.layers.Dense(n_hidden_3, activation='relu',kernel_initializer='he_uniform')(x)
  x = tf.keras.layers.Dense(n_hidden_4, activation='relu',kernel_initializer='he_uniform')(x)
  #copy_dense = x
  rnn_outputs = tf.keras.layers.Dense(NinputLabel,name='output_rnn')(x)
  rnn = tf.keras.Model(inputs=rnn_inputs,outputs=rnn_outputs)

#print(f'Printing data for visualization \n',
  #    f'Time Distributed :{copy_time_distributed_output}\n',
   #   f'GRU Output: {copy_gru_output}',
   #   f'Dense Output: {copy_dense}')


print(rnn.layers)
print("\nLength of rnn layers:{}".format(len(rnn.layers)))
k_value = K.eval(rnn.layers[0])
print("\nvalue of k :{}".format(k_value))
# Write model summary
if (debug>0):
  rnn.summary()
#keras.utils.plot_model(rnn, "my_first_model_with_shape_info.png", show_shapes=True)

# =====================================================================================
# Training
# =====================================================================================
printBanner( 'Starting Training' )

## Gauss-Lobatto integration weights for LGL weighted mse loss
#weights_LGL = LGL_weights_3D(CellPoints-1)

# Learning rate scheduler
decaySteps=(train_dataset.shape[0])/batch_size*decayEpochs
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initialLearningRate
  , decay_steps=decaySteps
  , decay_rate=decayRate
  , staircase=doStairCase
  )

# Optimizer
optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

# Compile Model or set initial epoch for restart
if (not doRestart):
  initial_epochs = 0 # Start from scratch
  rnn.compile(  optimizer=optimizer
              , loss='mse'
              , metrics=[correlation_coefficient_metric]
              )

# Tensorboard callback for loggging
log_dir = "logs/" + modelName +'_'+ str(modelNumb)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# Create a callback that saves the model's weights (or empty pseudo callback)
if doSave:
  cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=savePath,verbose=debug)
  printNotice('Model will be saved at '+savePath)
else:
  cp_callback = tf.keras.callbacks.Callback()
  printWarning('Model saving is disabled: The trained model weights will not be saved.')

# Training
rnn.fit( x=train_dataset
       , y=train_labels
       , batch_size=batch_size
       , epochs=num_epochs
       , initial_epoch=initial_epochs
       , validation_data=(test_dataset,test_labels)
       , callbacks=[tensorboard_callback,cp_callback]
       )
# Saving entire model in tf format
rnn.save("MyModel_tf",save_format='tf')

# Saving entire model in h5 format
rnn.save("MyModel_h5",save_format='h5')


# =====================================================================================
# Evaluate Model
# =====================================================================================
printBanner( 'Evaluating Model' )

# Evaluate the model on the test data using `evaluate`
printNotice('Evaluate on test data')
results = rnn.evaluate(test_dataset, test_labels, batch_size=batch_size, verbose=1)
print('test loss, test acc:' + str(results))
dtm.addForExport("%.2f%%" % (results[1]), "model_accuracy")

 
for layer in rnn.layers:
  print("\nrnn layer name and layer:{0}{1}".format(layer.name, layer))
  print("\nlrnn ayer.get_weights:{}".format(layer.get_weights))

rnn_weights_list_gru = rnn.get_weights()
print("\nrnn weights_list_gru : {}".format(rnn_weights_list_gru))

rnngruweights=[]
for i, weights in enumerate(rnn_weights_list_gru):
    rnngruweights.append(weights.tolist())
 
dtm.addForExport(rnngruweights, "gruweights")
 
 
# Transfer weight to a new model to get LSTM activations.

print("transfer weight model _rnn_inputs_start")

input_norm = tf.keras.layers.experimental.preprocessing.Normalization()
input_norm.adapt(train_dataset)

#Second model input
model_rnn = tf.keras.Input(shape=(seqLength,Ninput),name='input_rnn')
x = input_norm(model_rnn)
x = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_hidden_1,activation='relu',kernel_initializer='he_uniform'))(x)
x = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_hidden_2,activation='relu',kernel_initializer='he_uniform'))(x)
x1 = tf.keras.layers.GRU(n_hidden_2, activation='tanh', return_sequences=True, stateful=False)(x)

model_rnn = tf.keras.Model(inputs=model_rnn,outputs=x1)

#keras.utils.plot_model(model_rnn, "rnn_weight_model_with_shape_info.png", show_shapes=True)

print(model_rnn.layers)
print(len(model_rnn.layers))
k_value = K.eval(model_rnn.layers)
print(k_value)
if (debug>0):
  model_rnn.summary()


model_rnn.layers[0].set_weights(rnn.layers[0].get_weights())
model_rnn.layers[1].set_weights(rnn.layers[1].get_weights())
model_rnn.layers[2].set_weights(rnn.layers[2].get_weights())
model_rnn.layers[3].set_weights(rnn.layers[3].get_weights())
model_rnn.layers[4].set_weights(rnn.layers[4].get_weights())

print("transfer weight end")

#model_rnn_pred weight of last layer
print("model_rnn_pred weight of last layer_start")

model_rnn_pred = tf.keras.Input(shape=(model_rnn.layers[4].output_shape[1:]),name='input_rnn')
model_rnn_pred = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(n_hidden_3,activation='relu',kernel_initializer='he_uniform'))(model_rnn_pred)
model_rnn_pred = tf.keras.layers.Dense(n_hidden_4, activation='relu',kernel_initializer='he_uniform')(model_rnn_pred)
rnn_outputs = tf.keras.layers.Dense(NinputLabel,name='output_rnn',activation='relu')(model_rnn_pred)
model_rnn_hspred = tf.keras.Model(inputs=model_rnn_pred,outputs=rnn_outputs)

#keras.utils.plot_model(model_rnn_hspred, "model_rnn_hspred with_shape_info.png", show_shapes=True)
print(model_rnn_hspred.layers)
print(len(model_rnn_hspred.layers))
k_value = K.eval(model_rnn_hspred.layers)
print(k_value)
if (debug>0):
  model_rnn_hspred.summary()


print("model_rnn_pred weight of last layer end")

#hidden states
#test_indexes = np.arange(300)

res = [random.randrange(0, 110592) for i in range(500)]
res.sort() 
# printing result
print (type(res))
print ("Random number list is : " +  str(res))
print (len(res))

test_indexes=np.asarray(res)
print(test_indexes)
print (type(test_indexes))
print (len(test_indexes))


#normal without 0th hidden states
hs_output = model_rnn.predict(test_dataset[test_indexes])
hs_shape = hs_output.shape
print("\nhs_shape:{}".format(hs_shape))
print("\nhs_ouput values :{}".format(hs_output))
print("\ndatatype of hs_output:{}".format(type(hs_output)))

dtm.addForExport(hs_output, "hsoutputhiddenstates")

for layer in model_rnn.layers:
  print("\nmodelrnn layer name and layer:{0}{1}".format(layer.name, layer))
  print("\nmodelrnn layer.get_weights:{}".format(layer.get_weights))

weights_list_gru = model_rnn.get_weights()
print("\nmodel weights_list_gru : {}".format(weights_list_gru))

gruweights=[]
for i, weights in enumerate(weights_list_gru):
    gruweights.append(weights.tolist())

#dtm.addForExport(gruweights, "gruweights") 


#Including 0th hidden state
hs_outputo=hs_output
zerohidden=np.zeros(shape=(64),dtype=float)
print("\nzero hidden values :{}".format(zerohidden))
print("datatype of zero hidden values:{}".format(type(zerohidden)))
inczerohidden=np.insert(hs_outputo,0,zerohidden,axis=1)
inc_zero = inczerohidden.shape
print("\inc_zero:{}".format(inc_zero))
print("\ninczerohidden values :{}".format(inczerohidden))
print("datatype of inczerohidden values:{}".format(type(inczerohidden)))

dtm.addForExport(inczerohidden, "zerohidden")



#reshaping to 2 dimension from 3 dimension
#Without 0th hidden state
hidden_states = hs_output.reshape((hs_shape[0]*hs_shape[1], hs_shape[2]))
#with 0th hidden state
hidden_stateso = inczerohidden.reshape((inc_zero[0]*inc_zero[1], inc_zero[2]))
print("\nhiddenstateshape:{}".format(hidden_states.shape))
print("\nhiddenstate values :{}".format(hidden_states))
print("\ndatatype of hiddenstates:{}".format(type(hidden_states)))
print("\nhiddenstateo shape:{}".format(hidden_stateso.shape))
print("\nhiddenstateo values :{}".format(hidden_stateso))
print("\ndatatype of hiddenstateso:{}".format(type(hidden_stateso)))
dtm.addForExport(hidden_states, "hiddenstates")
dtm.addForExport(hidden_stateso, "hiddenstateso")


# Compute Cross-Correlation of test predictions
printNotice('Generate predictions on test data')
prediction = rnn.predict(test_dataset[test_indexes])
test_input=test_dataset[test_indexes]
test_output=test_labels[test_indexes]
print("\ntest_input : {}".format(test_input))
print("\ntest_output : {}".format(test_output))
print("\nprediction datashape: {}".format(prediction.shape))
print("\nprediction values: {}".format(prediction))
dtm.addForExport(test_input, "test_input")
dtm.addForExport(test_output, "test_output")
dtm.addForExport(prediction, "prediction")

"""
#sample code tried for SHAP, Feature importance
#feature importance
#results = permutation_importance(rnn, train_dataset.reshape((-1,3)), train_labels, scoring='neg_mean_squared_error')
#importance = results.importances_mean
#for i,v in enumerate(importance):
#	print('Feature: %0d, Score: %.5f' % (i,v))


#ann_viz(rnn, title="My first neural network")

#Gradient Tape
#seq = tf.Variable(test_dataset[np.newaxis,:,:], dtype=tf.float32)
#with tf.GradientTape() as tape:
#    predictions = rnn(seq)
#grads = tape.gradient(predictions, seq)
#grads = tf.reduce_mean(grads, axis=1).numpy()[0]

#print("\ngrads : {}".format(grads))

#DE = shap.DeepExplainer(rnn, train_dataset[0:5,:,:]) # X_train is 3d numpy.ndarray
#shap_values = DE.shap_values(test_dataset[0:5,:,:], check_additivity=False)

#explainer = shap.explainers.Permutation(rnn.predict, train_dataset[0:5,:,:])

#print("\nexplainer:{}".format(explainer))
#print("\ndatatype of explainer:{}".format(type(explainer)))

#shap_values = explainer(train_dataset[0:5])

#print("\nshap_value_single:{}".format(shap_values))

##shap
explainer = shap.KernelExplainer(model = rnn.predict, data = test_dataset[test_indexes], link = "identity")

print("\nexplainer:{}".format(explainer))
print("\ndatatype of explainer:{}".format(type(explainer)))

#onesample=0
shap_value_single = explainer.shap_values(X = test_dataset[test_indexes,:,:], nsamples = 100)

print("\nshap_value_single:{}".format(shap_value_single))

background = train_dataset[np.random.choice(train_dataset.shape[0], 100, replace=False)]

# explain predictions of the model on three images
e = shap.DeepExplainer(rnn, background)
# ...or pass tensors directly
# e = shap.DeepExplainer((model.layers[0].input, model.layers[-1].output), background)
shap_values = e.shap_values(test_dataset[1:5])


#explainer = shap.DeepExplainer(rnn, train_dataset)
#shap_values = explainer.shap_values(test_dataset[0:3])

# select backgroud for shap
background = train_dataset[np.random.choice(train_dataset.shape[0], 1000, replace=False)]
# DeepExplainer to explain predictions of the model
explainer = shap.DeepExplainer(rnn, background)
# compute shap values
shap_values = explainer.shap_values(test_dataset[test_indexes])


random_ind = np.random.choice(test_dataset.shape[0], 1000, replace=False)
print(random_ind)
data = test_dataset[random_ind[0:300]]
e = shap.DeepExplainer((rnn.layers[0].input, rnn.layers[-1].output),data)
test1 = test_dataset[random_ind[0:300]]
shap_val = e.shap_values(test1)
shap_val = np.array(shap_val)
shap_val = np.reshape(shap_val,(int(shap_val.shape[1]),int(shap_val.shape[2]),int(shap_val.shape[3])))
shap_abs = np.absolute(shap_val)
sum_0 = np.sum(shap_abs,axis=0)

print("\nexplainer:{}".format(e))
print("\ndatatype of explainer:{}".format(type(e)))
print("\nshap_value_single:{}".format(shap_val))


#background = X_train.iloc[np.random.choice(X_train.shape[0], 100, replace=False)]

#explainer = shap.DeepExplainer(
#    (model.layers[0].input, model.layers[-1].output), background
#)
#shap_values = explainer.shap_values(X_test[:3].values)


explainer = shap.DeepExplainer(rnn, train_dataset[test_indexes,:,:])
shap_values = explainer.shap_values(test_dataset[test_indexes,:,:])

print("\nexplainer.expected_value:{}".format(explainer.expected_value))

print("\nexplainer:{}".format(explainer))
print("\ndatatype of explainer:{}".format(type(explainer)))
print("\nshap_value_single:{}".format(shap_values))
print("\nlength shap_value_single:{}".format(len(shap_values)))
print("\nshap_values[0].shape:{}".format(shap_values[0].shape))

# Fits the explainer
explainer = shap.Explainer(rnn.predict, test_dataset[test_indexes])
# Calculates the SHAP values - It takes some time
shap_values = explainer.shap_values(test_dataset[test_indexes])

print("\nexplainer:{}".format(explainer))
print("\ndatatype of explainer:{}".format(type(explainer)))
print("\nshap_value_single:{}".format(shap_values))
"""
# PCA
pca_proj = PCA(n_components=2, random_state=randomStatePCA).fit_transform(hidden_states)
print("\nprojection_pca : {}".format(pca_proj))
print("\nprojection_pca datashape: {}".format(pca_proj.shape))
dtm.addForExport(pca_proj, "pcaprojection")
#dtm.writeJson("projection_pca_nopad_rs" + str(seqLength) + "_ts" + str(randomStatePCA), randomseed)

# t-SNE normal

tsne = TSNE(n_components=2, perplexity=perplexityTSNE, early_exaggeration=12.0, verbose=1, random_state=randomStateTSNE).fit(hidden_states)
projection_tsne = tsne.embedding_
nfeatures=tsne.n_features_in_
#featurenames=tsne.feature_names_in_
print("\nprojection_tsne : {}".format(projection_tsne))
print("\nprojection_tsne datashape: {}".format(projection_tsne.shape))
print("\nnfeatures: {}".format(nfeatures))
#print("\nfeaturenames: {}".format(featurenames))
dtm.addForExport(projection_tsne, "projection")
dtm.addForExport(nfeatures, "nfeatures")
#dtm.addForExport(featurenames, "featurenames")

# t-SNE normal with 0th hidden state

tsneo = TSNE(n_components=2, perplexity=perplexityTSNE, early_exaggeration=12.0, verbose=1, random_state=randomStateTSNE).fit(hidden_stateso)
projection_tsneo = tsneo.embedding_
nfeatureso=tsneo.n_features_in_
#featurenames=tsne.feature_names_in_
print("\nprojection_tsneo : {}".format(projection_tsneo))
print("\nprojection_tsneo datashape: {}".format(projection_tsneo.shape))
print("\nnfeatureso: {}".format(nfeatureso))
#print("\nfeaturenames: {}".format(featurenames))
dtm.addForExport(projection_tsneo, "projectiono")
dtm.addForExport(nfeatureso, "nfeatureso")
#dtm.addForExport(featurenames, "featurenames")


projection_tsned=projection_tsne
projection_tsnedo=projection_tsneo

"""
#cluster algorithm 3ts w/o 0th
subsample=projection_tsned[2::3]
print("\subsample : {}".format(subsample))

df = pd.DataFrame(subsample)
df = pd.DataFrame(subsample, 
             columns=['xaxis', 
                      'yaxis'])

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['xaxis','yaxis']])
df['cluster']=y_predicted
print("\nclustercenters : {}".format(km.cluster_centers_))


data=df.to_numpy()
print("\ndatanumpy : {}".format(data))
datalist=data.tolist()
print("\ndatalist : {}".format(datalist))
print("\ndatalist length : {}".format(len(datalist)))


dfcluster = pd.DataFrame(projection_tsned, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfcluster["cluster"]=np.nan
datacluster=dfcluster.to_numpy()
print("\ndatacluster : {}".format(datacluster))
print("\ndatacluster : {}".format(len(datacluster)))

dataclusterlist1=datacluster.tolist()
print("\ndatacluster : {}".format(dataclusterlist1))
print("\ndatacluster : {}".format(len(dataclusterlist1)))

dataclusterlist12 = dataclusterlist1.copy() 

j=2

for i in datalist:

    dataclusterlist12[j]=i
    j+=3
    


print("\nj value  : {}".format(j))
print("\n data clusterlist12: {}".format(dataclusterlist12)) 
print("\n data clusterlist12: {}".format(len(dataclusterlist12)))

dfwithcluster = pd.DataFrame(dataclusterlist12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbefore : {}".format(dfwithcluster))
dfwithcluster["clustersmerged"].fillna(method='bfill', limit=2, inplace=True)
print("\ndataclusterafter : {}".format(dfwithcluster))

cluster0 = dfwithcluster[dfwithcluster.clustersmerged==0]
cluster1 = dfwithcluster[dfwithcluster.clustersmerged==1]
cluster2 = dfwithcluster[dfwithcluster.clustersmerged==2]


cluster0.drop("clustersmerged", axis=1, inplace=True)
cluster1.drop("clustersmerged", axis=1, inplace=True)
cluster2.drop("clustersmerged", axis=1, inplace=True)


c0=cluster0.to_numpy()
c1=cluster1.to_numpy()
c2=cluster2.to_numpy()


print("\nc0 : {}".format(c0))
print("\nc0 length : {}".format(len(c0)))
print("\nc1 : {}".format(c1))
print("\nc1 length : {}".format(len(c1)))
print("\nc2 : {}".format(c2))
print("\nc2 length : {}".format(len(c2)))


dtm.addForExport(c0, "c0")
dtm.addForExport(c1, "c1")
dtm.addForExport(c2, "c2")

#cluster algorithm 3ts w 0th
subsampleo=projection_tsnedo[3::4]
print("\subsampleo : {}".format(subsampleo))

dfo = pd.DataFrame(subsampleo)
dfo = pd.DataFrame(subsampleo, 
             columns=['xaxis', 
                      'yaxis'])

kmo = KMeans(n_clusters=3)
y_predictedo = kmo.fit_predict(dfo[['xaxis','yaxis']])
dfo['cluster']=y_predictedo
print("\nclustercenterso : {}".format(kmo.cluster_centers_))


datao=dfo.to_numpy()
print("\ndatanumpyo : {}".format(datao))
datalisto=datao.tolist()
print("\ndatalisto : {}".format(datalisto))
print("\ndatalisto length : {}".format(len(datalisto)))


dfclustero = pd.DataFrame(projection_tsnedo, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfclustero["cluster"]=np.nan
dataclustero=dfclustero.to_numpy()
print("\ndataclustero : {}".format(dataclustero))
print("\ndataclustero : {}".format(len(dataclustero)))

dataclusterlisto1=dataclustero.tolist()
print("\ndataclustero : {}".format(dataclusterlisto1))
print("\ndataclustero : {}".format(len(dataclusterlisto1)))

dataclusterlisto12 = dataclusterlisto1.copy() 

j=3

for i in datalisto:

    dataclusterlisto12[j]=i
    j+=4
    


print("\njo value  : {}".format(j))
print("\n data clusterlisto12: {}".format(dataclusterlisto12)) 
print("\n data clusterlisto12: {}".format(len(dataclusterlisto12)))

dfwithclustero = pd.DataFrame(dataclusterlisto12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbeforeo : {}".format(dfwithclustero))
dfwithclustero["clustersmerged"].fillna(method='bfill', limit=3, inplace=True)
print("\ndataclusteraftero : {}".format(dfwithclustero))

clustero0 = dfwithclustero[dfwithclustero.clustersmerged==0]
clustero1 = dfwithclustero[dfwithclustero.clustersmerged==1]
clustero2 = dfwithclustero[dfwithclustero.clustersmerged==2]


clustero0.drop("clustersmerged", axis=1, inplace=True)
clustero1.drop("clustersmerged", axis=1, inplace=True)
clustero2.drop("clustersmerged", axis=1, inplace=True)


co0=clustero0.to_numpy()
co1=clustero1.to_numpy()
co2=clustero2.to_numpy()


print("\nco0 : {}".format(co0))
print("\nco0 length : {}".format(len(co0)))
print("\nco1 : {}".format(co1))
print("\nco1 length : {}".format(len(co1)))
print("\nco2 : {}".format(co2))
print("\nco2 length : {}".format(len(co2)))


dtm.addForExport(co0, "co0")
dtm.addForExport(co1, "co1")
dtm.addForExport(co2, "co2")

"""


#cluster algortihm 5ts w/o 0
subsample=projection_tsned[4::5]
print("\subsample : {}".format(subsample))

df = pd.DataFrame(subsample)
df = pd.DataFrame(subsample, 
             columns=['xaxis', 
                      'yaxis'])

km = KMeans(n_clusters=5)
y_predicted = km.fit_predict(df[['xaxis','yaxis']])
df['cluster']=y_predicted
print("\nclustercenters : {}".format(km.cluster_centers_))


data=df.to_numpy()
print("\ndatanumpy : {}".format(data))
datalist=data.tolist()
print("\ndatalist : {}".format(datalist))
print("\ndatalist length : {}".format(len(datalist)))


dfcluster = pd.DataFrame(projection_tsned, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfcluster["cluster"]=np.nan
datacluster=dfcluster.to_numpy()
print("\ndatacluster : {}".format(datacluster))
print("\ndatacluster : {}".format(len(datacluster)))

dataclusterlist1=datacluster.tolist()
print("\ndatacluster : {}".format(dataclusterlist1))
print("\ndatacluster : {}".format(len(dataclusterlist1)))

dataclusterlist12 = dataclusterlist1.copy() 

j=4

for i in datalist:

    dataclusterlist12[j]=i
    j+=5
    


print("\nj value  : {}".format(j))
print("\n data clusterlist12: {}".format(dataclusterlist12)) 
print("\n data clusterlist12: {}".format(len(dataclusterlist12)))

dfwithcluster = pd.DataFrame(dataclusterlist12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbefore : {}".format(dfwithcluster))
dfwithcluster["clustersmerged"].fillna(method='bfill', limit=4, inplace=True)
print("\ndataclusterafter : {}".format(dfwithcluster))

cluster0 = dfwithcluster[dfwithcluster.clustersmerged==0]
cluster1 = dfwithcluster[dfwithcluster.clustersmerged==1]
cluster2 = dfwithcluster[dfwithcluster.clustersmerged==2]
cluster3 = dfwithcluster[dfwithcluster.clustersmerged==3]
cluster4 = dfwithcluster[dfwithcluster.clustersmerged==4]

cluster0.drop("clustersmerged", axis=1, inplace=True)
cluster1.drop("clustersmerged", axis=1, inplace=True)
cluster2.drop("clustersmerged", axis=1, inplace=True)
cluster3.drop("clustersmerged", axis=1, inplace=True)
cluster4.drop("clustersmerged", axis=1, inplace=True)

c0=cluster0.to_numpy()
c1=cluster1.to_numpy()
c2=cluster2.to_numpy()
c3=cluster3.to_numpy()
c4=cluster4.to_numpy()

print("\nc0 : {}".format(c0))
print("\nc0 length : {}".format(len(c0)))
print("\nc1 : {}".format(c1))
print("\nc1 length : {}".format(len(c1)))
print("\nc2 : {}".format(c2))
print("\nc2 length : {}".format(len(c2)))
print("\nc3 : {}".format(c3))
print("\nc3 length : {}".format(len(c3)))
print("\nc4 : {}".format(c4))
print("\nc4 length : {}".format(len(c4)))

dtm.addForExport(c0, "c0")
dtm.addForExport(c1, "c1")
dtm.addForExport(c2, "c2")
dtm.addForExport(c3, "c3")
dtm.addForExport(c4, "c4")

#cluster algortihm 5ts with 0
subsampleo=projection_tsnedo[5::6]
print("\subsampleo : {}".format(subsampleo))

dfo = pd.DataFrame(subsampleo)
dfo = pd.DataFrame(subsampleo, 
             columns=['xaxis', 
                      'yaxis'])

kmo = KMeans(n_clusters=5)
y_predictedo = kmo.fit_predict(dfo[['xaxis','yaxis']])
dfo['cluster']=y_predictedo
print("\nclustercenterso : {}".format(kmo.cluster_centers_))


datao=dfo.to_numpy()
print("\ndatanumpyo : {}".format(datao))
datalisto=datao.tolist()
print("\ndatalisto : {}".format(datalisto))
print("\ndatalisto length : {}".format(len(datalisto)))


dfclustero = pd.DataFrame(projection_tsnedo, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfclustero["cluster"]=np.nan
dataclustero=dfclustero.to_numpy()
print("\ndataclustero : {}".format(dataclustero))
print("\ndataclustero : {}".format(len(dataclustero)))

dataclusterlisto1=dataclustero.tolist()
print("\ndataclustero : {}".format(dataclusterlisto1))
print("\ndataclustero : {}".format(len(dataclusterlisto1)))

dataclusterlisto12 = dataclusterlisto1.copy() 

j=5

for i in datalisto:

    dataclusterlisto12[j]=i
    j+=6
    


print("\nj value  : {}".format(j))
print("\n data clusterlisto12: {}".format(dataclusterlisto12)) 
print("\n data clusterlisto12: {}".format(len(dataclusterlisto12)))

dfwithclustero = pd.DataFrame(dataclusterlisto12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbeforeo : {}".format(dfwithclustero))
dfwithclustero["clustersmerged"].fillna(method='bfill', limit=5, inplace=True)
print("\ndataclusteraftero : {}".format(dfwithclustero))

clustero0 = dfwithclustero[dfwithclustero.clustersmerged==0]
clustero1 = dfwithclustero[dfwithclustero.clustersmerged==1]
clustero2 = dfwithclustero[dfwithclustero.clustersmerged==2]
clustero3 = dfwithclustero[dfwithclustero.clustersmerged==3]
clustero4 = dfwithclustero[dfwithclustero.clustersmerged==4]

clustero0.drop("clustersmerged", axis=1, inplace=True)
clustero1.drop("clustersmerged", axis=1, inplace=True)
clustero2.drop("clustersmerged", axis=1, inplace=True)
clustero3.drop("clustersmerged", axis=1, inplace=True)
clustero4.drop("clustersmerged", axis=1, inplace=True)

co0=clustero0.to_numpy()
co1=clustero1.to_numpy()
co2=clustero2.to_numpy()
co3=clustero3.to_numpy()
co4=clustero4.to_numpy()

print("\nco0 : {}".format(co0))
print("\nco0 length : {}".format(len(co0)))
print("\nco1 : {}".format(co1))
print("\nco1 length : {}".format(len(co1)))
print("\nco2 : {}".format(co2))
print("\nco2 length : {}".format(len(co2)))
print("\nco3 : {}".format(co3))
print("\nco3 length : {}".format(len(co3)))
print("\nco4 : {}".format(co4))
print("\nco4 length : {}".format(len(co4)))

dtm.addForExport(co0, "co0")
dtm.addForExport(co1, "co1")
dtm.addForExport(co2, "co2")
dtm.addForExport(co3, "co3")
dtm.addForExport(co4, "co4")

"""
#cluster algortihm 10ts w/o 0th
subsample=projection_tsned[9::10]
print("\subsample : {}".format(subsample))

df = pd.DataFrame(subsample)
df = pd.DataFrame(subsample, 
             columns=['xaxis', 
                      'yaxis'])

km = KMeans(n_clusters=10)
y_predicted = km.fit_predict(df[['xaxis','yaxis']])
df['cluster']=y_predicted
print("\nclustercenters : {}".format(km.cluster_centers_))


data=df.to_numpy()
print("\ndatanumpy : {}".format(data))
datalist=data.tolist()
print("\ndatalist : {}".format(datalist))
print("\ndatalist length : {}".format(len(datalist)))


dfcluster = pd.DataFrame(projection_tsned, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfcluster["cluster"]=np.nan
datacluster=dfcluster.to_numpy()
print("\ndatacluster : {}".format(datacluster))
print("\ndatacluster : {}".format(len(datacluster)))

dataclusterlist1=datacluster.tolist()
print("\ndatacluster : {}".format(dataclusterlist1))
print("\ndatacluster : {}".format(len(dataclusterlist1)))

dataclusterlist12 = dataclusterlist1.copy() 

j=9

for i in datalist:

    dataclusterlist12[j]=i
    j+=10
    


print("\nj value  : {}".format(j))
print("\n data clusterlist12: {}".format(dataclusterlist12)) 
print("\n data clusterlist12: {}".format(len(dataclusterlist12)))

dfwithcluster = pd.DataFrame(dataclusterlist12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbefore : {}".format(dfwithcluster))
dfwithcluster["clustersmerged"].fillna(method='bfill', limit=9, inplace=True)
print("\ndataclusterafter : {}".format(dfwithcluster))

cluster0 = dfwithcluster[dfwithcluster.clustersmerged==0]
cluster1 = dfwithcluster[dfwithcluster.clustersmerged==1]
cluster2 = dfwithcluster[dfwithcluster.clustersmerged==2]
cluster3 = dfwithcluster[dfwithcluster.clustersmerged==3]
cluster4 = dfwithcluster[dfwithcluster.clustersmerged==4]
cluster5 = dfwithcluster[dfwithcluster.clustersmerged==5]
cluster6 = dfwithcluster[dfwithcluster.clustersmerged==6]
cluster7 = dfwithcluster[dfwithcluster.clustersmerged==7]
cluster8 = dfwithcluster[dfwithcluster.clustersmerged==8]
cluster9 = dfwithcluster[dfwithcluster.clustersmerged==9]

cluster0.drop("clustersmerged", axis=1, inplace=True)
cluster1.drop("clustersmerged", axis=1, inplace=True)
cluster2.drop("clustersmerged", axis=1, inplace=True)
cluster3.drop("clustersmerged", axis=1, inplace=True)
cluster4.drop("clustersmerged", axis=1, inplace=True)
cluster5.drop("clustersmerged", axis=1, inplace=True)
cluster6.drop("clustersmerged", axis=1, inplace=True)
cluster7.drop("clustersmerged", axis=1, inplace=True)
cluster8.drop("clustersmerged", axis=1, inplace=True)
cluster9.drop("clustersmerged", axis=1, inplace=True)

c0=cluster0.to_numpy()
c1=cluster1.to_numpy()
c2=cluster2.to_numpy()
c3=cluster3.to_numpy()
c4=cluster4.to_numpy()
c5=cluster5.to_numpy()
c6=cluster6.to_numpy()
c7=cluster7.to_numpy()
c8=cluster8.to_numpy()
c9=cluster9.to_numpy()

print("\nc0 : {}".format(c0))
print("\nc0 length : {}".format(len(c0)))
print("\nc1 : {}".format(c1))
print("\nc1 length : {}".format(len(c1)))
print("\nc2 : {}".format(c2))
print("\nc2 length : {}".format(len(c2)))
print("\nc3 : {}".format(c3))
print("\nc3 length : {}".format(len(c3)))
print("\nc4 : {}".format(c4))
print("\nc4 length : {}".format(len(c4)))

dtm.addForExport(c0, "c0")
dtm.addForExport(c1, "c1")
dtm.addForExport(c2, "c2")
dtm.addForExport(c3, "c3")
dtm.addForExport(c4, "c4")
dtm.addForExport(c5, "c5")
dtm.addForExport(c6, "c6")
dtm.addForExport(c7, "c7")
dtm.addForExport(c8, "c8")
dtm.addForExport(c9, "c9")


#cluster algortihm 10ts with 0th
subsampleo=projection_tsnedo[10::11]
print("\subsampleo : {}".format(subsampleo))

dfo = pd.DataFrame(subsampleo)
dfo = pd.DataFrame(subsampleo, 
             columns=['xaxis', 
                      'yaxis'])

kmo = KMeans(n_clusters=10)
y_predictedo = kmo.fit_predict(dfo[['xaxis','yaxis']])
dfo['cluster']=y_predictedo
print("\nclustercenterso : {}".format(kmo.cluster_centers_))


datao=dfo.to_numpy()
print("\ndatanumpyo : {}".format(datao))
datalisto=datao.tolist()
print("\ndatalisto : {}".format(datalisto))
print("\ndatalisto length : {}".format(len(datalisto)))


dfclustero = pd.DataFrame(projection_tsnedo, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfclustero["cluster"]=np.nan
dataclustero=dfclustero.to_numpy()
print("\ndataclustero : {}".format(dataclustero))
print("\ndataclustero : {}".format(len(dataclustero)))

dataclusterlisto1=dataclustero.tolist()
print("\ndataclustero : {}".format(dataclusterlisto1))
print("\ndataclustero : {}".format(len(dataclusterlisto1)))

dataclusterlisto12 = dataclusterlisto1.copy() 

j=10

for i in datalisto:

    dataclusterlisto12[j]=i
    j+=11
    


print("\nj value  : {}".format(j))
print("\n data clusterlisto12: {}".format(dataclusterlisto12)) 
print("\n data clusterlisto12: {}".format(len(dataclusterlisto12)))

dfwithclustero = pd.DataFrame(dataclusterlisto12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbeforeo : {}".format(dfwithclustero))
dfwithclustero["clustersmerged"].fillna(method='bfill', limit=10, inplace=True)
print("\ndataclusteraftero : {}".format(dfwithclustero))

clustero0 = dfwithclustero[dfwithclustero.clustersmerged==0]
clustero1 = dfwithclustero[dfwithclustero.clustersmerged==1]
clustero2 = dfwithclustero[dfwithclustero.clustersmerged==2]
clustero3 = dfwithclustero[dfwithclustero.clustersmerged==3]
clustero4 = dfwithclustero[dfwithclustero.clustersmerged==4]
clustero5 = dfwithclustero[dfwithclustero.clustersmerged==5]
clustero6 = dfwithclustero[dfwithclustero.clustersmerged==6]
clustero7 = dfwithclustero[dfwithclustero.clustersmerged==7]
clustero8 = dfwithclustero[dfwithclustero.clustersmerged==8]
clustero9 = dfwithclustero[dfwithclustero.clustersmerged==9]

clustero0.drop("clustersmerged", axis=1, inplace=True)
clustero1.drop("clustersmerged", axis=1, inplace=True)
clustero2.drop("clustersmerged", axis=1, inplace=True)
clustero3.drop("clustersmerged", axis=1, inplace=True)
clustero4.drop("clustersmerged", axis=1, inplace=True)
clustero5.drop("clustersmerged", axis=1, inplace=True)
clustero6.drop("clustersmerged", axis=1, inplace=True)
clustero7.drop("clustersmerged", axis=1, inplace=True)
clustero8.drop("clustersmerged", axis=1, inplace=True)
clustero9.drop("clustersmerged", axis=1, inplace=True)

co0=clustero0.to_numpy()
co1=clustero1.to_numpy()
co2=clustero2.to_numpy()
co3=clustero3.to_numpy()
co4=clustero4.to_numpy()
co5=clustero5.to_numpy()
co6=clustero6.to_numpy()
co7=clustero7.to_numpy()
co8=clustero8.to_numpy()
co9=clustero9.to_numpy()

print("\nco0 : {}".format(co0))
print("\nco0 length : {}".format(len(co0)))
print("\nco1 : {}".format(co1))
print("\nco1 length : {}".format(len(co1)))
print("\nco2 : {}".format(co2))
print("\nco2 length : {}".format(len(co2)))
print("\nco3 : {}".format(co3))
print("\nco3 length : {}".format(len(co3)))
print("\nco4 : {}".format(co4))
print("\nco4 length : {}".format(len(co4)))

dtm.addForExport(co0, "co0")
dtm.addForExport(co1, "co1")
dtm.addForExport(co2, "co2")
dtm.addForExport(co3, "co3")
dtm.addForExport(co4, "co4")
dtm.addForExport(co5, "co5")
dtm.addForExport(co6, "co6")
dtm.addForExport(co7, "co7")
dtm.addForExport(co8, "co8")
dtm.addForExport(co9, "co9")
"""

"""
#cluster algortihm 20ts w/o 0th
subsample=projection_tsned[19::20]
print("\subsample : {}".format(subsample))

df = pd.DataFrame(subsample)
df = pd.DataFrame(subsample, 
             columns=['xaxis', 
                      'yaxis'])

km = KMeans(n_clusters=20)
y_predicted = km.fit_predict(df[['xaxis','yaxis']])
df['cluster']=y_predicted
print("\nclustercenters : {}".format(km.cluster_centers_))


data=df.to_numpy()
print("\ndatanumpy : {}".format(data))
datalist=data.tolist()
print("\ndatalist : {}".format(datalist))
print("\ndatalist length : {}".format(len(datalist)))


dfcluster = pd.DataFrame(projection_tsned, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfcluster["cluster"]=np.nan
datacluster=dfcluster.to_numpy()
print("\ndatacluster : {}".format(datacluster))
print("\ndatacluster : {}".format(len(datacluster)))

dataclusterlist1=datacluster.tolist()
print("\ndatacluster : {}".format(dataclusterlist1))
print("\ndatacluster : {}".format(len(dataclusterlist1)))

dataclusterlist12 = dataclusterlist1.copy() 

j=19

for i in datalist:

    dataclusterlist12[j]=i
    j+=20
    


print("\nj value  : {}".format(j))
print("\n data clusterlist12: {}".format(dataclusterlist12)) 
print("\n data clusterlist12: {}".format(len(dataclusterlist12)))

dfwithcluster = pd.DataFrame(dataclusterlist12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbefore : {}".format(dfwithcluster))
dfwithcluster["clustersmerged"].fillna(method='bfill', limit=19, inplace=True)
print("\ndataclusterafter : {}".format(dfwithcluster))

cluster0 = dfwithcluster[dfwithcluster.clustersmerged==0]
cluster1 = dfwithcluster[dfwithcluster.clustersmerged==1]
cluster2 = dfwithcluster[dfwithcluster.clustersmerged==2]
cluster3 = dfwithcluster[dfwithcluster.clustersmerged==3]
cluster4 = dfwithcluster[dfwithcluster.clustersmerged==4]
cluster5 = dfwithcluster[dfwithcluster.clustersmerged==5]
cluster6 = dfwithcluster[dfwithcluster.clustersmerged==6]
cluster7 = dfwithcluster[dfwithcluster.clustersmerged==7]
cluster8 = dfwithcluster[dfwithcluster.clustersmerged==8]
cluster9 = dfwithcluster[dfwithcluster.clustersmerged==9]
cluster10 = dfwithcluster[dfwithcluster.clustersmerged==10]
cluster11 = dfwithcluster[dfwithcluster.clustersmerged==11]
cluster12 = dfwithcluster[dfwithcluster.clustersmerged==12]
cluster13 = dfwithcluster[dfwithcluster.clustersmerged==13]
cluster14 = dfwithcluster[dfwithcluster.clustersmerged==14]
cluster15 = dfwithcluster[dfwithcluster.clustersmerged==15]
cluster16 = dfwithcluster[dfwithcluster.clustersmerged==16]
cluster17 = dfwithcluster[dfwithcluster.clustersmerged==17]
cluster18 = dfwithcluster[dfwithcluster.clustersmerged==18]
cluster19 = dfwithcluster[dfwithcluster.clustersmerged==19]

cluster0.drop("clustersmerged", axis=1, inplace=True)
cluster1.drop("clustersmerged", axis=1, inplace=True)
cluster2.drop("clustersmerged", axis=1, inplace=True)
cluster3.drop("clustersmerged", axis=1, inplace=True)
cluster4.drop("clustersmerged", axis=1, inplace=True)
cluster5.drop("clustersmerged", axis=1, inplace=True)
cluster6.drop("clustersmerged", axis=1, inplace=True)
cluster7.drop("clustersmerged", axis=1, inplace=True)
cluster8.drop("clustersmerged", axis=1, inplace=True)
cluster9.drop("clustersmerged", axis=1, inplace=True)
cluster10.drop("clustersmerged", axis=1, inplace=True)
cluster11.drop("clustersmerged", axis=1, inplace=True)
cluster12.drop("clustersmerged", axis=1, inplace=True)
cluster13.drop("clustersmerged", axis=1, inplace=True)
cluster14.drop("clustersmerged", axis=1, inplace=True)
cluster15.drop("clustersmerged", axis=1, inplace=True)
cluster16.drop("clustersmerged", axis=1, inplace=True)
cluster17.drop("clustersmerged", axis=1, inplace=True)
cluster18.drop("clustersmerged", axis=1, inplace=True)
cluster19.drop("clustersmerged", axis=1, inplace=True)

c0=cluster0.to_numpy()
c1=cluster1.to_numpy()
c2=cluster2.to_numpy()
c3=cluster3.to_numpy()
c4=cluster4.to_numpy()
c5=cluster5.to_numpy()
c6=cluster6.to_numpy()
c7=cluster7.to_numpy()
c8=cluster8.to_numpy()
c9=cluster9.to_numpy()
c10=cluster10.to_numpy()
c11=cluster11.to_numpy()
c12=cluster12.to_numpy()
c13=cluster13.to_numpy()
c14=cluster14.to_numpy()
c15=cluster15.to_numpy()
c16=cluster16.to_numpy()
c17=cluster17.to_numpy()
c18=cluster18.to_numpy()
c19=cluster19.to_numpy()

print("\nc0 : {}".format(c0))
print("\nc0 length : {}".format(len(c0)))
print("\nc1 : {}".format(c1))
print("\nc1 length : {}".format(len(c1)))
print("\nc2 : {}".format(c2))
print("\nc2 length : {}".format(len(c2)))
print("\nc3 : {}".format(c3))
print("\nc3 length : {}".format(len(c3)))
print("\nc4 : {}".format(c4))
print("\nc4 length : {}".format(len(c4)))

dtm.addForExport(c0, "c0")
dtm.addForExport(c1, "c1")
dtm.addForExport(c2, "c2")
dtm.addForExport(c3, "c3")
dtm.addForExport(c4, "c4")
dtm.addForExport(c5, "c5")
dtm.addForExport(c6, "c6")
dtm.addForExport(c7, "c7")
dtm.addForExport(c8, "c8")
dtm.addForExport(c9, "c9")
dtm.addForExport(c10, "c10")
dtm.addForExport(c11, "c11")
dtm.addForExport(c12, "c12")
dtm.addForExport(c13, "c13")
dtm.addForExport(c14, "c14")
dtm.addForExport(c15, "c15")
dtm.addForExport(c16, "c16")
dtm.addForExport(c17, "c17")
dtm.addForExport(c18, "c18")
dtm.addForExport(c19, "c19")

#cluster algortihm 20ts  with 0th
subsampleo=projection_tsnedo[20::21]
print("\subsampleo : {}".format(subsampleo))

dfo = pd.DataFrame(subsampleo)
dfo = pd.DataFrame(subsampleo, 
             columns=['xaxis', 
                      'yaxis'])

kmo = KMeans(n_clusters=20)
y_predictedo = kmo.fit_predict(dfo[['xaxis','yaxis']])
dfo['cluster']=y_predictedo
print("\nclustercenterso : {}".format(kmo.cluster_centers_))


datao=dfo.to_numpy()
print("\ndatanumpyo : {}".format(datao))
datalisto=datao.tolist()
print("\ndatalisto : {}".format(datalisto))
print("\ndatalisto length : {}".format(len(datalisto)))


dfclustero = pd.DataFrame(projection_tsnedo, 
             columns=['xaxis', 
                      'yaxis'
                     ])
dfclustero["cluster"]=np.nan
dataclustero=dfclustero.to_numpy()
print("\ndataclustero : {}".format(dataclustero))
print("\ndataclustero : {}".format(len(dataclustero)))

dataclusterlisto1=dataclustero.tolist()
print("\ndataclustero : {}".format(dataclusterlisto1))
print("\ndataclustero : {}".format(len(dataclusterlisto1)))

dataclusterlisto12 = dataclusterlisto1.copy() 

j=20

for i in datalisto:

    dataclusterlisto12[j]=i
    j+=21
    


print("\nj value  : {}".format(j))
print("\n data clusterlisto12: {}".format(dataclusterlisto12)) 
print("\n data clusterlisto12: {}".format(len(dataclusterlisto12)))

dfwithclustero = pd.DataFrame(dataclusterlisto12, columns=['xaxis', 'yaxis', 'clustersmerged'])
print("\ndataclusterbeforeo : {}".format(dfwithclustero))
dfwithclustero["clustersmerged"].fillna(method='bfill', limit=20, inplace=True)
print("\ndataclusteraftero : {}".format(dfwithclustero))

clustero0 = dfwithclustero[dfwithclustero.clustersmerged==0]
clustero1 = dfwithclustero[dfwithclustero.clustersmerged==1]
clustero2 = dfwithclustero[dfwithclustero.clustersmerged==2]
clustero3 = dfwithclustero[dfwithclustero.clustersmerged==3]
clustero4 = dfwithclustero[dfwithclustero.clustersmerged==4]
clustero5 = dfwithclustero[dfwithclustero.clustersmerged==5]
clustero6 = dfwithclustero[dfwithclustero.clustersmerged==6]
clustero7 = dfwithclustero[dfwithclustero.clustersmerged==7]
clustero8 = dfwithclustero[dfwithclustero.clustersmerged==8]
clustero9 = dfwithclustero[dfwithclustero.clustersmerged==9]
clustero10 = dfwithclustero[dfwithclustero.clustersmerged==10]
clustero11 = dfwithclustero[dfwithclustero.clustersmerged==11]
clustero12 = dfwithclustero[dfwithclustero.clustersmerged==12]
clustero13 = dfwithclustero[dfwithclustero.clustersmerged==13]
clustero14 = dfwithclustero[dfwithclustero.clustersmerged==14]
clustero15 = dfwithclustero[dfwithclustero.clustersmerged==15]
clustero16 = dfwithclustero[dfwithclustero.clustersmerged==16]
clustero17 = dfwithclustero[dfwithclustero.clustersmerged==17]
clustero18 = dfwithclustero[dfwithclustero.clustersmerged==18]
clustero19 = dfwithclustero[dfwithclustero.clustersmerged==19]

clustero0.drop("clustersmerged", axis=1, inplace=True)
clustero1.drop("clustersmerged", axis=1, inplace=True)
clustero2.drop("clustersmerged", axis=1, inplace=True)
clustero3.drop("clustersmerged", axis=1, inplace=True)
clustero4.drop("clustersmerged", axis=1, inplace=True)
clustero5.drop("clustersmerged", axis=1, inplace=True)
clustero6.drop("clustersmerged", axis=1, inplace=True)
clustero7.drop("clustersmerged", axis=1, inplace=True)
clustero8.drop("clustersmerged", axis=1, inplace=True)
clustero9.drop("clustersmerged", axis=1, inplace=True)
clustero10.drop("clustersmerged", axis=1, inplace=True)
clustero11.drop("clustersmerged", axis=1, inplace=True)
clustero12.drop("clustersmerged", axis=1, inplace=True)
clustero13.drop("clustersmerged", axis=1, inplace=True)
clustero14.drop("clustersmerged", axis=1, inplace=True)
clustero15.drop("clustersmerged", axis=1, inplace=True)
clustero16.drop("clustersmerged", axis=1, inplace=True)
clustero17.drop("clustersmerged", axis=1, inplace=True)
clustero18.drop("clustersmerged", axis=1, inplace=True)
clustero19.drop("clustersmerged", axis=1, inplace=True)

co0=clustero0.to_numpy()
co1=clustero1.to_numpy()
co2=clustero2.to_numpy()
co3=clustero3.to_numpy()
co4=clustero4.to_numpy()
co5=clustero5.to_numpy()
co6=clustero6.to_numpy()
co7=clustero7.to_numpy()
co8=clustero8.to_numpy()
co9=clustero9.to_numpy()
co10=clustero10.to_numpy()
co11=clustero11.to_numpy()
co12=clustero12.to_numpy()
co13=clustero13.to_numpy()
co14=clustero14.to_numpy()
co15=clustero15.to_numpy()
co16=clustero16.to_numpy()
co17=clustero17.to_numpy()
co18=clustero18.to_numpy()
co19=clustero19.to_numpy()

print("\nco0 : {}".format(co0))
print("\nco0 length : {}".format(len(co0)))
print("\nco1 : {}".format(co1))
print("\nco1 length : {}".format(len(co1)))
print("\nco2 : {}".format(co2))
print("\nco2 length : {}".format(len(co2)))
print("\nco3 : {}".format(co3))
print("\nco3 length : {}".format(len(co3)))
print("\nco4 : {}".format(co4))
print("\nco4 length : {}".format(len(co4)))

dtm.addForExport(co0, "co0")
dtm.addForExport(co1, "co1")
dtm.addForExport(co2, "co2")
dtm.addForExport(co3, "co3")
dtm.addForExport(co4, "co4")
dtm.addForExport(co5, "co5")
dtm.addForExport(co6, "co6")
dtm.addForExport(co7, "co7")
dtm.addForExport(co8, "co8")
dtm.addForExport(co9, "co9")
dtm.addForExport(co10, "co10")
dtm.addForExport(co11, "co11")
dtm.addForExport(co12, "co12")
dtm.addForExport(co13, "co13")
dtm.addForExport(co14, "co14")
dtm.addForExport(co15, "co15")
dtm.addForExport(co16, "co16")
dtm.addForExport(co17, "co17")
dtm.addForExport(co18, "co18")
dtm.addForExport(co19, "co19")
"""

#MDS

#mds = MDS(n_components=2,random_state=0).fit(hidden_states)
#mdsproj = mds.embedding_
#print("\nmdsproj : {}".format(mdsproj))
#print("\nmdsproj datashape: {}".format(mdsproj.shape))
#dtm.addForExport(mdsproj, "mdsprojection")


#UMAP normal
umap2d = umap.UMAP(n_components=2, init='random', random_state=0).fit(hidden_states)
umapproj = umap2d.embedding_
print("\numapproj : {}".format(umapproj))
print("\numapproj datashape: {}".format(umapproj.shape))
dtm.addForExport(umapproj, "umapprojection")


#dtm.writeJson("projection_tsne_nopad_rs" + str(seqLength) + "_ts" + str(randomStateTSNE) + "_p" + str(perplexityTSNE), randomseed)
dtm.writeJson("s" + str(seqLength) + "ts" + "ep" + str(num_epochs) + "bs" + str(batch_size) + "lr" + str(initialLearningRate)
+ "af" + str(activationfn), randomseed)

"""
# Copy testfile as results file
if writePredFile:
  fileName_result = "result_" + modelName +".h5"
  printNotice('Write predictions to file '+ fileName_result)
  copyfile(testFiles[-1], fileName_result)
  # write model prediction and ground truth to results file
  with h5py.File(fileName_result, 'r+') as f5:
    f5['FieldData'][:,:,:,:,          0:  NinputLabel] = prediction.reshape( -1,CellPoints,CellPoints,CellPoints,NinputLabel)
    f5['FieldData'][:,:,:,:,NinputLabel:2*NinputLabel] = test_labels.reshape(-1,CellPoints,CellPoints,CellPoints,NinputLabel)
"""
# Finish
printBanner( 'Finishing after: %.2f [s]' % (time.time()-start_time) )
