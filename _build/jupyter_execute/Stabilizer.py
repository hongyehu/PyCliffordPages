#!/usr/bin/env python
# coding: utf-8

# In[1]:


# will autoupdate any of the packages imported:
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[2]:


from context import *


# # Stablizer Formalism (`stabilizer`)

# ## General Idea: State-Map Duality

# Every stabilizer state $\rho$ is dual to a Clifford unitary $U$, such that the state can be generated from the zero state $|00\cdots0\rangle$ as
# $$\rho = U|00\cdots0\rangle\langle 00\cdots0|U^\dagger$$.
# Both $\rho$ and $U$ describes a stabilizer code:
# * $\rho$ is a projection operator that specifies the code subspace of the stabilizer code.
# * $U$ is the encoding Clifford unitary that encodes the logical + syndrome qubits to the physical qubits in the stabilizer code.
# 
# The package `stabilizer` (based on `paulialg`) provides related functions to represent stabilizer states and Clifford maps. There are two classes defined in this package.
# 
# * `stabilizer.CliffordMap`. Since the Clifford unitary $U$ maps Pauli operators to Pauli operators, it is sufficient to specify a Clifford unitary by how each single-qubit Pauli operator transforms under the unitary. Such transformation rules are stored in a table called the Clifford map.
# 
# * `stabilizer.StabilizerState`. The stabilizer state is specified by a set of stabilizers and the corresponding destabilizers. Using the binary representation of Pauli operators, they can be stored in a table, called the stabilizer tableau. 
# 
# Since both classes need to store a table of Pauli operators, they are both realized as subclasses of `paulialg.PauliList`.

# ## Basic Usage

# ---

# ### Constructors

# #### Construct Clifford Maps

# `identity_map(N)` constructs an identity Clifford map on $N$ qubits.

# In[3]:


stabilizer.identity_map(4)


# In[4]:


stabilizer.identity_map(4).ps


# `random_pauli_map(N)` samples a random Clifford map made of random single-qubit Clifford gates on $N$ qubits, i.e. $U=\prod_i U_i\in\mathrm{Cl}(2)^N$. Each realization specifies a random local Pauli basis.

# In[5]:


stabilizer.random_pauli_map(4)


# `random_clifford_map(N)` samples a globally random Clifford map on $N$ qubits, i.e. $U\in\mathrm{Cl}(2^N)$. Each realization specifies a random global stabilizer basis.

# In[6]:


stabilizer.random_clifford_map(4)


# `clifford_rotation_map(N)` constructs a Clifford map based for a Clifford rotation given its generator.

# In[7]:


stabilizer.clifford_rotation_map('-XXYZ')


# #### Construct Stabilizer States

# `maximally_mixed_state(N)` constructs a $N$-qubit maximally mixed state (by setting the density matrix to full rank).
# $$\rho=2^{-N}\mathbb{1}.$$

# In[8]:


stabilizer.maximally_mixed_state(4)


# `zero_state(N)` constructs a $N$-qubit all-zero state 
# $$\rho=|0\cdots0\rangle\langle 0\cdots0|=\prod_{i}\frac{1+Z_i}{2}.$$

# In[9]:


stabilizer.zero_state(4)


# `one_state(N)` constructs a $N$-qubit all-one state 
# $$\rho=|1\cdots1\rangle\langle 1\cdots1|=\prod_{i}\frac{1-Z_i}{2}.$$

# In[10]:


stabilizer.one_state(4)


# `ghz_state(N)` constructs a $N$-qubit GHZ state
# $$\rho = |\Psi\rangle\langle\Psi|, \qquad \text{with }|\Psi\rangle=\frac{1}{\sqrt{2}}(|0\cdots0\rangle+|1\cdots1\rangle).$$

# In[11]:


stabilizer.ghz_state(4)


# `random_pauli_map(N)` samples a $N$ qubit random Pauli state.
# $$\rho=U|0\cdots0\rangle\langle 0\cdots0|U^\dagger,\qquad\text{with }U\in \mathrm{Cl}(2)^N.$$

# In[12]:


stabilizer.random_pauli_map(4)


# `random_clifford_map(N)` samples a $N$ qubit random Clifford (random stabilizer) state.
# $$\rho=U|0\cdots0\rangle\langle 0\cdots0|U^\dagger,\qquad\text{with }U\in \mathrm{Cl}(2^N).$$

# In[13]:


stabilizer.random_clifford_state(4)


# `stabilizer_state(...)` is a universal constructor of stabilizer state by specifying all stabilizers.

# In[14]:


stabilizer.stabilizer_state('XXY','ZZI','IZZ')


# #### Low level constructor

# The user can also construct stabilizer state by low-level constructor `StabilizerState(gs, ps, r=0)`:
# 
# **Parameters**
# - `gs: int (2*N, 2*N)`: strings of Pauli operators in the stabilizer tableau.
# - `ps: int (2*N)`: phase indicators (should only be 0 or 2).
# - `r:  int`: number of logical qubits (log2 rank of density matrix)'''
# 
# **Returns**
# - Object of `StabilizerState`

# In[15]:


tmp_state = stabilizer.random_clifford_state(3)
print(tmp_state)


# In[16]:


gs = tmp_state.gs
gs


# In[17]:


ps = tmp_state.ps
ps


# In[18]:


stabilizer.StabilizerState(gs=gs, ps = ps)


# In[19]:


stabilizer.StabilizerState(gs=gs, ps = ps,r=1)


# A hack to inspect the full stabilizer tableau is by converting `StabilizerState` to `PauliList` by

# In[20]:


stabilizer.stabilizer_state('XXY','ZZI','IZZ')[:]


# <div class="alert alert-block alert-danger">
# User need to <b>ensure</b> that stabilizers commute with each other, otherwise an error will be raised.
# </div>

# In[21]:


stabilizer.stabilizer_state('XXY','-YYI','IZZ')


# #### State-Map Conversion

# Stabilizer states and Clifford maps can be mapped to each other.

# In[26]:


rho = stabilizer.stabilizer_state('XXX','ZZI','IZZ')
print("quantum state: \n", rho)


# In[27]:


rho.to_map()


# And Clifford map can be converted back to the stabilizer state.

# In[28]:


rho.to_map().to_state()


# * `.to_map()` and `.to_state()` will make **new copies** of Pauli string data in the memory.

# <div class="alert alert-block alert-danger">
# The information about the rank of the density matrix is lost in the Clifford map, so the back conversion will result in a zero rank stabilizer state.
# </div>

# ---

# ### Clifford Map Methods

# #### - Map Embedding

# `.embed(small_map, mask)` provides the method to embed a smaller Clifford map on a subset of qubits to the current Clifford map. This is a **in-place** operation. The Clifford map object that provide this method will get modified under the embedding.
# 
# **Parameters:**
# * `small_map` is a `CliffordMap` object supported on a subset of qubits.
# * `mask` is a boolean array specifying the subset of qubits.

# In[29]:


cmap = stabilizer.identity_map(6)
cmap


# In[30]:


cmap.embed(stabilizer.random_clifford_map(3), numpy.array([True,False,False,True,True,False]))


# #### - Map Composition

# `.compose(other)` returns the composition of the current Clifford map with another Clifford map. This will return a new Clifford map without modifying either of the input maps. The Clifford map object which initiates this method will be the preceeding map in the composition. 
# 
# **Parameters:**
# * `other` - another `CliffordMap`.

# In[34]:


cmap.compose(stabilizer.random_clifford_map(6))


# #### - Map Inversion

# `.inverse()` returns the inverse of the current Clifford map. This will return a new Clifford map withoutt modifying the original map. The inverse map is such that its composition with the original map must be identity

# In[37]:


cmap = stabilizer.clifford_rotation_map('Y')
cmap


# In[38]:


cmap.inverse()


# Test on random maps.

# In[44]:


cmap = stabilizer.random_clifford_map(20)
cmap.inverse().compose(cmap)


# In[45]:


cmap.compose(cmap.inverse()) 


# ---

# ### Stabilizer State Methods

# - ####  **Active stabilizers**

# @property `StabilizerState.stabilizers` will return the active stabilizers, as PauliList, of the current state

# In[88]:


stabilizer.ghz_state(3).stabilizers


# - ####  **Measurement**

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

# In[49]:


state = stabilizer.ghz_state(3)
state


# In[50]:


state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# In the above example, I created a GHZ state, and did single qubit Z-basis measurements on each of the qubit. We get -1 for all qubits with probility $2^{-1}=0.5$

# <div class="alert alert-block alert-danger">
# Measurement will <b>in place </b> change the state, as measurement will collapse the quantum state.
# </div>

# In[51]:


state = stabilizer.ghz_state(3)
state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# In[52]:


state.measure(paulialg.paulis('ZII','IZI','IIZ'))


# We see the second measurement will return the same measurement result with 100% probability

# - ####  **Expectation**

# `StabilizerState.expect()` provide fast algorithm to evaluate expectation value of:
# - Pauli operator
# - Pauli Monomial/Polynomial
# - Overlap between stabilizer states <font color='red'>Warning: currently it only supports pure state overlap with general stabilizer states.</font>

# In[55]:


state = stabilizer.ghz_state(3)


# In[68]:


state.expect(paulialg.paulis('XXXXX','IZIII','-ZZIII'))


# In[72]:


pauli_poly = 0.5*paulialg.pauli('XXXXX')+0.2j*paulialg.pauli('-ZZIII')


# In[73]:


state.expect(pauli_poly)


#  - #### **Stabilizer state overlap**

# In[20]:


state = stabilizer.ghz_state(3)
state2 = stabilizer.random_clifford_state(3)
print("State overlap is:", state.expect(state2))


# In[22]:


tate = stabilizer.ghz_state(3)
state2 = stabilizer.random_clifford_state(3)
state2.set_r(1)
print("State overlap is:", state.expect(state2))


# - #### **Bit-string probability**

# `StabilizerState.get_prob(bitstring)` will return the probability of measuring given bitstring at current stabilizer state.
# **Input**
# - bitstring: Integer type 1D array
# **Output**
# - probability

# In[19]:


state = stabilizer.ghz_state(625)


# In[20]:


state.get_prob(np.ones(625))


# In[19]:


state = stabilizer.stabilizer_state("ZZ","XX")


# In[20]:


state.get_prob(np.array([0,0]))


# - #### **Transform stabilzier state by rotation/Clifford transformation**

# As a derived class of `PauliList`, `StabilizerState` also support `StabilizerState.rotate_by(pauli)` and `StabilizerState.transform_by(clifford_map)`

# In[21]:


rho = stabilizer.ghz_state(4)


# In[22]:


rho.rotate_by(paulialg.pauli([1,3,1,0]))


# In[25]:


rho = stabilizer.ghz_state(4)


# In[26]:


rho.transform_by(stabilizer.random_clifford_map(4))


# - #### **Sample stabilizers in the group**

# `Stabilizer.sample(L)` will sample $L$ stabilizers in the stabilizer group

# In[97]:


np.random.randint(2, size=(10,5-0))


# - #### **Entropy**

# `StabilizerState.entropy(subsys)` will calculate the second Renyi entropy of the stabilizer state on subregion.
# **Parameter**
# - `subsys`: List containing the location of region

# In[58]:


state = stabilizer.random_clifford_state(20)


# In[59]:


state.entropy([1,2])


# In[60]:


state.entropy([1,5,10])


# It also support entanglement entropy for mixed state

# In[25]:


state = stabilizer.random_clifford_state(4)
state.set_r(4)
state.entropy([1,2])


# - #### **Copy**

# `Stabilizer.copy()` will return a copy of stabilizer state

# In[26]:


state = stabilizer.random_clifford_state(4).copy()


# `StabilizerState.copy()` returns a copy of the state, such that the original state will not be touch by modification on the copy state. It is useful to copy the state for measurement (as measurement changes the state).
# 
# Example:

# In[19]:


state = stabilizer.random_clifford_map(4).to_state()
new_state = state.copy()


# - #### **Set Rank**

# `Stabilizer.set_r(r)` will set the $\log_2$ rank of stabilizer state. For $r>0$, the state is mixed.

# In[27]:


stabilizer.random_clifford_state(4).set_r(1)


# - #### **Sample**

# `StabilizerState.sample(L)` will sample $L$ pauli strings in the stabilizer group

# In[29]:


stabilizer.ghz_state(10).sample(3)


# - #### **Density matrix**

# @property `StabilizerState.density_matrix` will return density matrix of stabilizer state as `PauliPolynomial`

# In[30]:


stabilizer.ghz_state(3).density_matrix


# `StabilizerState.set_r(r)` will set the $log_2$ rank of stabilizer state. Default value is zero (pure state)

# In[22]:


state = stabilizer.random_clifford_map(4).to_state()
state


# In[24]:


state.set_r(2)


# ## A little hack into the design

# ---

# ### StabilizerState

# The basic classes in stabilizer are: 1. StabilizerState and 2. CliffordMap, which are linked through state-map duality

# #### The Representation of Density Matrix

# A $[N,r]$ stabilizer state is describe by the **density matrix** of the following form:
# $$\rho = \frac{1}{2^r}\prod_{k=1}^{N-r}\frac{1+(-)^{b_k}S_k}{2}.$$
# * Each stabilizer $S_k$ is a (non-trivial) Pauli operator defined on totally $N$ qubits. The stabilizers commute with each other $[S_k,S_{k'}]=0$. They generate an Abelian subgroup $\mathcal{S}=\{\prod_{k=1}^{N-r} S_k^{a_k}|a_k=0,1\}$ of the $N$-qubit Pauli group, called the *stabilizer group*.
# * Each sign indicator $b_k=0,1$ is a binary variable specifying the eigen space of the stabilizer.
# * There are totally $N-r$ stabilizers for a $[N,r]$ stablizer code (of code rate: $r/N$). The simultaneous eigenspace of all stabilizers constitutes the *code subspace*. 
# * The code subspace is $2^r$ dimensional (which is also the rank of the density matrix $\rho$). The stabilizer state $\rho$ is always defined to be the maximally mixed state in the code subspace, such that $\rho$ is also the **projection operator** that projects any state into the code subspace.

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

# #### Stabilizer Tableau

# Each stabilizer state is internally stored in the form of a **stabilizer tableau** $S$, together with the **sign indicator** $b$. For a $[N,r]$ stabilizer state, its stabilizer tableau is a $2N\times 2N$ matrix of the following structure

# <img src="fig_tableau.png" alt="stabilizer tableau." style="width: 320px;"/>

# * Each row is a binary representation $(x,z)$ of a Pauli oparator $\sigma_{(x,z)}$.
# * Totally $2N$ Pauli operators grouped into $N$ stabilizers and $N$ destabilizers, such that for $i,j=0,\cdots,2N-1$:
# $$\sigma_{g_{i}}\sigma_{g_{j}}=(-)^{\delta_{i+N,j}-\delta_{j+N,i}}\sigma_{g_{j}}\sigma_{g_{i}},$$
# i.e. the $i$th stabilizer only anticommute with the $i$th destabilizer and they commute with all the other operators in the tableau.
# * The rows $r:N$ correspond to the $N-r$ active stabilizers $S_k$, which stabilize the code subspace (impleted as projection operators). The rows $0:r$ corresponds to the $r$ standby (inactive) stabilizers that does not realy stabilizer the code subspace (but they will act as logical operators in the code subspace).
# * The rows $N+r:2N$ correspond to the $N-r$ active destabilizers that anticommute with the active stabilizers. The rows $N:N+r$ correspond to the $r$ standby destabilizers taht anticommute with the standby stabilizers.
# 
# Although the stabilizer state is only specified by the active stabilizers, the other operators in the stabilizer tableau are still important in order to complete the operator basis. Such that the tableau can specify an unitary operator in the Clifford group that generate the state. The algorithm must mantain the algebraic structure betwen all stabilizers and destabilizers while updating the tableau.

# Example: stabilizer tableau is given by `StabilizerState.gs`

# In[50]:


rho = stabilizer.random_clifford_state(4)
print('state is: \n',rho)


# In[51]:


rho.gs


# The sign of (de)stabilziers can be read through `StabilizerState.ps`, which returns the power of $i$

# In[55]:


rho.ps


# ## Link with QuTip Library

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[59]:


stabilizer.identity_map(3).to_state().gs


# In[43]:


stabilizer.maximally_mixed_state(3).r


# In[39]:


paulialg.paulis(paulialg.pauli([3,0,0]),-1*paulialg.pauli([0,3,0])).gs


# In[37]:


paulialg.paulis(paulialg.pauli({i:'Z'}, 4) for i in range(4))


# ## Development

# In[1]:


from context import *


# #### Test Unit: two pure state overlap

# In[2]:


test_res = []
N = 6
test_num = 100
for i in range(test_num):
    state = stabilizer.random_clifford_state(N)
    state2 = stabilizer.random_clifford_state(N)
    trace = np.real(np.trace((state.to_qutip())*(state2.to_qutip())))
    # _, _, _, trace_test = utils.stabilizer_projection_trace(np.array(state.gs), np.array(state.ps), \
    #                               np.array(state2.gs[:N,:]), np.array(state2.ps[:N]), state2.r)
    trace_test = state.expect(state2)
    test_res.append(trace==trace_test)


# In[3]:


if not(len(test_res)-np.sum(test_res)):
    print('Stochastic test passed!')


# #### Test Unit: pure state A overlap with mixed state B

# In[4]:


test_res = []
N = 6
test_num = 100
rank = 2
for i in range(test_num):
    state = stabilizer.random_clifford_state(N)
    state2 = stabilizer.random_clifford_state(N)
    state2.set_r(rank)
    trace = np.real(np.trace((state.to_qutip())*(state2.to_qutip())))
    # _, _, _, trace_test = utils.stabilizer_projection_trace(np.array(state.gs), np.array(state.ps), \
    #                               np.array(state2.gs[rank:N,:]), np.array(state2.ps[rank:N]), state.r)
    # trace_test = trace_test/2**rank
    trace_test = state.expect(state2)
    test_res.append(trace_test==trace)


# In[5]:


if not(len(test_res)-np.sum(test_res)):
    print('Stochastic test passed!')


# In[6]:


state = stabilizer.random_clifford_state(N)
state.set_r(2)
state2 = stabilizer.random_clifford_state(N)
state.expect(state2)


# In[ ]:





# In[ ]:





# In[ ]:





# In[32]:


type(stabilizer.ghz_state(3).to_map())


# In[59]:





# In[14]:


state = stabilizer.random_clifford_state(2)


# In[15]:


state


# In[16]:


state.density_matrix


# In[34]:


state2=state.copy()


# In[35]:


state2.measure(paulialg.paulis('ZI','IZ'))


# In[ ]:





# In[ ]:





# In[17]:


state.to_qutip()


# In[19]:


qt.hadamard_transform(1)


# In[20]:


qt.hadamard_transform(1)*qt.sigmay()


# In[21]:


qt.sigmaz()*qt.hadamard_transform(1)


# In[22]:


qt.hadamard_transform(1)*qt.sigmax()


# In[23]:


qt.tensor([qt.sigmaz(),qt.sigmaz()])


# In[ ]:




