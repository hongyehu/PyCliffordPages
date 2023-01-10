#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Methods for Clifford maps

# ## Embedding small Clifford map into larger map

# `.embed(small_map, mask)` provides the method to embed a smaller Clifford map on a subset of qubits to the current Clifford map. This is a **in-place** operation. The Clifford map object that provide this method will get modified under the embedding.
# 
# **Parameters:**
# * `small_map` is a `CliffordMap` object supported on a subset of qubits.
# * `mask` is a boolean array specifying the subset of qubits.

# In[2]:


cmap = stabilizer.identity_map(6)
cmap


# In[3]:


cmap.embed(stabilizer.random_clifford_map(3), np.array([True,False,False,True,True,False]))


# ## Map Composition

# `.compose(other)` returns the composition of the current Clifford map with another Clifford map. This will return a new Clifford map without modifying either of the input maps. The Clifford map object which initiates this method will be the preceeding map in the composition. 
# 
# **Parameters:**
# * `other` - another `CliffordMap`.

# In[4]:


cmap.compose(stabilizer.random_clifford_map(6))


# ## Map Inversion

# `.inverse()` returns the inverse of the current Clifford map. This will return a new Clifford map withoutt modifying the original map. The inverse map is such that its composition with the original map must be identity

# In[5]:


cmap = stabilizer.clifford_rotation_map('Y')
cmap


# In[6]:


cmap.inverse()


# In[ ]:




