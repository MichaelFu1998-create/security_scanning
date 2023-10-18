def _plot_dag(dag, results, snames):
    """
    makes plot to help visualize the DAG setup. For developers only.
    """
    try:
        import matplotlib.pyplot as plt
        from matplotlib.dates import date2num
        from matplotlib.cm import gist_rainbow

        ## first figure is dag layout
        plt.figure("dag_layout", figsize=(10, 10))
        nx.draw(dag,
                pos=nx.spring_layout(dag),
                node_color='pink',
                with_labels=True)
        plt.savefig("./dag_layout.png", bbox_inches='tight', dpi=200)

        ## second figure is times for steps
        pos = {}
        colors = {}

        for node in dag:
            #jobkey = "{}-{}".format(node, sample)
            mtd = results[node].metadata
            start = date2num(mtd.started)
            #runtime = date2num(md.completed)# - start
            ## sample id to separate samples on x-axis
            _, _, sname = node.split("-", 2)
            sid = snames.index(sname)
            ## 1e6 to separate on y-axis
            pos[node] = (start+sid, start*1e6)
            colors[node] = mtd.engine_id

        ## x just spaces out samples;
        ## y is start time of each job with edge leading to next job
        ## color is the engine that ran the job
        ## all jobs were submitted as 3 second wait times
        plt.figure("dag_starttimes", figsize=(10, 16))
        nx.draw(dag, pos,
                node_list=colors.keys(),
                node_color=colors.values(),
                cmap=gist_rainbow,
                with_labels=True)
        plt.savefig("./dag_starttimes.png", bbox_inches='tight', dpi=200)

    except Exception as inst:
        LOGGER.warning(inst)