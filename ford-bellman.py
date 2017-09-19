
# coding: utf-8

# ## Ford-Bellman algorithm
# ---
# Represents a way to find the minimum path in weighted graph using Ford-Bellman[-Moore] algorithm with predefined weight matrix for the graph.

# In[1]:

# Define shorthands
import numpy as np
inf = np.inf
s = 1 # start vertex
e = 4 # end vertex
n = 7 # matrix dimensions

# Graph weight matrix
graph = np.array([
    (inf, 5.0, 4.0, inf, 3.0, inf, inf),
    (inf, inf, inf, inf, inf, -1., inf),
    (inf, inf, inf, inf, inf, inf, 3.0),
    (4.5, inf, inf, inf, inf, inf, inf),
    (inf, inf, 7.0, 5.0, inf, 6.0, inf),
    (inf, inf, inf, inf, inf, inf, inf),
    (inf, inf, inf, inf, inf, inf, inf)], dtype=float)

# Append lambda-0 column to the matrix
graph = np.append(graph, np.ones((7, 1), dtype=float) * inf, axis = 1)

# Set lambda-0 start element as zero (reachable for itself)
graph[(s - 1), -1:] = 0

# Stage 1: Build lambda-matrix
while True:
    # Add lambda-n column to the matrix (copy of lambda-m, m = n - 1)
    graph = np.append(graph, graph[:, -1:], axis = 1)
    # Cycle through images (relaxation)
    for vertex in range(0, graph.shape[0]):
        # Cycle through preimages for the image (the same dimension)
        for preimage in range(0, graph.shape[0]):
            # If preimage's weight is finite, then compare with prev relax of preimage + preimage's weight
            if graph[preimage, vertex] != inf:
                graph[vertex, -1:] = min(graph[vertex, -1:], graph[preimage, -2:-1] + graph[preimage, vertex])
    # Finish the cycle if the relaxation gave no more options (or maximum size is reached)
    if (graph[:, -2:-1] == graph[:, -1:]).all() or graph.shape[1] >= n * 2:
    #if graph.shape[1] >= n * 2:
        break

# Display output
print (graph)
#print ("Final relaxations match:", (graph[:,-2:-1] == graph[:,-1:]).all()) # DEBUG
#print (graph.shape[1]) # DEBUG
#print ("Matrix width:", len(graph[0,:])) # DEBUG

# Stage 2: Build path
length = 0
#print (graph.shape[1] - n)
for i in range(n + 1, graph.shape[1]):
    if graph[e - 1, i] < graph[e - 1, i - 1]:
        length = i - n
print ("Graph minimal path length =", length)
# Prepare minimal path vector
path = np.zeros([length + 1], dtype=int)
# Set the last path vertex
path[length] = e
# Add vertices to the path in reverse order
for node in range(length, 0, -1):
    #print ("Processing node:", node) # DEBUG
    # Check each preimage (each row in the node's column)
    for vertex in range(0, n):
        # Process only finite weights
        if graph[vertex, path[node] - 1] != inf:
            #print ("Processing preimage:", vertex) # DEBUG
            # If condition "lambda-m (preimage) = lambda-n (image) + weight" match
            if graph[vertex, n + length] == graph[path[node] - 1, n + length + 1] - graph[vertex, path[node] - 1]:
                # Then this is the correct preimage - add it to the path
                path[node - 1] = vertex + 1
print ("Graph minimal path (by vertices):", path)
# TODO: Add path weight

