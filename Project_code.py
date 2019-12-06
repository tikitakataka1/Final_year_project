#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import math
import random


# In[2]:


#data generation functions
def doubler (v, e):
    # Takes a node and splits into two descendants with probability epsilon of switching value
    t = np.array([])
    for i in range(0, len(v)):
        t = np.append(t, [np.random.choice([v[i],-v[i]], p = [1-e, e]), np.random.choice([v[i],-v[i]], p = [1-e, e])]).astype(int)
    
    return t

def leaf_maker (v, e, B):
    # Takes a node and splits into B descendants with probability epsilon of switching value
    # v is parent node, e is epsilon and B is number of descendants
    t = np.array([])
    for i in range(0, len(v)):
        to_add = np.array([])
        for nodes in range(B):
            to_add = np.append(to_add, np.random.choice([v[i],-v[i]], p = [1-e, e]))
        t = np.append(t,to_add).astype(int)
    
    return t

def sample_generator(e ,P, B, n):
    # Produces leaf nodes for n data points
    # e is epsilon, P is total number of output nodes, B is number of descendants, n is number of datapoints
    levels = int((math.log(P, B)))
    result = np.zeros((1,P))
    features = np.array([])
    for n in range(n):
        v = np.array([np.random.choice([1,-1], p = [0.5,0.5])])
        features = np.append(features, v)
        for level in range(0, levels):
            v = leaf_maker(v,e,B)
            # B can be set to change with level, would need to input B as a matrix etcetc
        result = np.vstack([result,v])
    
    return features, result[1:,:]  


# In[3]:


#forward function for passing on inputs and generating predictions
def forward(x, w_1, w_2):
    h = np.matmul(w_1, x)
    return np.matmul(w_2, h)


# In[4]:


#squared error calculation function
def error(w_1, w_2, animals):
    error = 0
    for animal in animals:
        y_hat = forward(animal.input, w_1, w_2)
        y = animal.feature
        error = error + (y - y_hat)**2
    return error


# In[5]:


#weight matrix gradient calculation function
def gradient(i, w_1, w_2, n_1, n_2, n_3, animals):
    #item/ particular animal performing the learning on
    #separate input and output
    x = animals[i].input
    y = animals[i].feature

    h = np.matmul(w_1, x)
    y_hat = np.matmul(w_2, h)

    x_matrix = np.reshape(x, (x.shape[0],1))
    h_matrix = np.reshape(h, (h.shape[0],1))
    y_difference = np.reshape((y - y_hat), (y.shape[0], 1))
    
    delta_w_1 = np.matmul(np.transpose(w_2) ,np.matmul(y_difference, np.transpose(x_matrix)))
    delta_w_2 = np.matmul(y_difference, np.transpose(h_matrix))
    
    return delta_w_1, delta_w_2


# In[6]:


#variables for data generation
epsilon = 0.01 # small probability of value flipping 
P = 16 #total leaf nodes in tree
B = 2 #number of descendants
total_data = 10 #number of data points


# In[7]:


#generate sample of data
feature, item = sample_generator(epsilon, P, B, total_data)


# In[8]:


#Animal class that encapsulates data generated from tree (animals and their features)
class Animal(object):
    def __init__(self, animal_n, total_n, feature):
        self.input = np.zeros(total_n,dtype=np.float64)
        self.input[animal_n] = 1.0
        self.feature = feature
    


# In[9]:


#variables for size of matrices and learning process
n_1 = 16 #number of inputs/ item/ animals
n_2 = 5 #number of hidden layer nodes
n_3 = 10 #number of features/ output
trial_n = 500 # number of trials for learning process
lamda = 0.1 #learning rate of backpropagation


# In[10]:


#creating a list of n_1 pairs of item/feature
animals = np.array([])
for i in range(0,n_1):
    animals = np.append(animals, [Animal(i,n_1,item[:,i])])
#animals[0].feature   


# In[11]:


#initial random weight matrices
w_1 = np.random.rand(n_2, n_1)
w_2 = np.random.rand(n_3, n_2)


# In[12]:


#loop with updates of weights and printing updated errors at each step
for trial_c in range(0,trial_n):
    dw_1, dw_2 = gradient(random.randint(0,n_1-1), w_1, w_2, n_1, n_2, n_3, animals)
    w_1 = w_1 + lamda * dw_1
    w_2 = w_2 + lamda * dw_2
    print(error(w_1, w_2, animals))


# In[ ]:




