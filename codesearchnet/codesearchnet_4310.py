def create_annotation_node(self, annotation):
        """
        Return an annotation node.
        """
        annotation_node = URIRef(str(annotation.spdx_id))
        type_triple = (annotation_node, RDF.type, self.spdx_namespace.Annotation)
        self.graph.add(type_triple)

        annotator_node = Literal(annotation.annotator.to_value())
        self.graph.add((annotation_node, self.spdx_namespace.annotator, annotator_node))
        annotation_date_node = Literal(annotation.annotation_date_iso_format)
        annotation_triple = (annotation_node, self.spdx_namespace.annotationDate, annotation_date_node)
        self.graph.add(annotation_triple)
        if annotation.has_comment:
            comment_node = Literal(annotation.comment)
            comment_triple = (annotation_node, RDFS.comment, comment_node)
            self.graph.add(comment_triple)
        annotation_type_node = Literal(annotation.annotation_type)
        annotation_type_triple = (annotation_node, self.spdx_namespace.annotationType, annotation_type_node)
        self.graph.add(annotation_type_triple)

        return annotation_node