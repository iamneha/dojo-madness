from src.apis.routes import app


client = app.test_client()


class TestApis:

    def test_index_endpoint(self):
        response = client.get('/')
        assert response.status_code == 302  # redirect
