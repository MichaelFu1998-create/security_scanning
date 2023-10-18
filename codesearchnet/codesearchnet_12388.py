def add_download_total(rows):
    """Add a final row to rows showing the total downloads"""
    total_row = [""] * len(rows[0])
    total_row[0] = "Total"
    total_downloads, downloads_column = get_download_total(rows)
    total_row[downloads_column] = str(total_downloads)
    rows.append(total_row)

    return rows