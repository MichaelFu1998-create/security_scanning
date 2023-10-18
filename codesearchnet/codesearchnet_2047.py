def roundfrac(intpart, fraction, digs):
    """Round or extend the fraction to size digs."""
    f = len(fraction)
    if f <= digs:
        return intpart, fraction + '0'*(digs-f)
    i = len(intpart)
    if i+digs < 0:
        return '0'*-digs, ''
    total = intpart + fraction
    nextdigit = total[i+digs]
    if nextdigit >= '5': # Hard case: increment last digit, may have carry!
        n = i + digs - 1
        while n >= 0:
            if total[n] != '9': break
            n = n-1
        else:
            total = '0' + total
            i = i+1
            n = 0
        total = total[:n] + chr(ord(total[n]) + 1) + '0'*(len(total)-n-1)
        intpart, fraction = total[:i], total[i:]
    if digs >= 0:
        return intpart, fraction[:digs]
    else:
        return intpart[:digs] + '0'*-digs, ''