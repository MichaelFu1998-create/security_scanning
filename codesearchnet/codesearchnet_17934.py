def sphere_constrained_cubic(dr, a, alpha):
    """
    Sphere generated by a cubic interpolant constrained to be (1,0) on
    (r0-sqrt(3)/2, r0+sqrt(3)/2), the size of the cube in the (111) direction.
    """
    sqrt3 = np.sqrt(3)

    b_coeff = a*0.5/sqrt3*(1 - 0.6*sqrt3*alpha)/(0.15 + a*a)
    rscl = np.clip(dr, -0.5*sqrt3, 0.5*sqrt3)

    a, d = rscl + 0.5*sqrt3, rscl - 0.5*sqrt3
    return alpha*d*a*rscl + b_coeff*d*a - d/sqrt3