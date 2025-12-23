import allure
from faker import Faker
from playwright.sync_api import expect  
from pytest_bdd import scenario, given, when, then, parsers
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
@allure.title("Przypadek 01 - Poprawna rejestracja użytkownika")
@allure.description("Test służy sprawdzeniu czy wpisując dane prawidłowe zostanie użytkownik zarejestrowany")
@scenario('../../features/registerUser.feature', 'Successful user registration')
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

@allure.step("Fill registration form with valid data")
@when(parsers.parse('I fill in the registration form with valid details for user {username}, {password}'))
def fill_register_form(shared_data, username, password):
    faker = Faker()
    shared_data['username'] = username
    home_page = shared_data['homePage'] 
    home_page.register(faker.first_name(), faker.last_name(), faker.street_name(), faker.city(), faker.state(), 
                                faker.zipcode(), faker.phone_number(), faker.ssn(), username, password, password)

@allure.step("Verify success message")
@then('I should see a confirmation message indicating successful registration')
def verify_success(page, shared_data):
    expect_url = "https://parabank.parasoft.com/parabank/register.htm"
    expect(page).to_have_url(expect_url)
    expect(page.locator("#rightPanel > h1.title")).to_have_text(f"Welcome {shared_data['username']}")
    expect(page.locator("#rightPanel > p")).to_have_text("Your account was created successfully. You are now logged in.")   
