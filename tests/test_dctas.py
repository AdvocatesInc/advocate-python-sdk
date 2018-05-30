from unittest import TestCase

from adv.client import AdvClient
from adv.dctas import DCTA
from adv.widgets import TextWidget, ImageWidget


class DCTATests(TestCase):
    def setUp(self):
        self.client = AdvClient('test-api-key')

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

    def test_simple_serialization(self):
        """
        Calling `serialize` on a DCTA should convert it (and contained widgets)
        to the appropriate dict data
        """
        pass
