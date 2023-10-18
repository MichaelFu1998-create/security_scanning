def show_time_signal(pcnn_output_dynamic):
        """!
        @brief Shows time signal (signal vector information) using network dynamic during simulation.
        
        @param[in] pcnn_output_dynamic (pcnn_dynamic): Output dynamic of the pulse-coupled neural network.
        
        """
        
        time_signal = pcnn_output_dynamic.allocate_time_signal()
        time_axis = range(len(time_signal))
        
        plt.subplot(1, 1, 1)
        plt.plot(time_axis, time_signal, '-')
        plt.ylabel("G (time signal)")
        plt.xlabel("t (iteration)")
        plt.grid(True)
        
        plt.show()