def get_route_difference_with_other_db(self, other_gtfs, start_time, end_time, uniqueness_threshold=None,
                                           uniqueness_ratio=None):
        """
        Compares the routes based on stops in the schedule with the routes in another db and returns the ones without match.
        Uniqueness thresholds or ratio can be used to allow small differences
        :param uniqueness_threshold:
        :param uniqueness_ratio:
        :return:
        """
        from gtfspy.stats import frequencies_by_generated_route

        this_df = frequencies_by_generated_route(self, start_time, end_time)
        other_df = frequencies_by_generated_route(other_gtfs, start_time, end_time)
        this_routes = {x: set(x.split(',')) for x in this_df["route"]}
        other_routes = {x: set(x.split(',')) for x in other_df["route"]}
        # this_df["route_set"] = this_df.apply(lambda x: set(x.route.split(',')), axis=1)
        # other_df["route_set"] = other_df.apply(lambda x: set(x.route.split(',')), axis=1)

        this_uniques = list(this_routes.keys())
        other_uniques = list(other_routes.keys())
        print("initial routes A:", len(this_uniques))
        print("initial routes B:", len(other_uniques))
        for i_key, i in this_routes.items():
            for j_key, j in other_routes.items():
                union = i | j
                intersection = i & j
                symmetric_difference = i ^ j
                if uniqueness_ratio:
                    if len(intersection) / len(union) >= uniqueness_ratio:
                        try:
                            this_uniques.remove(i_key)
                            this_df = this_df[this_df["route"] != i_key]
                        except ValueError:
                            pass
                        try:
                            other_uniques.remove(j_key)
                            other_df = other_df[other_df["route"] != j_key]
                        except ValueError:
                            pass

        print("unique routes A", len(this_df))
        print("unique routes B", len(other_df))
        return this_df, other_df