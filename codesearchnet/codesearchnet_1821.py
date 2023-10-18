def countOf(a, b):
    "Return the number of times b occurs in a."
    count = 0
    for i in a:
        if i == b:
            count += 1
    return count