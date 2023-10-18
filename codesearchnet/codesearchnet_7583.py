def _numpy_solver(A, B):
    """This function solve Ax=B directly without taking care of the input
    matrix properties.
    """
    x = numpy.linalg.solve(A, B)
    return x