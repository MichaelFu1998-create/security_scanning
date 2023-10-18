def SyntheticRestaurant(n=20):
    "Generate a DataSet with n examples."
    def gen():
        example = map(random.choice, restaurant.values)
        example[restaurant.target] = Fig[18,2](example)
        return example
    return RestaurantDataSet([gen() for i in range(n)])