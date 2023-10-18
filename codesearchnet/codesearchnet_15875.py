def run(self):
        """Perform the Oct2Py speed analysis.

        Uses timeit to test the raw execution of an Octave command,
        Then tests progressively larger array passing.

        """
        print('Oct2Py speed test')
        print('*' * 20)
        time.sleep(1)

        print('Raw speed: ')
        avg = timeit.timeit(self.raw_speed, number=10) / 10
        print('    {0:0.01f} usec per loop'.format(avg * 1e6))
        sides = [1, 10, 100, 1000]
        runs = [10, 10, 10, 5]
        for (side, nruns) in zip(sides, runs):
            self.array = np.reshape(np.arange(side ** 2), (-1))
            print('Put {0}x{1}: '.format(side, side))
            avg = timeit.timeit(self.large_array_put, number=nruns) / nruns
            print('    {0:0.01f} msec'.format(avg * 1e3))

            print('Get {0}x{1}: '.format(side, side))
            avg = timeit.timeit(self.large_array_get, number=nruns) / nruns
            print('    {0:0.01f} msec'.format(avg * 1e3))

        self.octave.exit()
        print('*' * 20)
        print('Test complete!')