def clone_with_updates(self, **kwargs):
        """Returns new BindingPrediction with updated fields"""
        fields_dict = self.to_dict()
        fields_dict.update(kwargs)
        return BindingPrediction(**fields_dict)