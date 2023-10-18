def show_evolution(observer, start_iteration = 0, stop_iteration=None, ax=None, display=True):
        """!
        @brief Displays evolution of fitness function for the best chromosome, for the current best chromosome and
                average value among all chromosomes.
        
        @param[in] observer (ga_observer): Genetic algorithm observer that was used for collecting evolution in the algorithm and
                    where whole required information for visualization is stored.
        @param[in] start_iteration (uint): Iteration from that evolution should be shown.
        @param[in] stop_iteration (uint): Iteration after that evolution shouldn't be shown.
        @param[in] ax (Axes): Canvas where evolution should be displayed.
        @param[in] display (bool): If 'True' then visualization of the evolution will be shown by the function.
                    This argument should be 'False' if you want to add something else to the canvas and display it later.
        
        @return (Axis) Canvas where evolution was shown.
        
        """
        
        if (ax is None):
            _, ax = plt.subplots(1)
            ax.set_title("Evolution")
        
        if stop_iteration is None:
            stop_iteration = len(observer)
        
        line_best, = ax.plot(observer.get_global_best()['fitness_function'][start_iteration:stop_iteration], 'r')
        line_current, = ax.plot(observer.get_population_best()['fitness_function'][start_iteration:stop_iteration], 'k')
        line_mean, = ax.plot(observer.get_mean_fitness_function()[start_iteration:stop_iteration], 'c')

        if start_iteration < (stop_iteration - 1):
            ax.set_xlim([start_iteration, (stop_iteration - 1)])
        
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Fitness function")
        ax.legend([line_best, line_current, line_mean], ["The best pop.", "Cur. best pop.", "Average"], prop={'size': 10})
        ax.grid()

        if display is True:
            plt.show()
        
        return ax