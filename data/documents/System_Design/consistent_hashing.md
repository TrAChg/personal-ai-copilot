# Consistent Hashing with Virtual Nodes in Distributed Systems

## 1. Problem Formulation
In a distributed caching or database system (e.g. Cassandra, DynamoDB, Memcached), traditional modulo hashing $H(key) \pmod N$ causes massive rehashing ($O(K)$ keys moved) when a node is added or removed, inducing severe cache stampedes.

## 2. Mathematical Definition
Consistent hashing maps both servers and keys onto a circular hash ring $[0, 2^{32} - 1]$ using a uniform hash function (e.g., MurmurHash3 or SHA-256):
$$\text{RingPosition} = H(x) \pmod{2^{32}}$$

When a key $k$ is queried, it moves clockwise until it finds the first node whose position is greater than or equal to $H(k)$:
$$\text{AssignedNode}(k) = \min \{ n \in \text{Nodes} \mid H(n) \ge H(k) \} \cup \{\min(\text{Nodes})\}$$

## 3. Virtual Nodes (V-Nodes) for Load Balance
To avoid hot spots and non-uniform clustering on the ring, each physical node is replicated as $V$ virtual nodes:
- Physical server $S_i$ is mapped to $\{H(S_i \# 1), H(S_i \# 2), \dots, H(S_i \# V)\}$.
- Standard recommendation: $V \approx 100\text{--}256$ virtual nodes per physical host.
- When server $S_i$ crashes, its keys are evenly distributed across all remaining servers rather than overloading a single neighbor.

