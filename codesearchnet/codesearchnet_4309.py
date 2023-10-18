def create_review_node(self, review):
        """
        Return a review node.
        """
        review_node = BNode()
        type_triple = (review_node, RDF.type, self.spdx_namespace.Review)
        self.graph.add(type_triple)

        reviewer_node = Literal(review.reviewer.to_value())
        self.graph.add((review_node, self.spdx_namespace.reviewer, reviewer_node))
        reviewed_date_node = Literal(review.review_date_iso_format)
        reviewed_triple = (review_node, self.spdx_namespace.reviewDate, reviewed_date_node)
        self.graph.add(reviewed_triple)
        if review.has_comment:
            comment_node = Literal(review.comment)
            comment_triple = (review_node, RDFS.comment, comment_node)
            self.graph.add(comment_triple)

        return review_node