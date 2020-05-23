#! /usr/bin/python

import random
from math import sqrt
from math import floor
from math import ceil
from math import log

SHOW_CUTS = False

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
    new_history = history

    # replace the vertices contracted by the new one
    for i in range(3):

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

# This is not a magic number
current_min = 40000000

## each cell will contain [cut_size, [[hash0, [set0]], [hash1, set1], ...]]
## ordered by hash value for later comparison
## A min_cut is represented only once
global_history = []

def new_min(x):
    global current_min
    current_min = min(x, current_min)

def insert_cut(cut_size, history):
    global global_history

    if cut_size > current_min:
        return

    new_min(cut_size)

    ## Prepare candidate
    ## Sort the sets inside
    prep0 = [sorted(cut_set) for cut_set in history if len(cut_set) > 0]

    if SHOW_CUTS:
        ## Compute hash for each set
        prep1 = [[hash(tuple(cut_set)), cut_set] for cut_set in prep0]

        ## Sort sets according to hash value
        prep2 = sorted(prep1, key=lambda k: k[0])

        ## Extract list of hash list of current cuts
        current_hash_list = [[e[0] for e in cut[1]] for cut in global_history]

        ## Extract hash list for comparison
        candidate_hash_list = [h[0] for h in prep2]

        if candidate_hash_list not in current_hash_list:
            global_history.append([cut_size, prep2])

    else:
        ## Compute hash for each set
        prep1 = [hash(tuple(cut_set)) for cut_set in prep0]

        ## Sort sets according to hash value
        prep2 = sorted(prep1)

        ## Extract list of hash list of current cuts
        current_hash_list = [x[1] for x in global_history]

        if prep2 not in current_hash_list:
            global_history.append([cut_size, prep2])
    

    return

## Karger-Stein
def min_cut(n, graph, history):

    if n <= 3:

        cut_size = 0
        
        if n == 2:
            cut_size = len(graph)
            insert_cut(cut_size, history)
            return
        
        # try one last contraction
        to_contract = graph[random.randint(0, len(graph)-1)]
        new_n, last_try, new_history = contract_hyperedge(to_contract, graph, n, history)

        if new_n == 1: #should not have contracted
            cut_size = len(graph)
            insert_cut(cut_size, history)
        else:
            cut_size = len(last_try)
            insert_cut(cut_size, new_history)

        return

    precontracted = graph
    new_n = n
    new_history = [[i for i in group] for group in history]

    for _ in range(n - ceil(n/sqrt(2))):
        to_contract = precontracted[random.randint(0, len(precontracted)-1)]
        new_n, precontracted, new_history = contract_hyperedge(to_contract, precontracted, new_n, new_history)

    for _ in range(2):
        min_cut(new_n, precontracted, new_history)

    return


def yeet():
    n, graph = get_input()

    # at first, each element represents itself
    history = [[x] for x in range(1, n+1)]

    for _ in range(4*ceil((log(n, 2)**2))):
        min_cut(n, graph, history)

    global global_history
    global_history = [x[1] for x in global_history if x[0] == current_min]

    print(current_min, len(global_history))

    if SHOW_CUTS:
        cuts = [[hashed_tuple[1] for hashed_tuple in complete] for complete in global_history]
        for _, e in enumerate(cuts):
            print()
            print(e)

yeet()
# It was a magic number