def __calculate_elbows(self):
        """!
        @brief Calculates potential elbows.
        @details Elbow is calculated as a distance from each point (x, y) to segment from kmin-point (x0, y0) to kmax-point (x1, y1).

        """

        x0, y0 = 0.0, self.__wce[0]
        x1, y1 = float(len(self.__wce)), self.__wce[-1]

        for index_elbow in range(1, len(self.__wce) - 1):
            x, y = float(index_elbow), self.__wce[index_elbow]

            segment = abs((y0 - y1) * x + (x1 - x0) * y + (x0 * y1 - x1 * y0))
            norm = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            distance = segment / norm

            self.__elbows.append(distance)