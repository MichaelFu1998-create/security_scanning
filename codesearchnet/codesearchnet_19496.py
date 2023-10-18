def consistent_with(event, evidence):
    "Is event consistent with the given evidence?"
    return every(lambda (k, v): evidence.get(k, v) == v,
                 event.items())