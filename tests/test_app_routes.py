from app import app


class TestShowIndex:
    """Тестирование функции show_index."""

    def test_show_index(self):
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200

    def test_home_page_post(self):
        with app.test_client() as client:
            response = client.post('/')
            assert response.status_code == 405

