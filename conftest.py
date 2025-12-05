import base64
import json
import os
import allure
from dotenv import load_dotenv
import pytest

from Pages.homePage import HomePage


load_dotenv()


class APIRequestContext:
    def __init__(self, playwright, base_url, email, password):
        self.anonim = self.anonymous_context(playwright, base_url)
        self.auth = self.auth_context(playwright, base_url, email, password)

    def anonymous_context(self, playwright, base_url):
        return playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={"Content-Type": "application/json"},
        )

    def auth_context(self, playwright, base_url, email, password):
        login_payload = {"email": email, "password": password}
        response = self.anonim.post("auth/login", data=json.dumps(login_payload))
        assert response.ok, f"Login failed: {response.status} {response.text()}"
        data = response.json()
        access_token = data["access_token"]

        context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
            }
        )
        check = context.get("users/me")
        assert check.ok, f"Token invalid: {check.status} {check.text()}"
        return context

        
    def dispose(self):
        self.anonim.dispose()
        self.auth.dispose()


@pytest.fixture(scope="session")
def api_request_context(playwright):
    base_url = "http://127.0.0.1:8000/"
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    context = APIRequestContext(playwright, base_url, email, password)
    yield context
    context.dispose()

@pytest.fixture(autouse=True)
def setup_pages(page, request):
    """
    Fixture dla całej klasy testowej.
    Tworzy instancje wszystkich potrzebnych Page Object.
    """
    request.cls.page = page
    request.cls.home_page = HomePage(page)
    # request.cls.dashboard_page = DashboardPage(page)
    # request.cls.login_page = LoginPage(page) 

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            png = page.screenshot()
            allure.attach(
                png, name="screenshot", attachment_type=allure.attachment_type.PNG
            )
