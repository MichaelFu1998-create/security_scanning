def write_annotation(annotation, out):
    """
    Write the fields of a single annotation to out.
    """
    out.write('# Annotation\n\n')
    write_value('Annotator', annotation.annotator, out)
    write_value('AnnotationDate', annotation.annotation_date_iso_format, out)
    if annotation.has_comment:
        write_text_value('AnnotationComment', annotation.comment, out)
    write_value('AnnotationType', annotation.annotation_type, out)
    write_value('SPDXREF', annotation.spdx_id, out)