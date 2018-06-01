from unittest import TestCase
import responses

from adv.client import AdvClient
from adv.dctas import DCTA, class_from_type
from adv.widgets import TextWidget, ImageWidget, GroupWidget


class DCTATests(TestCase):
    maxDiff = None

    def setUp(self):
        self.client = AdvClient('test-api-key')
        self.dcta = DCTA(self.client, id=15, name='Test DCTA')
        self.client.dctas[15] = self.dcta

    def test_simple_deserialization(self):
        """
        passing `deserialize` an advocate client and valid DCTA
        data should create a DCTA object (include deserialized Widget
        objects)
        """
        dcta_data = {
            'id': 2,
            'name': 'Test DCTA',
            'global_styles': {
                'position': 'absolute',
                'top': '50%',
            },
            'widgets': [
                {
                    'id': 1,
                    'type': 'text',
                    'text': 'Hello!',
                },
                {
                    'id': 5,
                    'type': 'image',
                    'src': 'https://my/image.jpg',
                },
            ],
        }

        dcta = DCTA.deserialize(self.client, dcta_data)

        self.assertEqual(dcta.id, 2)
        self.assertEqual(dcta.name, 'Test DCTA')
        self.assertEqual(dcta.global_styles, {
            'position': 'absolute',
            'top': '50%',
        })
        self.assertEqual(dcta.widgets[0].__class__, TextWidget)
        self.assertEqual(dcta.widgets[1].__class__, ImageWidget)
        self.assertEqual(dcta.widgets[0].text, 'Hello!')
        self.assertEqual(dcta.widgets[1].src, 'https://my/image.jpg')

    @responses.activate
    def test_add_text_widget_creates_and_adds_widget(self):
        """
        Calling `add_text_widget` should create a new widget in the API,
        and the add that widget locally to the DCTA
        """
        self.assertEqual(len(self.dcta.widgets), 0)

        widget_response_data = {
            'text': 'I am a widget',
            'name': 'Test Text Widget',
            'broadcasters': [],
            'styles': {},
            'attributes': {},
            'id': 10,
            'dcta': self.dcta.id,
            'parent': None,
        }

        responses.add(
            responses.POST, 'https://api.adv.gg/v1/widgets/text/',
            json=widget_response_data, status=201,
        )

        self.dcta.add_text_widget(name='Test Text Widget', text='I am a widget')

        self.assertEqual(len(self.dcta.widgets), 1)
        self.assertEqual(self.dcta.widgets[0].dcta, self.dcta)
        self.assertEqual(self.dcta.widgets[0].text, 'I am a widget')

    @responses.activate
    def test_add_image_widget_creates_and_adds_widget(self):
        """
        Calling `add_image_widget` should create a new widget in the API,
        and the add that widget locally to the DCTA
        """
        self.assertEqual(len(self.dcta.widgets), 0)

        widget_response_data = {
            'src': 'https://my/image.jpg',
            'name': 'Test Image Widget',
            'broadcasters': [],
            'styles': {},
            'attributes': {},
            'id': 10,
            'dcta': self.dcta.id,
            'parent': None,
        }

        responses.add(
            responses.POST, 'https://api.adv.gg/v1/widgets/image/',
            json=widget_response_data, status=201,
        )

        self.dcta.add_image_widget(name='Test Image Widget', src='tests/test.png')

        self.assertEqual(len(self.dcta.widgets), 1)
        self.assertEqual(self.dcta.widgets[0].dcta, self.dcta)
        self.assertEqual(self.dcta.widgets[0].src, 'https://my/image.jpg')

    def test_simple_serialization(self):
        """
        Calling `serialize` on a DCTA should convert it (and contained widgets)
        to the appropriate dict data
        """
        # Manually creating widgets; Note: this would rarely/never happen in real usage, as
        # we'd want the Widgets to be created by the API to maintain consistency
        text_widget = TextWidget(
            self.client, name='Dummy Text Widget', text='Hello World',
            dcta=self.dcta.id, id=4,
        )
        image_widget = ImageWidget(
            self.client, name='Dummy Image Widget', src='https://my/image.jpg',
            dcta=self.dcta.id, id=5,
        )

        self.dcta.widgets.append(text_widget)
        self.dcta.widgets.append(image_widget)

        serialized_data = self.dcta.serialize()

        expected_data = {
            'name': 'Test DCTA',
            'global_styles': {},
            'id': self.dcta.id,
            'widgets': [
                {
                    'name': 'Dummy Text Widget',
                    'text': 'Hello World',
                    'broadcasters': [],
                    'styles': {},
                    'attributes': {},
                    'id': 4,
                    'dcta': self.dcta.id,
                    'parent': None,
                    'type': 'text',
                },
                {
                    'name': 'Dummy Image Widget',
                    'src': 'https://my/image.jpg',
                    'broadcasters': [],
                    'styles': {},
                    'attributes': {},
                    'id': 5,
                    'dcta': self.dcta.id,
                    'parent': None,
                    'type': 'image',
                },
            ],
        }

        self.assertEqual(serialized_data, expected_data)

    def test_class_from_type(self):
        """
        the `class_from_type` function should load a particular widget class from the given
        type text.  For example, the string 'text' should return the `TextWidget` class
        """
        self.assertEqual(TextWidget, class_from_type('text'))
        self.assertEqual(GroupWidget, class_from_type('group'))
        self.assertEqual(ImageWidget, class_from_type('image'))
