#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.insert(0, '..')
import numpy as np
import qutip as qt
import src
from src import (utils, paulialg, stabilizer, circuit)


# # Pauli Algebra

# ## Dot Productor (Matrix Multiplication)

# Dot productor (composition) of Pauli operators is implemented as the matrix multiplication `matmul`, which can be implemented using the operand `@`.

# In[2]:


paulialg.pauli('X') @ paulialg.pauli('Y'), paulialg.pauli('Y') @ paulialg.pauli('X')


# Dot product of Pauli polynomials will be expanded.

# In[3]:


poly = paulialg.pauli('XX') + paulialg.pauli('YY') - 0.5 * paulialg.pauli('ZZ')
poly @ poly


# Terms will not be combined automatically. To combine them, the `.reduce()` method should be explicitly called.

# In[4]:


(poly @ poly).reduce()


# ## Trace of Pauli operators

# - `Pauli.trace()` will return the trace of a Pauli operator
#  - `PauliList.trace()` will return the trace of a list of Pauli operators
#  - `PauliPolynomial.trace()` will return the trace of a Pauli polynomial

# In[5]:


paulialg.pauli('II').trace()


# In[6]:


paulialg.paulis('II','YY').trace()


# In[7]:


(3*paulialg.pauli('II')).trace()


# In[8]:


(3*paulialg.pauli('II')+(3+2.5j)*paulialg.pauli('II')).trace()


# ## Weight (number of non-identity support)

# - `Pauli.weight()` will return the weight (the support of non identity operators) of a Pauli operator
# - `PauliList.weight()` will return the weight of a list of Pauli operators

# In[9]:


paulialg.pauli('IXIYZII').weight()


# In[10]:


paulialg.paulis('IXIYZII','IXIIIII').weight()


# ## Type conversion

# Automatic type conversion enables the algebra to be carried out among different classes with great flexibiliity.
# * When `Pauli` is multiplied (`*`) by a generic number (beyond powers of the imaginary unit), it is converted to `PauliMonomial`.
# * When `Pauli` or `PauliMonomial` is added (`+`) or subtracted (`-`) with other Pauli objects, they are converted to `PauliPolynomial`.
# * The dot product (`@`) generally returns `PauliPolynomial`, unless the two Pauli objects are both `Pauli`, in which case it returns `Pauli`.

# # Clifford Transformation

#  `PauliList` provides useful methods to implement Clifford transformations efficiently on all Pauli operators together. The same methods are available to all its subclasses (including `PauliPolynomial`, `CliffordMap`, `StabilizerState`).

# ## Clifford Rotation

# A Clifford rotation is a $\mathbb{Z}_4$ rotation in the Clifford group generated by a single Pauli operator, which takes the form of
# $$
# U=e^{\frac{i\pi}{4}\sigma}=\frac{1}{\sqrt{2}}(1+i \sigma)
# $$
# Every Pauli operator is transformed by $\sigma \to U^\dagger \sigma U$. The Clifford rotation can be applied by the method `.rotate_by(gen)` (given the generator `gen`). The operation is in-place (meaning that the operators in the Pauli list will be modified).

# In[11]:


paulialg.paulis('II','XX','YY','ZZ').rotate_by(paulialg.pauli('XI'))


# ## Clifford Map

# A Clifford map is a generic clifford transformation by specifying how each single Pauli operator gets mapped to. It can be listed as a table

# In[12]:


cmap = stabilizer.random_clifford_map(2)
cmap


# It can be applied by the method `.transform_by(cmap)` (given the Clifford map `cmap`). 

# In[13]:


paulialg.paulis('II','XX','YY','ZZ').transform_by(cmap)


# ## Masked Transformation

# Clifford transformation can be applied to a subsystem of qubits specified by a mask.

# In[14]:


mask = np.array([True,False,False,True])
paulialg.paulis('IIII','XXXX','YYYY','ZZZZ').rotate_by(paulialg.pauli('XY'), mask)


# In[15]:


mask = np.array([True,False,False,True])
paulialg.paulis('IIII','XXXX','YYYY','ZZZZ').transform_by(cmap, mask)


# In[ ]:



