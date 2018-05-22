# from .widgets import Widget


class DCTA:
    def __init__(self, client, id=None, name='',  widgets={}, global_styles={}):
        self.id = id
        self.global_styles = global_styles
        self.name = name

        self.widgets = widgets

    def __str__(self):
        return self.name

    @classmethod
    def deserialize(cls, client, dcta_data):
        """
        Deserializes DCTA from dictionary
        """
        # widgets = dcta_data.pop('widgets', [])

        return cls(client, **dcta_data)
