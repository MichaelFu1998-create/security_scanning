def sum_out(var, factors, bn):
    "Eliminate var from all factors by summing over its values."
    result, var_factors = [], []
    for f in factors:
        (var_factors if var in f.vars else result).append(f)
    result.append(pointwise_product(var_factors, bn).sum_out(var, bn))
    return result