from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import csv
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from pandas import DataFrame as df


import argparse
import time

import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

from tensorflow.python.keras import models
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Dropout
NGRAM_RANGE = (1, 2)

# Limit on the number of features. We use the top 20K features.
TOP_K = 20000

# Whether text should be split into word or character n-grams.
# One of 'word', 'char'.
TOKEN_MODE = 'word'

# Minimum document/corpus frequency below which a token will be discarded.
MIN_DOCUMENT_FREQUENCY = 2
#converts pdf, returns its text content as a string
def convert(fname, pages=None):
    data_path='docs'
    fname=os.path.join(data_path,fname)
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = io.StringIO() #reads and writes a string buffer
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue() 
    output.close
    return text 


# Vectorization parameters
# Range (inclusive) of n-gram sizes for tokenizing text.


def ngram_vectorize(train_texts, train_labels, val_texts):
    """Vectorizes texts as n-gram vectors.

    1 text = 1 tf-idf vector the length of vocabulary of unigrams + bigrams.

    # Arguments
        train_texts: list, training text strings.
        train_labels: np.ndarray, training labels.
        val_texts: list, validation text strings.

    # Returns
        x_train, x_val: vectorized training and validation texts
    """
    # Create keyword arguments to pass to the 'tf-idf' vectorizer.
    kwargs = {
            'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
            'dtype': 'int32',
            'strip_accents': 'unicode',
            'decode_error': 'replace',
            'analyzer': TOKEN_MODE,  # Split text into word tokens.
            'min_df': MIN_DOCUMENT_FREQUENCY,
    }
    vectorizer = TfidfVectorizer(**kwargs)

    # Learn vocabulary from training texts and vectorize training texts.
    x_train = vectorizer.fit_transform(train_texts)
    
    # Vectorize validation texts.
    x_val = vectorizer.transform(val_texts)
    # Select top 'k' of the vectorized features.
    selector = SelectKBest(f_classif, k=min(TOP_K, x_train.shape[1]))
    selector.fit(x_train, train_labels)
    
    x_train = selector.transform(x_train)
    
    x_val = selector.transform(x_val).astype('float32')
    return x_train, x_val


# In[80]:


def _get_last_layer_units_and_activation(num_classes):
    """Gets the # units and activation function for the last network layer.

    # Arguments
        num_classes: int, number of classes.

    # Returns
        units, activation values.
    """
    
    activation = 'softmax'
    units = num_classes
    return units, activation


# In[84]:




def mlp_model(layers, units, dropout_rate, input_shape, num_classes):
    """Creates an instance of a multi-layer perceptron model.

    # Arguments
        layers: int, number of `Dense` layers in the model.
        units: int, output dimension of the layers.
        dropout_rate: float, percentage of input to drop at Dropout layers.
        input_shape: tuple, shape of input to the model.
        num_classes: int, number of output classes.

    # Returns
        An MLP model instance.
    """
    op_units, op_activation = _get_last_layer_units_and_activation(num_classes)
    #print(op_activation)
    #print(op_units)
    model = models.Sequential()
    model.add(Dropout(rate=dropout_rate, input_shape=input_shape))
 #   print('!!!')
    for _ in range(layers-1):
        model.add(Dense(units=units, activation='relu'))
        model.add(Dropout(rate=dropout_rate))

    model.add(Dense(units=op_units, activation=op_activation))
  #  print('!!!!')
    return model


# In[88]:



FLAGS = None
def train_ngram_model(train_texts, train_labels,val_texts,val_labels,
                      learning_rate=1e-3,
                      epochs=1000,
                      batch_size=10,
                      layers=2,
                      units=64,
                      dropout_rate=0.2):
    num_classes = 2
    unexpected_labels = [v for v in val_labels if v not in range(num_classes)]
    if len(unexpected_labels):
        raise ValueError('Unexpected label values found in the validation set:'
                         ' {unexpected_labels}. Please make sure that the '
                         'labels in the validation set are in the same range '
                         'as training labels.'.format(
                             unexpected_labels=unexpected_labels))

    # Vectorize texts.
    x_train, x_val = ngram_vectorize(
        train_texts, train_labels, val_texts)

    # Create model instance.
    model = mlp_model(layers=layers,
                                  units=units,
                                  dropout_rate=dropout_rate,
                                  input_shape=x_train.shape[1:],
                                  num_classes=num_classes)

    # Compile model with learning parameters.
   # if num_classes == 2:
    #    loss = 'binary_crossentropy'
    #else:
    loss = 'sparse_categorical_crossentropy'
    optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
    model.compile(optimizer=optimizer, loss=loss, metrics=['acc'])
    #print('!!')
    # Create callback for early stopping on validation loss. If the loss does
    # not decrease in two consecutive tries, stop training.
    callbacks = [tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=2)]

    # Train and validate model.
    history = model.fit(
            x_train,
            train_labels,
            epochs=epochs,
            callbacks=callbacks,
            validation_data=(x_val, val_labels),
            verbose=2,  # Logs once per epoch.
            batch_size=batch_size)

    # Print results.
    history = history.history
    #print('Validation accuracy: {acc}, loss: {loss}'.format(
     #       acc=history['val_acc'][-1], loss=history['val_loss'][-1]))

    # Save model.
    model.save('classification_model_rc.h5')
    return history['val_acc'][-1], history['val_loss'][-1]



def main_func():
    data1=pd.read_csv('cases-rentcontrol.csv',delimiter=',')
    data=pd.DataFrame(data1)
    cases=data['Case']
    tags=data['Tag']
    case_train,case_test,tag_train,tag_test=train_test_split(cases,tags,train_size=0.75,random_state=42)
    text_train=[]
    text_test=[]
    for i in case_train:
        d=convert(i)
        text_train.append(d)
    for j in case_test:
        d=convert(j)
        text_test.append(d)
    number_of_samples=len(data)
    number_of_classes= data['Tag'].nunique()
    train_ngram_model(text_train,tag_train,text_test,tag_test)
    file=open('doc3.txt','r',encoding='utf-8')
    e=file.read()
    check_data=[]
    check_data.append(e)
    x_train,x_val=ngram_vectorize(text_train,tag_train,check_data)
    model=models.load_model('classification_model_rc.h5')
    if(model.predict_classes(x_val)[0]==0):
        cat_name='Eviction'
    else:
        cat_name='No eviction'
    doc_name= [i.split(', ', 1)[0] for i in check_data]
    return cat_name,model.predict_classes(x_val)[0]