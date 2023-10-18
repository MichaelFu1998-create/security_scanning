def unexpo(intpart, fraction, expo):
    """Remove the exponent by changing intpart and fraction."""
    if expo > 0: # Move the point left
        f = len(fraction)
        intpart, fraction = intpart + fraction[:expo], fraction[expo:]
        if expo > f:
            intpart = intpart + '0'*(expo-f)
    elif expo < 0: # Move the point right
        i = len(intpart)
        intpart, fraction = intpart[:expo], intpart[expo:] + fraction
        if expo < -i:
            fraction = '0'*(-expo-i) + fraction
    return intpart, fraction