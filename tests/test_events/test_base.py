from unittest import TestCase
from fastapi.testclient import TestClient
from document_filling_tool.app.application import create_application


class TestBaseEventHandler(TestCase):
    def test_startup_handler(self):
        app = create_application()
        with self.assertLogs('document_filling_tool', level='INFO') as cm:

            with TestClient(app):
                pass
            self.assertEqual(cm.output,
                             ['INFO:document_filling_tool:Starting up ...',
                              'INFO:document_filling_tool:Shutting down ...'])
