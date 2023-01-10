#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Clifford Layers

# `CliffordLayer` has the following attributes:
# - gates(list): contains a list of `CliffordGate`
# - prev_layer: Default `None`. It will be automatically setup in `CliffordCircuit`
# - next_layer: Default `None`. It will be automatically setup in `CliffordCircuit`
# - forward_map
# - backward_map

# `CliffordLayer` can take `CliffordGates` by `layer.take(gate)`:

# In[2]:


circlayer = circuit.CliffordLayer()


# In[3]:


circlayer.take(circuit.CliffordGate(0,1))
circlayer.take(circuit.CliffordGate(1,3))


# In[4]:


circlayer


# In[5]:


psi=stabilizer.random_clifford_state(4)
print(psi)


# In[6]:


circlayer.forward(psi)


# <div class="alert alert-block alert-success">
# If the forward map and backward map for a gate is Null, then it will be assigned a <b> different </b>random clifford map each time when use calls forward() or backward()
# </div>

# In[ ]:




