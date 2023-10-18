def draw_cornu_bezier(x0, y0, t0, t1, s0, c0, flip, cs, ss, cmd, scale, rot):

    """ Mark Meyer's code draws elegant CURVETO segments.
    """

    s = None
    for j in range(0, 5):
        # travel along the function two points at a time (at time t and t2)
        # the first time through we'll need to get both points
        # after that we only need the second point because the old second point
        # becomes the new first point
        t = j * .2
        t2 = t+ .2
        
        curvetime = t0 + t * (t1 - t0)
        curvetime2 = t0 + t2 * (t1 - t0)
        Dt = (curvetime2 - curvetime) * scale
        
        if not s:
            # get first point
            # avoid calling this again: the next time though x,y will equal x3, y3
            s, c = eval_cornu(curvetime)
            s *= flip
            s -= s0
            c -= c0
            # calculate derivative of fresnel function at point to get tangent slope
            # just take the integrand of the fresnel function
            dx1 =  cos(pow(curvetime, 2) + (flip * rot))  
            dy1 =  flip * sin(pow(curvetime, 2) + (flip *rot))
            # x,y = first point on function
            x = ((c * cs - s * ss) +x0)
            y = ((s * cs + c * ss) + y0)

        #evaluate the fresnel further along the function to look ahead to the next point
        s2,c2 = eval_cornu(curvetime2) 
        s2 *= flip
        s2 -= s0
        c2 -= c0

        dx2 = cos(pow(curvetime2, 2) + (flip * rot)) 
        dy2 = flip * sin(pow(curvetime2, 2) + (flip * rot))
        # x3, y3 = second point on function
        x3 = ((c2 * cs - s2 * ss)+x0)
        y3 = ((s2 * cs + c2 * ss)+y0)

        # calculate control points
        x1 = (x + ((Dt/3.0) * dx1))
        y1 = (y + ((Dt/3.0) * dy1))   
        x2 = (x3 - ((Dt/3.0) * dx2))
        y2 = (y3 - ((Dt/3.0) * dy2))

        if cmd == 'moveto':
            print_pt(x, y, cmd)
            cmd = 'curveto'
        print_crv(x1, y1, x2, y2, x3, y3)
                    
        dx1, dy1 = dx2, dy2
        x,y = x3, y3
        
    return cmd