def fix_journal_name(journal, knowledge_base):
    """Convert journal name to Inspire's short form."""
    if not journal:
        return '', ''
    if not knowledge_base:
        return journal, ''
    if len(journal) < 2:
        return journal, ''
    volume = ''
    if (journal[-1] <= 'Z' and journal[-1] >= 'A') \
            and (journal[-2] == '.' or journal[-2] == ' '):
        volume += journal[-1]
        journal = journal[:-1]
    journal = journal.strip()

    if journal.upper() in knowledge_base:
        journal = knowledge_base[journal.upper()].strip()
    elif journal in knowledge_base:
        journal = knowledge_base[journal].strip()
    elif '.' in journal:
        journalnodots = journal.replace('. ', ' ')
        journalnodots = journalnodots.replace('.', ' ').strip().upper()
        if journalnodots in knowledge_base:
            journal = knowledge_base[journalnodots].strip()

    journal = journal.replace('. ', '.')
    return journal, volume