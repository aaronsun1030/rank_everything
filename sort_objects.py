from collections import deque
from compare_objects import ListManager

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


a = ListManager()
comparisons = [(x.better, x.worse) for x in a.comp_list]
ranked = sort_objects(comparisons)
final_ranking = [a.get_item(x) for x in ranked]
print([x.name for x in final_ranking])
