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

def replace_endpoints(hyperedge, e):
    new_vertice = hyperedge[0]
    new_edge = []

    # replace the vertices contracted by the new one
    for i in range(len(e)):
        if e[i] in hyperedge:
            new_edge.append(new_vertice)
        else:
            new_edge.append(e[i])


    return new_edge

def contract_hyperedge(hyperedge, graph, n):
    contracted_graph = []

    ## If all the endpoints of the edge to are different, 2 will disappear into the one remaining
    ## If only 2 different endpoints, 1 will disappear

    new_n = n

    if (hyperedge[0] != hyperedge[1]) and (hyperedge[1] != hyperedge[2]) and (hyperedge[0] != hyperedge[2]):
        new_n -= 2
    else:
        new_n -= 1


    for _, e in enumerate(graph):
        contracted_edge = replace_endpoints(hyperedge, e)

        if not (contracted_edge[0] == contracted_edge[1] == contracted_edge[2]): # ignore if it's a point
            contracted_graph.append(contracted_edge)

    return new_n, contracted_graph


## Karger-Stein
def min_cut(n, graph):

    precontracted = graph
    new_n = n
    #print("graph")
    #print(n)
    #print(graph)
    #print()
    #print(n - ceil(n/sqrt(2)))

    if n <= 3:
        
        if n == 2:
            return len(graph)
        
        # try one last contraction
        to_contract = precontracted[random.randint(0, len(precontracted)-1)]
        new_n, last_try = contract_hyperedge(to_contract, precontracted, new_n)

        if new_n == 1: #should not have contracted
            return len(graph)
        else:
            return len(last_try)
        

    for _ in range(n - ceil(n/sqrt(2))):
        to_contract = precontracted[random.randint(0, len(precontracted)-1)]
        new_n, temp = contract_hyperedge(to_contract, precontracted, new_n)

        precontracted = temp
        #print("deleted")
        #print(to_contract)
        #print("temp")
        #print(new_n)
        #print(temp)
        #print()


    res = []
    for _ in range(3):
        sub_min = min_cut(new_n, precontracted)
        #print(str(i) + ": " + str(sub_min))
        res.append(sub_min)

    print(res)

    return min(res)

n, graph = get_input()

res = []

for _ in range(ceil((log(n, 2)**2))):
    temp = min_cut(n, graph)
    if temp != 0:
        res.append(temp)

print(min(res))

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