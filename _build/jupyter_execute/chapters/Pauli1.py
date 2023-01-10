#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# In this section, we will go through the basic construction of Pauli operators

# # Pauli operator

# ## Construct Pauli operator with its expression

# A **Pauli operator** can be constructed using the `pauli()` constructor.

# In[2]:


paulialg.pauli('XXIYZ')


# By default the operator has a $+1$ phase factor in the front. To specify other phase factors($\pm1$ or $\pm \mathrm{i}$), use `'+'`, `'-'`, `'i'` indicators before the Pauli string.

# In[3]:


paulialg.pauli('-X'), paulialg.pauli('iX'), paulialg.pauli('-iX')


# It is also possible to assign the phase factor by scalar mutiplication.

# In[4]:


-paulialg.pauli('X'), 1j*paulialg.pauli('X')


# ## Other methods to construct a Pauli operator

# You can construct a Pauli operator from a tuple / list / array of indices (`0` = `I`, `1` = `X`, `2` = `Y`, `3` = `Z`)

# In[5]:


paulialg.pauli((0,1,2,3)), paulialg.pauli([0,1,2,3]), paulialg.pauli(np.array([0,1,2,3]))


# Or you can construct a Pauli operator from a dictionary that maps positions to indices. (*Note*: using this method must also provide the total number of qubits as the second argument, because the qubit number can not be infered from the dictionary alone.)

# In[6]:


paulialg.pauli({1:'X', 4:'Y', 5:'Z'}, 6), paulialg.pauli({1:1, 4:2, 5:3}, 6)


# ## Size information

# For Pauli operator, `.N` returns the number of qubits (size of system) that the operator acts on.

# In[7]:


paulialg.pauli('IXYIXI').N


# # Pauli operator list

# A **list of Pauli operators** can be constructed by the `paulis()` constructor.

# In[8]:


paulialg.paulis('iX', '-iY', 'Z')


# It can also take a generator and iterate through its elements to construct a list of Pauli operators.

# In[9]:


paulialg.paulis(paulialg.pauli({i:'Z'}, 4) for i in range(4))


# It can also take a iterable (tuple / list / set) and convert it to a list of Pauli operators.

# In[10]:


lists = ['iX', '-iY', 'Z']
paulialg.paulis(lists)


# ## Size information

# For Pauli operator list, `.L` returns the number of operators in the list and `.N` returns of the number fo qubits in the system.

# In[11]:


plst = paulialg.paulis('II','XX','YY','ZZ')
plst.L, plst.N


# We can also return the number of operators in the list by naive python `len()` function

# In[12]:


len(plst)


# ## Selection and Slicing of Pauli List

# Select a single element in the Pauli operator list.

# In[13]:


plst[1]


# Select a range of operators in the Pauli operator list: the slicing is the same as python array

# In[14]:


plst[0:3]


# In[15]:


plst[::2]


# It is also allow to be selected by a index array or a boolean mask.

# In[16]:


plst[np.array([2,1,1,0,3])]


# In[17]:


plst[np.array([True,False,False,True])]


# # Pauli Polynomials

# Pauli operators can be linearly combined in to a **Pauli polynomial**.

# In[18]:


paulialg.pauli('XX') + paulialg.pauli('YY') - 0.5 * paulialg.pauli('ZZ')


# <div class="alert alert-block alert-success">
# Adding Pauli operators with any number, the number will be promoted to the number times identity operator automatically. For example, a projection operator can be written as
# </div>

# In[19]:


(paulialg.pauli('ZZ') + 1)/2


# Operators can be summed up with python built-in function `sum()`.

# In[20]:


sum(paulialg.paulis('II','XX','YY','ZZ'))

