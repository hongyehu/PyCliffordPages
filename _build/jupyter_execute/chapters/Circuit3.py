#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Clifford Circuit

# `CliffordCircuit` is the high level API to assemble gates and layers, and it **automatically** calculate number of qubits in the system
# It has attributes:
# - first_layer
# - last_layer
# - forward_map
# - backward_map
# 
# When `CliffordCircuit` is initialized, a null `CliffordLayer()` will be initiated.
# `CliffordCircuit` can take `CliffordGate` by `circ.take(gate)`.
# 
# If the gate is independent from the current layer, it will be added. Otherwise, the circuit will create a new layer and add the gate.

# In[2]:


circ = circuit.CliffordCircuit()


# In[3]:


circ.take(circuit.CliffordGate(0,1))


# In[4]:


circ.take(circuit.CliffordGate(9,10))


# In[5]:


circ.N


# In[ ]:




