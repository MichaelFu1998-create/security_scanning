def job_title():
    """Return a random job title."""
    result = random.choice(get_dictionary('job_titles')).strip()
    result = result.replace('#{N}', job_title_suffix())
    return result