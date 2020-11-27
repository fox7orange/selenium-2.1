import pytest
from Apps.app import Application


@pytest.fixture
def app(request):
    app = Application()
    request.addfinalizer(app.quit)
    return app
