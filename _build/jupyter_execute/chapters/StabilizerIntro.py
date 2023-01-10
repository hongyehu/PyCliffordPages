#!/usr/bin/env python
# coding: utf-8

# In this chapter, you will learn the basic of stabilizer states, and Clifford Maps

# # State-Map Duality

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

# In[ ]:




