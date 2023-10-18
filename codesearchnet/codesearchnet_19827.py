def htmlListToTR(l,trClass=None,tdClass=None,td1Class=None):
    """
    turns a list into a <tr><td>something</td></tr>
    call this when generating HTML tables dynamically.
    """
    html="<tr>"
    for item in l:
        if 'array' in str(type(item)):
            item=item[0] #TODO: why is this needed
        html+="<td>%s</td>"%item
    html+="</tr>"
    if trClass:
        html=html.replace("<tr>",'<tr class="%s">'%trClass)
    if td1Class:
        html=html.replace("<td>",'<td class="%s">'%td1Class,1)
    if tdClass:
        html=html.replace("<td>",'<td class="%s">'%tdClass)


    return html