#!/usr/bin/env python
# coding: utf-8

# In[1]:


from context import *


# The design of 'PyClifford' is the hierarchy of: 
# 
# * Pauli String and its algebra
# 
# * Stabilizer states and Clifford Unitarys Map (state-map duality)
# 
# * Circuit 
# 
# * Device

# # Pauli Algebra (`paulialg`)

# This tutorial contains two part: 1. the basic usage of PauliAlgebra class and 2. its implementation details

# ## Basic Usage

# ----

# ### Operator Construction

# #### Pauli Operator

# A **Pauli operator** can be constructed using the `pauli()` constructor.

# In[2]:


paulialg.pauli('XXIYZ')


# **Specify the Phase Factor**
# 
# By default the operator has a $+1$ phase factor in the front. To specify other phase factors($\pm1$ or $\pm \mathrm{i}$), use `'+'`, `'-'`, `'i'` indicators before the Pauli string.

# In[3]:


paulialg.pauli('-X'), paulialg.pauli('iX'), paulialg.pauli('-iX')


# It is also possible to assign the phase factor by scalar mutiplication.

# In[4]:


-paulialg.pauli('X'), 1j*paulialg.pauli('X')


# Other methods to specify a Pauli string:
# * construct from a tuple / list / array of indices (`0` = `I`, `1` = `X`, `2` = `Y`, `3` = `Z`)

# In[5]:


paulialg.pauli((0,1,2,3)), paulialg.pauli([0,1,2,3]), paulialg.pauli(numpy.array([0,1,2,3]))


# * construct from a dictionary that maps positions to indices. (*Note*: using this method must also provide the total number of qubits as the second argument, because the qubit number can not be infered from the dictionary alone.)

# In[19]:


paulialg.pauli({1:'X', 4:'Y', 5:'Z'}, 6), paulialg.pauli({1:1, 4:2, 5:3}, 6),


# #### Pauli Operator List

# A **list of Pauli operators** can be constructed by the `paulis()` constructor.

# In[23]:


paulialg.paulis('iX', '-iY', 'Z')


# It can take a generator and iterate through its elements to construct a list of Pauli operators.

# In[26]:


paulialg.paulis(paulialg.pauli({i:'Z'}, 4) for i in range(4))


# It can also take a iterable (tuple / list / set) and convert it to a list of Pauli operators.

# In[28]:


lists = ['iX', '-iY', 'Z']
paulialg.paulis(lists)


# #### Size information

# For Pauli operator, `.N` returns the number of qubits (size of system) that the operator acts on.

# In[30]:


paulialg.pauli('IXYIXI').N


# For Pauli operator list, `.L` returns the number of operators in the list and `.N` returns of the number fo qubits in the system.

# In[32]:


plst = paulialg.paulis('II','XX','YY','ZZ')
plst.L, plst.N


# We can also return the number of operators in the list by naive python `len()` function

# In[33]:


len(plst)


# #### Selection and Slicing

# Select a single element in the Pauli operator list.

# In[34]:


plst[1]


# Select a range of operators in the Pauli operator list: the slicing is the same as python array

# In[35]:


plst[0:3]


# In[36]:


plst[::2]


# It is also allow to be selected by a index array or a boolean mask.

# In[37]:


plst[numpy.array([2,1,1,0,3])]


# In[38]:


plst[numpy.array([True,False,False,True])]


# ---

# ### Operator Algebra

# #### Scalar Product

# Pauli operator and operator list can be multiplied with a scalar.
# * If the scalar is a phase factor (as power of imaginary unit), the phase will be multiplied to the operator.

# In[40]:


-paulialg.pauli('X'), 1j*paulialg.pauli('X')


# For operator list, the scalar multiplication broadcast to every operator in the list.

# In[43]:


-paulialg.paulis('II','XX','YY','ZZ')


# * if the scalar is beyond a phase factor, the Pauli operator will be promoted to a **Poly monomial** (i.e. Pauli operator equipted with a complex coefficient.)

# In[44]:


2*paulialg.pauli('X'), -1.5*paulialg.pauli('X'), (-0.3+0.4j)*paulialg.pauli('X')


# In[45]:


a = (-0.3+0.4j)*paulialg.pauli('X')


# In[48]:


a.c


# <div class="alert alert-block alert-danger">
# However, Pauli opreator list <b>does not support</b> scalar multiplication beyond the four phase factors. (Because there is no canonical meanding for a list of Pauli monomials).
# </div>

# #### Linear Combination

# Pauli operators can be linearly combined in to a **Pauli polynomial**.

# In[54]:


paulialg.pauli('XX') + paulialg.pauli('YY') - 0.5 * paulialg.pauli('ZZ')


# <div class="alert alert-block alert-success">
# Adding Pauli operators with any number, the number will be promoted to the number times identity operator automatically. For example, a projection operator can be written as
# </div>

# In[56]:


(paulialg.pauli('ZZ') + 1)/2


# Operators can be summed up with python built-in function `sum()`.

# In[59]:


sum(paulialg.paulis('II','XX','YY','ZZ'))


# #### Dot Productor (Matrix Multiplication)

# Dot productor (composition) of Pauli operators is implemented as the matrix multiplication `matmul`, which can be implemented using the operand `@`.

# In[61]:


paulialg.pauli('X') @ paulialg.pauli('Y'), paulialg.pauli('Y') @ paulialg.pauli('X')


# <div class="alert alert-block alert-success">
# The dot product of two Pauli operators is still a Pauli operator. However if any one of them is Pauli monomial, the result will also be Pauli monomial.
# </div>

# In[63]:


(3*paulialg.pauli('X')) @ paulialg.pauli('X'), (2*paulialg.pauli('X')) @ (3*paulialg.pauli('Z'))


# Dot product of Pauli polynomials will be expanded.

# In[65]:


poly = paulialg.pauli('XX') + paulialg.pauli('YY') - 0.5 * paulialg.pauli('ZZ')
poly @ poly


# Terms will not be combined automatically. To combine them, the `.reduce()` method should be explicitly called.

# In[66]:


(poly @ poly).reduce()


# #### Trace

#  - `Pauli.trace()` will return the trace of a Pauli operator
#  - `PauliList.trace()` will return the trace of a list of Pauli operators
#  - `PauliMonomial.trace()` will return the trace of a Pauli monomial
#  - `PauliPolynomial.trace()` will return the trace of a Pauli polynomial

# In[4]:


paulialg.pauli('II').trace()


# In[6]:


paulialg.paulis('II','YY').trace()


# In[8]:


(3*paulialg.pauli('II')).trace()


# In[9]:


(3*paulialg.pauli('II')+(3+2.5j)*paulialg.pauli('II')).trace()


# #### Weight

# - `Pauli.weight()` will return the weight (the support of non identity operators) of a Pauli operator
# - `PauliList.weight()` will return the weight of a list of Pauli operators

# In[10]:


paulialg.pauli('IXIYZII').weight()


# In[12]:


paulialg.paulis('IXIYZII','IXIIIII').weight()


# ---

# ### Properties and Type Conversion

# There are four different types of objects involved in the above discussion.
# * `Pauli` (base class): a Pauli operator (in the Pauli group).
#     * `PauliMonomial` (subclass of `Pauli`): a Pauli operator with general coefficient (outside the Pauli group). 
# * `PauliList` (base class): a list of Pauli operators.
#     * `PauliPolynomial` (subclass of `PauliList`): a linear combination of Pauli operators (stored as Pauli operator list together with combination coefficients.)

# In[67]:


type(paulialg.pauli('X')), type(2*paulialg.pauli('X')), type(paulialg.paulis('X','X')), type(sum(paulialg.paulis('X','X')))


# #### Properties

# As subclasses, `PauliMonomial` and `PauliPolynomial` inherit the related size properties from their parent classes.

# In[69]:


(5*paulialg.pauli('XYZ')).N


# In[75]:


poly = sum(paulialg.paulis('II','XX','YY','ZZ'))
poly, poly.L, poly.N


# `PauliPolynomial` can be selected and sliced as a list.

# In[76]:


poly[1], poly[:2], poly[::2]


# In[77]:


poly[numpy.array([1,1,1,2])]


# In[78]:


poly[numpy.array([True,False,False,True])]


# #### Type Conversion

# `Pauli` can be converted to `PauliMonomial`.

# In[80]:


paulialg.pauli('XX').as_monomial()


# `Pauli`, `PauliList`, `PauliMonomial` can all be converted to `PauliPolynomial`.

# In[81]:


paulialg.pauli('XX').as_polynomial()


# In[82]:


paulialg.paulis('II','XX','YY','ZZ').as_polynomial()


# Automatic type conversion enables the algebra to be carried out among different classes with great flexibiliity.
# * When `Pauli` is multiplied (`*`) by a generic number (beyond powers of the imaginary unit), it is converted to `PauliMonomial`.
# * When `Pauli` or `PauliMonomial` is added (`+`) or subtracted (`-`) with other Pauli objects, they are converted to `PauliPolynomial`.
# * The dot product (`@`) generally returns `PauliPolynomial`, unless the two Pauli objects are both `Pauli`, in which case it returns `Pauli`.

# ---

# ### Clifford Transformation

# `PauliList` provides useful methods to implement Clifford transformations efficiently on all Pauli operators together. The same methods are available to all its subclasses (including `PauliPolynomial`, `CliffordMap`, `StabilizerState`).

# #### Clifford Rotation

# A Clifford rotation is a $\mathbb{Z}_4$ rotation in the Clifford group generated by a single Pauli operator, which takes the form of
# $$U=e^{\frac{i\pi}{4}\sigma}=\frac{1}{\sqrt{2}}(1+i \sigma).$$
# Every Pauli operator is transformed by $\sigma \to U^\dagger \sigma U$. The Clifford rotation can be applied by the method `.rotate_by(gen)` (given the generator `gen`). The operation is in-place (meaning that the operators in the Pauli list will be modified).

# In[25]:


paulialg.paulis('II','XX','YY','ZZ').rotate_by(paulialg.pauli('XI'))


# #### Clifford Map

# A Clifford map is a generic clifford transformation by specifying how each single Pauli operator gets mapped to. It can be listed as a table

# In[87]:


cmap = stabilizer.random_clifford_map(2)
cmap


# It can be applied by the method `.transform_by(cmap)` (given the Clifford map `cmap`). 

# In[88]:


paulialg.paulis('II','XX','YY','ZZ').transform_by(cmap)


# #### Masked Transformation

# Clifford transformation can be applied to a subsystem of qubits specified by a mask.

# In[90]:


mask = numpy.array([True,False,False,True])
paulialg.paulis('IIII','XXXX','YYYY','ZZZZ').rotate_by(paulialg.pauli('XY'), mask)


# In[91]:


mask = numpy.array([True,False,False,True])
paulialg.paulis('IIII','XXXX','YYYY','ZZZZ').transform_by(cmap, mask)


# ---

# ## Algorithm Details

# ### Internal Representation

# #### Binary Representation of Pauli Operators

# Any Pauli operator can be specified by two one-hot (binary) vectors $x$ and $z$ ($x_i,z_i=0,1$ for $i=1,\cdots,N$):
# $$\sigma_{(x,z)}=\mathrm{i}^{x\cdot z}\prod_{i=1}^{N}X_i^{x_i}\prod_{i=1}^{N}Z_i^{z_i}.$$
# * The binary vector $x$ (or $z$) specifies the qubits where the $X$ (or $Z$) operator acts ($Y$ operator acts at where $X$ and $Z$ act simultaneously).
# * **Multiplication** of two Pauli operators
# $$\sigma_{(x,z)}\sigma_{(x',z')}=\mathrm{i}^{p(x,z;x',z')}\sigma_{(x+x',z+z')\%2},$$
# where the power $p$ of $\mathrm{i}$ in the prefactor is given by
# $$p(x,z;x',z')=\sum_{i=1}^{N}\left(z_ix'_i-x_iz'_i + 2(z_i+z'_i)\left\lfloor\frac{x_i+x'_i}{2}\right\rfloor+2(x_i+x'_i)\left\lfloor\frac{z_i+z'_i}{2}\right\rfloor\right)\mod 4.$$
# * **Commutation relation**: two Pauli operator either commute to anticommute.
# $$\sigma_{(x,z)}\sigma_{(x',z')}=(-)^{c(x,z;x',z')}\sigma_{(x',z')}\sigma_{(x,z)},$$
# where the *anticommutation indicator* $c$ has a simpler form
# $$c(x,z;x',z')=\frac{p(x,z;x',z')-p(x',z';x,z)}{2}=\sum_{i=1}^{N}\left(z_ix'_i-x_iz'_i\right)\mod 2.$$
# 
# The binary vectors $x$ and $z$ can be interweaved into a $2N$-component vector $g=(x_0,z_0,x_1,z_1,\cdots)$, which forms the binary representation of a Pauli operator $\sigma_g$.

# #### `Pauli` Class

# `Pauli(g,p)` represents a Pauli operator.
# 
# **Parameters:**
# * `g` binary representation of Pauli string.
# * `p` phase indicator ($p=0,1,2,3$ stands for $i^p$ phase factor).

# In[4]:


paulialg.pauli('iX').__dict__


# #### `PauliList` Class

# `PauliList(gs,ps)` represents a list of Pauli operators.
# 
# **Parameters:**
# * `gs` array of binary representations of Pauli strings.
# * `ps` array of phase indicators ($p=0,1,2,3$ stands for $i^p$ phase factor).

# In[5]:


paulialg.paulis('XX','YY','ZZ').__dict__


# #### `PauliMonomial` Class

# `PauliMonomial(g,p)` represents a Pauli operator with coefficient.
# 
# **Parameters:**
# * `g` binary representation of Pauli string.
# * `p` phase indicator ($p=0,1,2,3$ stands for $i^p$ phase factor).
# * `c` coefficient (complex).

# In[6]:


paulialg.pauli('iX').as_monomial().__dict__


# The property `c` can be set by the method `.set_c(c)`

# In[8]:


paulialg.pauli('X').as_monomial().set_c(2.+0.j).__dict__


# #### `PauliPolynomial` Class

# `PauliPolynomial(gs,ps)` represents a polynomial (linear combination) of Pauli operators.
# 
# **Parameters:**
# * `gs` array of binary representations of Pauli strings.
# * `ps` array of phase indicators ($p=0,1,2,3$ stands for $i^p$ phase factor).
# * `cs` array of coefficients (complex).

# In[9]:


(paulialg.pauli('XX') - 2*paulialg.pauli('YY')).__dict__


# The property `cs` can be set by the method `.set_cs(cs)`

# In[2]:


(paulialg.pauli('XX') - 2*paulialg.pauli('YY')).set_cs(np.array([3.4,2.4])).__dict__


# ## Link with QuTip Library

# Pauli operators can be easily converted to the `Qobj` in qutip library
# - `Pauli.to_qupit()`
# - `PauliList.to_qutip()`
# - `PauliMonomial.to_qutip()`
# - `PauliPolynomial.to_qutip()`

# In[2]:


paulialg.pauli('XY').to_qutip()


# In[3]:


paulialg.paulis('XY','ZZ').to_qutip()


# In[3]:


((2+3j)*paulialg.pauli('XY')).to_qutip()


# In[5]:


((2+3j)*paulialg.pauli('XY')+(1.5)*paulialg.pauli('ZZ')).to_qutip()


# In[ ]:





# In[17]:


a = np.array([1,2])


# In[18]:


b=np.array(a)


# In[19]:


b[0]=4


# In[20]:


b


# In[21]:


a


# In[ ]:




