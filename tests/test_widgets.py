from unittest import TestCase

from adv.widgets import Widget
from adv.client import AdvocateClient


class WidgetTests(TestCase):
    def setUp(self):
        self.client = AdvocateClient('test-api-key')

    def test_simple_deserialization(self):
        """
        passing `deserialize` an advocate client and valid widget data
        should create a Widget object with the appropriate values set
        """
        widget_data = {
            'parent': 2,
            'attributes': {
                'class': 'my-widget',
            },
            'styles': {
                'position': 'absolute',
                'top': '50%',
            },
        }

        widget = Widget.deserialize(self.client, widget_data)

        self.assertEqual(widget.parent, 2)
        self.assertEqual(widget.attributes, {'class': 'my-widget'})
        self.assertEqual(widget.styles, {'position': 'absolute', 'top': '50%'})

    def test_deserialization_with_extra_fields(self):
        """
        subclassing Widget and adding `extra_fields` should allow deserialization
        for the extra fields in addition to the standard widget
        fields
        """
        pass
