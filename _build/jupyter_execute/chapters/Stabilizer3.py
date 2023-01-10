#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Methods for stabilizer states

# ## Measurement

# `StabilizerState.measure(obs)` measure the stabilizer state on a set of commuting observables.
# 
# **Parameters:**
# * `obs` - Observables to measure. The following types are supported:
#     * `PauliList` - a list of Pauli operators (user must ensure that operators in the list are commuting, otherwise they can not measured simutaneously).
#     * `StabilizerState` - stabilizers of a stabilizer state is always commuting, which can be treated as commuting observables for measurement.
# 
# **Returns:**
# * `out` - measuremnt outcome, can only be $0$, $1$ for independent Pauli observables on stabilizer state, where 0 means positive (+1) eigenvalue, and 1 means negative (-1) eigenvalue.
# * `log2prob` - the log2 of the probability of realizing this particular outcome.

# In[2]:


state = stabilizer.ghz_state(3)
state


# In[3]:


state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# In the above example, I created a GHZ state, and did single qubit Z-basis measurements on each of the qubit. We get -1 for all qubits with probility $2^{-1}=0.5$

# <div class="alert alert-block alert-danger">
# Measurement will <b>in place </b> change the state, as measurement will collapse the quantum state.
# </div>

# In[4]:


state = stabilizer.ghz_state(3)
state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# In[5]:


state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# We see the second measurement will return the same measurement result with 100% probability

# ## Expectation

# `StabilizerState.expect()` provide fast algorithm to evaluate expectation value of:
# - Pauli operator
# - Pauli Monomial/Polynomial
# - Overlap between stabilizer states <font color='red'>Warning: currently it only supports pure state overlap with general stabilizer states.</font>

# In[6]:


state = stabilizer.ghz_state(5)


# In[7]:


state.expect(paulialg.paulis('XXXXX','IZIII','-ZZIII'))


# In[8]:


pauli_poly = 0.5*paulialg.pauli('XXXXX')+0.2j*paulialg.pauli('-ZZIII')


# In[9]:


state.expect(pauli_poly)


# ## Overlap between two stabilizer states (fidelity)

# In[10]:


state = stabilizer.ghz_state(3)
state2 = stabilizer.random_clifford_state(3)
print("State overlap is:", state.expect(state2))


# In[11]:


tate = stabilizer.ghz_state(3)
state2 = stabilizer.random_clifford_state(3)
state2.set_r(1)
print("State overlap is:", state.expect(state2))


# ## The probability of getting a bit-string readout (Bit-string probability)

# `StabilizerState.get_prob(bitstring)` will return the probability of measuring given bitstring at current stabilizer state.
# **Input**
# - bitstring: Integer type 1D array
# **Output**
# - probability

# In[12]:


state = stabilizer.ghz_state(625)


# In[13]:


state.get_prob(np.ones(625))


# ## Transform stabilzier state by rotation/Clifford transformation

# As a derived class of `PauliList`, `StabilizerState` also support `StabilizerState.rotate_by(pauli)` and `StabilizerState.transform_by(clifford_map)`

# In[14]:


rho = stabilizer.ghz_state(4)


# In[15]:


rho.rotate_by(paulialg.pauli([1,3,1,0]))


# In[16]:


rho.transform_by(stabilizer.random_clifford_map(4))


# ## Sample stabilizers from the stabilizer group

# `Stabilizer.sample(L)` will sample $L$ stabilizers in the stabilizer group

# In[17]:


rho = stabilizer.ghz_state(4)
rho.sample(4)


# ## Get density matrix of a stabilizer state

# @property `StabilizerState.density_matrix` will return density matrix of stabilizer state as `PauliPolynomial`

# In[18]:


stabilizer.ghz_state(2).density_matrix


# ## Calculate Entropy of a stabilizer state

# `StabilizerState.entropy(subsys)` will calculate the second Renyi entropy of the stabilizer state on subregion.
# **Parameter**
# - `subsys`: List containing the location of region

# In[19]:


state = stabilizer.random_clifford_state(20)


# In[20]:


state.entropy([1,5,10])


# ## Copy a stabilizer state

# `StabilizerState.copy()` returns a copy of the state, such that the original state will not be touch by modification on the copy state. It is useful to copy the state for measurement (as measurement changes the state).
# 
# Example:

# In[21]:


state = stabilizer.random_clifford_state(4).copy()


# In[ ]:




