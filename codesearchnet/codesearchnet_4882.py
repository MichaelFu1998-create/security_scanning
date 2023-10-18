def animate(self, animation_velocity=75, movie_fps=25, movie_filename=None):
        """!
        @brief Animates clustering process that is performed by BANG algorithm.

        @param[in] animation_velocity (uint): Interval between frames in milliseconds (for run-time animation only).
        @param[in] movie_fps (uint): Defines frames per second (for rendering movie only).
        @param[in] movie_filename (string): If it is specified then animation will be stored to file that is specified in this parameter.

        """
        def init_frame():
            self.__figure.clf()
            self.__ax = self.__figure.add_subplot(1, 1, 1)
            self.__figure.suptitle("BANG algorithm", fontsize=18, fontweight='bold')

            for point in self.__directory.get_data():
                self.__ax.plot(point[0], point[1], color='red', marker='.')

            return frame_generation(0)


        def frame_generation(index_iteration):
            if self.__current_level < self.__directory.get_height():
                block = self.__level_blocks[self.__current_block]
                self.__draw_block(block)
                self.__increment_block()

            else:
                if self.__special_frame == 0:
                    self.__draw_leaf_density()

                elif self.__special_frame == 15:
                    self.__draw_clusters()

                elif self.__special_frame == 30:
                    self.__figure.clf()
                    self.__ax = self.__figure.add_subplot(1, 1, 1)
                    self.__figure.suptitle("BANG algorithm", fontsize=18, fontweight='bold')

                    self.__draw_clusters()

                self.__special_frame += 1



        iterations = len(self.__directory) + 60
        # print("Total number of iterations: %d" % iterations)
        cluster_animation = animation.FuncAnimation(self.__figure, frame_generation, iterations,
                                                    interval=animation_velocity,
                                                    init_func=init_frame,
                                                    repeat_delay=5000)

        if movie_filename is not None:
            cluster_animation.save(movie_filename, writer = 'ffmpeg', fps = movie_fps, bitrate = 3500)
        else:
            plt.show()