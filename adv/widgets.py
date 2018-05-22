class Widget:
    # List of dictionaries with the following keys:
    #    `name`: the name of the extra field on the widget
    #    `default` (optional): the value to use if there is none passed into init
    extra_fields = []

    def __init__(self, client, *args, **kwargs):
        self.id = kwargs.get('id', None)
        self.parent = kwargs.get('parent', None)
        self.attributes = kwargs.get('attributes', {})
        self.styles = kwargs.get('styles', {})

        for field in self.extra_fields:
            try:
                setattr(
                    self, field['name'], kwargs.get(field['name'], field.get('default', None))
                )
            except KeyError:
                raise ValueError(
                    'All items in `extra_fields` must be a dictionary with a `name` key'
                )

        self.client = client

    @classmethod
    def deserialize(cls, client, widget_data):
        """
        Deserializes Widget data from dictionary
        """
        return cls(client, **widget_data)

    def serialize(self):
        """
        Serializes Widget data to dictionary
        """
        data = {
            'parent': self.parent,
            'attributes': self.attributes,
            'styles': self.styles,
        }

        for field in self.extra_fields:
            data['field'] = getattr(self, field['name'])

        if not self.is_new:
            data['id'] = self.id

        return data

    @property
    def is_new(self):
        return self.id is None


class TextWidget(Widget):
    extra_fields = [{'name': 'text'}]


class ImageWidget(Widget):
    extra_fields = [{'name': 'image'}]


class GroupWidget(Widget):
    pass
