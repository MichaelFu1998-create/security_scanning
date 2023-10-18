def compare_graph_searchers():
    """Prints a table of results like this:
    >>> compare_graph_searchers()
    Searcher                      Romania(A, B)        Romania(O, N)         Australia          
    breadth_first_tree_search     <  21/  22/  59/B>   <1158/1159/3288/N>    <   7/   8/  22/WA>
    breadth_first_search          <   7/  11/  18/B>   <  19/  20/  45/N>    <   2/   6/   8/WA>
    depth_first_graph_search      <   8/   9/  20/B>   <  16/  17/  38/N>    <   4/   5/  11/WA>
    iterative_deepening_search    <  11/  33/  31/B>   < 656/1815/1812/N>    <   3/  11/  11/WA>
    depth_limited_search          <  54/  65/ 185/B>   < 387/1012/1125/N>    <  50/  54/ 200/WA>
    recursive_best_first_search   <   5/   6/  15/B>   <5887/5888/16532/N>   <  11/  12/  43/WA>"""
    compare_searchers(problems=[GraphProblem('A', 'B', romania),
                                GraphProblem('O', 'N', romania),
                                GraphProblem('Q', 'WA', australia)],
            header=['Searcher', 'Romania(A, B)', 'Romania(O, N)', 'Australia'])