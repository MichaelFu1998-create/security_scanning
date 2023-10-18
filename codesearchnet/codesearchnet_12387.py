def get_download_total(rows):
    """Return the total downloads, and the downloads column"""
    headers = rows.pop(0)
    index = headers.index('download_count')
    total_downloads = sum(int(row[index]) for row in rows)

    rows.insert(0, headers)
    return total_downloads, index