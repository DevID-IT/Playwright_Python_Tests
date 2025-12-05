import allure
from playwright.sync_api import expect
import pytest
from faker import Faker



@allure.parent_suite("Testy automatyczne Parabank")
@allure.suite("Rejestracja")
class TestRegister:
    def setup_method(self):
        self.faker = Faker()

    @allure.title("Przypadek 01 - Poprawna rejestracja użytkownika")
    @allure.description("Test służy sprawdzeniu czy wpisując dane prawidłowe zostanie użytkownik zarejestrowany")
    def test_register_success(self):
        username = self.faker.user_name()
        password = self.faker.password()
        self.home_page.navigate()
        self.home_page.click_go_to_register_form()
        self.home_page.register(self.faker.first_name(), self.faker.last_name(), self.faker.street_name(), self.faker.city(), self.faker.state(), 
                                self.faker.zipcode(), self.faker.phone_number(), self.faker.ssn(), username, password, password)
        expect_url = "https://parabank.parasoft.com/parabank/register.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("#rightPanel > h1.title")).to_have_text(f"Welcome {username}")
        expect(self.page.locator("#rightPanel > p")).to_have_text("Your account was created successfully. You are now logged in.")
        self.faker = Faker()

    @allure.title("Przypadek 02 - Rejestracja z istniejącym loginem")
    @allure.description("Test służy sprawdzeniu czy wpisując istniejący login użytkownik dostanie informację o błędzie")
    def test_register_with_existing_username(self):
        username = 'Dawid6286'
        password = self.faker.password()
        self.home_page.navigate()
        self.home_page.click_go_to_register_form()
        self.home_page.register(self.faker.first_name(), self.faker.last_name(), self.faker.street_name(), self.faker.city(), self.faker.state(), 
                                self.faker.zipcode(), self.faker.phone_number(), self.faker.ssn(), username, password, password)
        expect_url = "https://parabank.parasoft.com/parabank/register.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("span[id='customer.username.errors']")).to_have_text(f"This username already exists.")
        self.faker = Faker()

    @allure.title("Przypadek 03 - Rejestracja z pustymi polami")
    @allure.description("Test służy sprawdzeniu czy wszystkie pola obowiązkowe są sprawdzane podczas rejestracji")
    def test_register_validation(self):
        self.home_page.navigate()
        self.home_page.click_go_to_register_form()
        self.home_page.register('', '', '', '', '', '', '', '', '', '', '')
        expect_url = "https://parabank.parasoft.com/parabank/register.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("span[id='customer.firstName.errors']")).to_have_text(f"First name is required.")
        expect(self.page.locator("span[id='customer.lastName.errors']")).to_have_text(f"Last name is required.")
        expect(self.page.locator("span[id='customer.address.street.errors']")).to_have_text(f"Address is required.")
        expect(self.page.locator("span[id='customer.address.city.errors']")).to_have_text(f"City is required.")
        expect(self.page.locator("span[id='customer.address.state.errors']")).to_have_text(f"State is required.")
        expect(self.page.locator("span[id='customer.address.zipCode.errors']")).to_have_text(f"Zip Code is required.")
        expect(self.page.locator("span[id='customer.ssn.errors']")).to_have_text(f"Social Security Number is required.")
        expect(self.page.locator("span[id='customer.username.errors']")).to_have_text(f"Username is required.")
        expect(self.page.locator("span[id='customer.password.errors']")).to_have_text(f"Password is required.")
        expect(self.page.locator("span[id='repeatedPassword.errors']")).to_have_text(f"Password confirmation is required.")

    @allure.title("Przypadek 04 - Niepoprawne potwierdzenie hasła")
    @allure.description("Test służy sprawdzeniu czy użytkownik otrzyma informację o niepoprawnym potwierdzeniu hasła podczas rejestracji")
    def test_password_validation(self):
        self.home_page.navigate()
        self.home_page.click_go_to_register_form()
        self.home_page.register(self.faker.first_name(), self.faker.last_name(), self.faker.street_name(), self.faker.city(), self.faker.state(), 
                                self.faker.zipcode(), self.faker.phone_number(), self.faker.ssn(), self.faker.user_name(), self.faker.password(), self.faker.password())
        expect_url = "https://parabank.parasoft.com/parabank/register.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("span[id='repeatedPassword.errors']")).to_have_text(f"Passwords did not match.")