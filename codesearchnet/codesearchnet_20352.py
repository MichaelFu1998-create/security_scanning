def chop(list_, n):
    "Chop list_ into n chunks. Returns a list."
    # could look into itertools also, might be implemented there
    size = len(list_)
    each = size // n
    if each == 0:
        return [list_]
    chopped = []
    for i in range(n):
        start = i * each
        end = (i+1) * each
        if i == (n - 1):
        # make sure we get all items, let last worker do a litte more
            end = size
        chopped.append(list_[start:end])
    return chopped