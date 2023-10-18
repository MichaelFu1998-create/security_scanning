def to_json(self):
        """ Method to call to get a serializable object for json.dump or jsonify based on the target

        :return: dict
        """
        if self.subreference is not None:
            return {
                "source": self.objectId,
                "selector": {
                    "type": "FragmentSelector",
                    "conformsTo": "http://ontology-dts.org/terms/subreference",
                    "value": self.subreference
                }
            }
        else:
            return {"source": self.objectId}