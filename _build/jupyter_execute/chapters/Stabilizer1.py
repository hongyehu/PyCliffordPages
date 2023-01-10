#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Construct Clifford Maps

# `identity_map(N)` constructs an identity Clifford map on $N$ qubits.

# In[2]:


stabilizer.identity_map(4)


# `random_pauli_map(N)` samples a random Clifford map made of random single-qubit Clifford gates on $N$ qubits, i.e. $U=\prod_i U_i\in\mathrm{Cl}(2)^N$. Each realization specifies a random local Pauli basis.

# In[3]:


stabilizer.random_pauli_map(4)


# `random_clifford_map(N)` samples a globally random Clifford map on $N$ qubits, i.e. $U\in\mathrm{Cl}(2^N)$. Each realization specifies a random global stabilizer basis.

# In[4]:


stabilizer.random_clifford_map(4)


# `clifford_rotation_map(N)` constructs a Clifford map based for a Clifford rotation given its generator.

# In[5]:


stabilizer.clifford_rotation_map('-XXYZ')


# # Construct Stabilizer States

# `maximally_mixed_state(N)` constructs a $N$-qubit maximally mixed state (by setting the density matrix to full rank).
# $$\rho=2^{-N}\mathbb{1}.$$

# In[6]:


stabilizer.maximally_mixed_state(4)


# `zero_state(N)` constructs a $N$-qubit all-zero state 
# $$\rho=|0\cdots0\rangle\langle 0\cdots0|=\prod_{i}\frac{1+Z_i}{2}.$$

# In[7]:


stabilizer.zero_state(4)


# `one_state(N)` constructs a $N$-qubit all-one state 
# $$\rho=|1\cdots1\rangle\langle 1\cdots1|=\prod_{i}\frac{1-Z_i}{2}.$$

# In[8]:


stabilizer.zero_state(4).ps


# `ghz_state(N)` constructs a $N$-qubit GHZ state
# $$\rho = |\Psi\rangle\langle\Psi|, \qquad \text{with }|\Psi\rangle=\frac{1}{\sqrt{2}}(|0\cdots0\rangle+|1\cdots1\rangle).$$

# In[9]:


stabilizer.ghz_state(4)


# `random_pauli_map(N)` samples a $N$ qubit random Pauli state.
# $$\rho=U|0\cdots0\rangle\langle 0\cdots0|U^\dagger,\qquad\text{with }U\in \mathrm{Cl}(2)^N.$$

# In[10]:


stabilizer.random_pauli_map(4)


# `random_clifford_map(N)` samples a $N$ qubit random Clifford (random stabilizer) state.
# $$\rho=U|0\cdots0\rangle\langle 0\cdots0|U^\dagger,\qquad\text{with }U\in \mathrm{Cl}(2^N).$$

# In[11]:


stabilizer.random_clifford_state(4)


# `stabilizer_state(...)` is a universal constructor of stabilizer state by specifying all stabilizers.

# In[12]:


stabilizer.stabilizer_state('XXY','ZZI','IZZ')


# # Construct Stabilizer States by Checker Matrix

# The user can also construct stabilizer state by low-level constructor `StabilizerState(gs, ps, r=0)`:
# 
# **Parameters**
# - `gs: int (2*N, 2*N)`: strings of Pauli operators in the stabilizer tableau.
# - `ps: int (2*N)`: phase indicators (should only be 0 or 2).
# - `r:  int`: number of logical qubits (log2 rank of density matrix)'''
# 
# **Returns**
# - Object of `StabilizerState`

# In[13]:


tmp_state = stabilizer.random_clifford_state(3)
print(tmp_state)


# In[14]:


gs = tmp_state.gs
ps = tmp_state.ps


# In[15]:


stabilizer.StabilizerState(gs=gs,ps=ps)


# A hack to inspect the full stabilizer tableau is by converting `StabilizerState` to `PauliList` by

# In[16]:


stabilizer.stabilizer_state('XXY','ZZI','IZZ')[:]


# # State-Map convertion

# Stabilizer states and Clifford maps can be mapped to each other.

# In[17]:


rho = stabilizer.stabilizer_state('XXX','ZZI','IZZ')
print("quantum state: \n", rho)


# In[18]:


rho.to_map()


# And Clifford map can be converted back to the stabilizer state.

# In[19]:


rho.to_map().to_state()


# * `.to_map()` and `.to_state()` will make **new copies** of Pauli string data in the memory.

# <div class="alert alert-block alert-danger">
# The information about the rank of the density matrix is lost in the Clifford map, so the back conversion will result in a zero rank stabilizer state.
# </div>

# In[ ]:




