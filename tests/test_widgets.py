from unittest import TestCase

from adv.widgets import Widget, TextWidget, ImageWidget
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
        class ExtraFieldWidget(Widget):
            extra_fields = [
                {'name': 'test_field', 'default': 'some value'},
                {'name': 'another_field'}
            ]

        widget_data = {
            'parent': 1,
        }

        widget = ExtraFieldWidget.deserialize(self.client, widget_data)

        self.assertEqual(widget.parent, 1)
        self.assertEqual(widget.attributes, {})
        self.assertEqual(widget.styles, {})
        self.assertEqual(widget.test_field, 'some value')
        self.assertIsNone(widget.another_field)

    def test_TextWidget_creates_name_field(self):
        """
        TextWidget should create a text attribute, even if nothing is passed in
        """
        widget = TextWidget.deserialize(self.client)
        self.assertEqual(widget.text, '')

    def test_ImageWidget_creates_name_field(self):
        """
        ImageWidget should create a src attribute, even if nothing is passed in
        """
        widget = ImageWidget.deserialize(self.client)
        self.assertIsNone(widget.src)

    def test_basic_serializer(self):
        """
        A Widget's `serialize` function should transform all relevant data, including the widget
        "type", into a dictionary
        """
        widget = Widget(self.client, parent=1, styles={'top': '50%', 'left': '10px'})

        expected_data = {
            'parent': 1,
            'styles': {'top': '50%', 'left': '10px'},
            'attributes': {},
            'type': 'Widget',
        }

        self.assertEqual(widget.serialize(), expected_data)
