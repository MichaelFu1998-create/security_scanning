def link_to_modal(link_text, index, autoescape=True):  # pylint: disable=unused-argument
    """
    Django template filter that returns an anchor with attributes useful for course modal selection.

    General Usage:
        {{ link_text|link_to_modal:index }}

    Examples:
        {{ course_title|link_to_modal:forloop.counter0 }}
        {{ course_title|link_to_modal:3 }}
        {{ view_details_text|link_to_modal:0 }}
    """
    link = (
        '<a'
        ' href="#!"'
        ' class="text-underline view-course-details-link"'
        ' id="view-course-details-link-{index}"'
        ' data-toggle="modal"'
        ' data-target="#course-details-modal-{index}"'
        '>{link_text}</a>'
    ).format(
        index=index,
        link_text=link_text,
    )
    return mark_safe(link)