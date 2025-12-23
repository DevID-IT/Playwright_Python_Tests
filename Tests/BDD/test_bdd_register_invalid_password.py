import allure
from faker import Faker
from playwright.sync_api import expect  
from pytest_bdd import scenario, given, when, then
import pytest

from Pages.homePage import HomePage

@pytest.fixture
def shared_data():
    return {}

@pytest.fixture
def home_page(page):
    return HomePage(page)

@pytest.fixture
def page(page):
    return page


@allure.feature("Registration")
@allure.story("User Registration")
@allure.title("Przypadek 04 - Rejestracja z niezgodnymi hasłami")
@allure.description("Test służy sprawdzeniu czy wpisując niezgodne hasła użytkownik dostanie informację o błędzie")
@scenario('../../features/registerUser.feature', 'Invalid user registration form - password mismatch')
def test_publish():
    pass

@allure.step("Navigate to Parabank home page")
@given('I am on the Parabank home page')
def go_to_home_page(home_page, shared_data):
    shared_data["homePage"] = home_page
    home_page.navigate()

@allure.step("Navigate to register form")
@given('I navigate to the registration page')
def navigate_to_register(shared_data):
    home_page = shared_data['homePage']
    home_page.click_go_to_register_form()

@allure.step("Fill in the registration form with password mismatch")
@when('Fill in the registration form with password mismatch')
def fill_register_form(shared_data):
    faker = Faker()
    username = 'Dawid6286'
    password = faker.password()
    shared_data['username'] = username
    home_page = shared_data['homePage'] 
    home_page.register(faker.first_name(), faker.last_name(), faker.street_name(), faker.city(), faker.state(), 
                                faker.zipcode(), faker.phone_number(), faker.ssn(), username, password, faker.password())
    

@allure.step("Verify error message")
@then('Verify error message')
def verify_message(page):
    expect_url = "https://parabank.parasoft.com/parabank/register.htm"
    expect(page).to_have_url(expect_url)
    expect(page.locator("span[id='repeatedPassword.errors']")).to_have_text(f"Passwords did not match.")  
