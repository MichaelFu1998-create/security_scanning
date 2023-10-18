def brandes_betweenness_centrality(graph, normalized=True):

    """ Betweenness centrality for nodes in the graph.
    
    Betweenness centrality is a measure of the number of shortests paths that pass through a node.
    Nodes in high-density areas will get a good score.
    
    The algorithm is Brandes' betweenness centrality,
    from NetworkX 0.35.1: Aric Hagberg, Dan Schult and Pieter Swart,
    based on Dijkstra's algorithm for shortest paths modified from Eppstein.
    https://networkx.lanl.gov/wiki
    
    """

    G = graph.keys()
    W = adjacency(graph)
    
    betweenness = dict.fromkeys(G, 0.0) # b[v]=0 for v in G
    for s in G: 
        S = [] 
        P = {} 
        for v in G: P[v] = [] 
        sigma = dict.fromkeys(G, 0) # sigma[v]=0 for v in G 
        D = {} 
        sigma[s] = 1
        seen = { s: 0 }  
        Q = [] # use Q as heap with (distance, node id) tuples 
        heapq.heappush(Q, (0, s, s)) 
        while Q:    
            (dist, pred, v) = heapq.heappop(Q) 
            if v in D: continue # already searched this node
            sigma[v] = sigma[v] + sigma[pred] # count paths 
            S.append(v) 
            D[v] = seen[v] 
            for w in graph[v].links:
                
                w = w.id
                vw_dist = D[v] + W[v][w]
                
                if w not in D and (w not in seen or vw_dist < seen[w]): 
                    seen[w] = vw_dist 
                    heapq.heappush(Q, (vw_dist, v, w)) 
                    P[w] = [v] 
                elif vw_dist == seen[w]: # handle equal paths 
                    sigma[w] = sigma[w] + sigma[v] 
                    P[w].append(v)
                    
        delta = dict.fromkeys(G,0)  
        while S: 
            w = S.pop() 
            for v in P[w]: 
                delta[v] = delta[v] + (float(sigma[v]) / float(sigma[w])) * (1.0 + delta[w]) 
            if w != s: 
                betweenness[w] = betweenness[w] + delta[w]

        #-----------------------------------
        if normalized:
            # Normalize between 0.0 and 1.0.
            m = max(betweenness.values())
            if m == 0: m = 1
        else:
            m = 1
            
        betweenness = dict([(id, w/m) for id, w in betweenness.iteritems()])
        return betweenness