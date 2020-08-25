from collections import deque
from compare_objects import ListManager
from math import pow

def sort_objects(comps):
    '''
    Returns a sorting of objects from best to worst.
    >>> comps = [('A', 'B'), ('B', 'A'), ('C', 'A'), ('C', 'D'), ('D', 'C'), ('E', 'B')]
    >>> sort_objects(comps)
    ['E', 'D', 'C', 'B', 'A']
    >>> comps = [('bread', 'wheat'), ('butter', 'guns'), ('guns', 'bread')]
    >>> sort_objects(comps)
    ['butter', 'guns', 'bread', 'wheat']
    '''
    # Create adjacency lists for forward and reverse graphs
    fwd_graph, rev_graph = {}, {}
    for comp in comps:
        better, worse = comp[0], comp[1]
        if better not in fwd_graph:
            fwd_graph[better] = []
        if worse not in fwd_graph:
            fwd_graph[worse] = []
        if better not in rev_graph:
            rev_graph[better] = []
        if worse not in rev_graph:
            rev_graph[worse] = []
        fwd_graph[worse].append(better)
        rev_graph[better].append(worse)
    # Create stack to hold reverse postorder
    rev_postorder = deque()
    visited = set()
    # Run visit subroutine on each vertex
    for v in fwd_graph.keys():
        visit(fwd_graph, v, rev_postorder, visited)
    # Create sorted list by adding SCCs in reverse postorder
    sorted_objects = []
    visited = set()
    while rev_postorder:
        # Run BFS to add all vertices in the same SCC
        q = deque()
        q.append(rev_postorder.pop())
        while q:
            cur_v = q.pop()
            if cur_v not in visited:
                sorted_objects.insert(0, cur_v)
                visited.add(cur_v)
                q.extendleft(rev_graph[cur_v])
    return sorted_objects

def visit(fwd_graph, v, rev_postorder, visited):
    '''
    Visit subroutine for creating reverse postorder stack
    '''
    if v in visited:
        return
    visited.add(v)
    # Push all vertices reachable from current vertex first
    for v2 in fwd_graph[v]:
        visit(fwd_graph, v2, rev_postorder, visited)
    rev_postorder.append(v)

'''a = ListManager()
comparisons = [(x.better, x.worse) for x in a.comp_list]
ranked = sort_objects(comparisons)
final_ranking = [a.get_item(x) for x in ranked]
print([x.name for x in final_ranking])'''

def find_elos(comps):
    elos = {}
    for (item1, item2) in comps:
        if item1 not in elos:
            elos[item1] = (1000, 0)
        if item2 not in elos:
            elos[item2] = (1000, 0)

    def Probability(rating1, rating2): 
        return 1.0 * 1.0 / (1 + 1.0 * pow(10, 1.0 * (rating1 - rating2) / 400)) 

    def EloRating(item1, item2): 
        def K_factor(item):
            if elos[item][1] <= 30:
                return 40
            elif elos[item][0] >= 2400:
                return 10
            else:
                return 20

        K1, K2 = K_factor(item1), K_factor(item2) 

        Pb = Probability(elos[item1][0], elos[item2][0]) 
        Pa = Probability(elos[item2][0], elos[item1][0]) 
    
        elos[item1] = (elos[item1][0] + K1 * (1 - Pa), elos[item1][1] + 1)
        elos[item2] = (elos[item2][0] + K2 * (0 - Pb), elos[item2][1] + 1)

    for (winner, loser) in comps:
        EloRating(winner, loser)

    return elos
        
a = ListManager()
comparisons = [(x.better, x.worse) for x in a.comp_list]
elos = find_elos(comparisons)
final_elos = {}
for item in elos:
    final_elos[a.get_item(item)] = elos[item]
print({k.get_name(): v for k, v in sorted(final_elos.items(), key=lambda item: item[1])})