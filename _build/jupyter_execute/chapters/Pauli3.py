#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Link to QuTip Library

# Pauli operators can be easily converted to the `Qobj` in qutip library
# - `Pauli.to_qupit()`
# - `PauliList.to_qutip()`
# - `PauliMonomial.to_qutip()`
# - `PauliPolynomial.to_qutip()`

# In[2]:


paulialg.pauli('XY').to_qutip()


# In[3]:


paulialg.paulis('XY','ZZ').to_qutip()


# In[4]:


((2+3j)*paulialg.pauli('XY')).to_qutip()


# In[5]:


((2+3j)*paulialg.pauli('XY')+(1.5)*paulialg.pauli('ZZ')).to_qutip()


# In[ ]:




