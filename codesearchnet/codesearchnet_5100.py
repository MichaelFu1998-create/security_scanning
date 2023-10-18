def find_chunk (phrase, np):
    """
    leverage noun phrase chunking
    """
    for i in iter(range(0, len(phrase))):
        parsed_np = find_chunk_sub(phrase, np, i)

        if parsed_np:
            return parsed_np