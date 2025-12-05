import allure
from playwright.sync_api import expect
import pytest


@allure.parent_suite("Testy automatyczne Parabank")
@allure.suite("Logowanie")
class TestLogin:
    wrong_login_credentials = [("Dawid6286", "wrong"), ("wrongUser", "Dawid6286")]
    field_missing_credentials = [("", ""), ("Dawid6286", ""), ("", "Dawid6286")]

    # @allure.sub_suite("Logowanie")
    @allure.title("Przypadek 01 - Zalogowanie poprawnymi danymi")
    @allure.description("Test służy sprawdzeniu czy wpisując dane prawidłowe zostanie użytkownik zalogowany")
    def test_login_success(self):
        self.home_page.navigate()
        self.home_page.login("Dawid6286", "Dawid6286")
        expect_url = "https://parabank.parasoft.com/parabank/overview.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("#showOverview > h1")).to_have_text("Accounts Overview")

    
    @pytest.mark.parametrize("username, password", wrong_login_credentials)
    @allure.title("Przypadek 02-03 - Zalogowanie błędnymi danymi")
    @allure.description("Test służy sprawdzeniu czy wpisując błędne dane logowania użytkownik nie zostanie zalogowany")
    def test_wrong_login(self, username, password):
        self.home_page.navigate()
        self.home_page.login(username, password)
        expect(self.page.locator("#rightPanel > h1.title")).to_have_text("Error!")
        expect(self.page.locator("#rightPanel > p.error")).to_have_text("The username and password could not be verified.") 

    @pytest.mark.parametrize("username, password", field_missing_credentials)
    @allure.title("Przypadek 04-06 - Logowanie bez podania danych")
    @allure.description("Test służy sprawdzeniu czy bez podania danych logowania użytkownik dostanie informację o braku informacji")
    def test_field_missing_login(self, username, password):
        self.home_page.navigate()
        self.home_page.login(username, password)
        expect(self.page.locator("#rightPanel > h1.title")).to_have_text("Error!")
        expect(self.page.locator("#rightPanel > p.error")).to_have_text("Please enter a username and password.")
