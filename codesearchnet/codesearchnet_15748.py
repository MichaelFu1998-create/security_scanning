def title(words_quantity=4):
    """Return a random sentence to be used as e.g. an e-mail subject."""
    result = words(quantity=words_quantity)
    result += random.choice('?.!')
    return result.capitalize()