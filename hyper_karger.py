#! /usr/bin/python

import random
from math import sqrt
from math import floor
from math import ceil
from math import log

def get_input():
    raw_nm = input()

    n, m = raw_nm.split(' ')

    m = int(m)
    n = int(n)

    hyperedges = []

    for _ in range(m):

        raw_elements = input()
        endpoints = raw_elements.split(' ')
        endpoints = [int(x) for x in endpoints]

        hyperedges.append(endpoints)
    
    return n, hyperedges

def replace_endpoints(hyperedge, e, history):
    new_vertice = hyperedge[0]
    new_edge = []
    new_history = [[i for i in group] for group in history]

    #print("***** BEGIN *****")

    #print(hyperedge)
    #print(e)

    # replace the vertices contracted by the new one
    for i in range(len(e)):

        elt = e[i]

        if elt in hyperedge:
            new_edge.append(new_vertice)

            # transfer history to new node
            if elt != new_vertice:
                for _, h in enumerate(new_history[elt-1]):
                    new_history[new_vertice-1].append(h)

                new_history[elt-1] = []

        else:
            new_edge.append(elt)

        #print(i, elt)
        #print(new_history)

    #print("***** END *****")


    return new_edge, new_history

def contract_hyperedge(hyperedge, graph, n, history):
    contracted_graph = []

    ## If all the endpoints of the edge to are different, 2 will disappear into the one remaining
    ## If only 2 different endpoints, 1 will disappear

    new_n = n
    new_history = [[i for i in group] for group in history]

    if (hyperedge[0] != hyperedge[1]) and (hyperedge[1] != hyperedge[2]) and (hyperedge[0] != hyperedge[2]):
        new_n -= 2
    else:
        new_n -= 1


    for _, e in enumerate(graph):
        contracted_edge, new_history = replace_endpoints(hyperedge, e, new_history)

        if not (contracted_edge[0] == contracted_edge[1] == contracted_edge[2]): # ignore if it's a point (lööp)
            contracted_graph.append(contracted_edge)

    return new_n, contracted_graph, new_history


## Karger-Stein
def min_cut(n, graph, res_count, history):

    #print("graph")
    #print(n)
    #print(graph)
    #print()
    #print(n - ceil(n/sqrt(2)))

    if n <= 3:

        cut_size = 0
        
        if n == 2:
            cut_size = len(graph)
            res_count.append((cut_size, history))
            return cut_size
        
        # try one last contraction
        to_contract = graph[random.randint(0, len(graph)-1)]
        new_n, last_try, new_history = contract_hyperedge(to_contract, graph, n, history)

        if new_n == 1: #should not have contracted
            cut_size = len(graph)
            res_count.append((cut_size, history))
        else:
            cut_size = len(last_try)
            res_count.append((cut_size, new_history))

        return cut_size

    precontracted = graph
    new_n = n
    new_history = [[i for i in group] for group in history]

    for _ in range(n - ceil(n/sqrt(2))):
        to_contract = precontracted[random.randint(0, len(precontracted)-1)]
        new_n, precontracted, new_history = contract_hyperedge(to_contract, precontracted, new_n, new_history)

        #print("deleted")
        #print(to_contract)
        #print("temp")
        #print(new_n)
        #print(temp)
        #print()


    res = []

    for _ in range(2):
        sub_min = min_cut(new_n, [[endpoint for endpoint in edge] for edge in precontracted], res_count, new_history)
        res.append(sub_min)

    #print(res)

    return min(res)

n, graph = get_input()

res = []

res_count = []
# used to count how many min cuts we encountered
# will contain the history of the contractions at the end of each recursion
# first indice of each sub array is the min cut value found

# at first, each element represents itself
history = [[x] for x in range(1, n+1)]

for _ in range(ceil((log(n, 2)**2))):
    temp = min_cut(n, graph, res_count, history)
    res.append(temp)

min_cut = min(res)

# keep only best and remove empty buckets
best = [[group for group in x[1] if len(group) > 0] for x in res_count if x[0] == min_cut]

print(min_cut, best)

## LONG
'''def min_cut(graph):
    contracted_new = graph
    contracted_old = contracted_new

    while len(contracted_new) > 0:
        contracted_old = contracted_new
        to_contract = contracted_old[random.randint(0, len(contracted_old)-1)]
        contracted_new = contract_hyperedge(to_contract, contracted_old)

    return len(contracted_old)

n, graph = get_input()

res = []

for _ in range(floor(n*n*log(n,2))):
    res.append(min_cut(graph))

print(min(res))'''