import allure
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
@allure.title("Przypadek 03 - Rejestracja z pustymi polami")
@allure.description("Test służy sprawdzeniu czy wszystkie pola obowiązkowe są sprawdzane podczas rejestracji")
@scenario('../../features/registerUser.feature', 'Invalid user registration form - obligatory fields')
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

@allure.step("Save form with empty obligatory fields")
@when('Save form with empty obligatory fields')
def fill_register_form(shared_data):
    home_page = shared_data['homePage'] 
    home_page.register('', '', '', '', '', '', '', '', '', '', '')
        
@allure.step("Verify error message")
@then('Verify error message')
def verify_message(page):
    expect_url = "https://parabank.parasoft.com/parabank/register.htm"
    expect(page).to_have_url(expect_url)
    expect(page.locator("span[id='customer.firstName.errors']")).to_have_text(f"First name is required.")
    expect(page.locator("span[id='customer.lastName.errors']")).to_have_text(f"Last name is required.")
    expect(page.locator("span[id='customer.address.street.errors']")).to_have_text(f"Address is required.")
    expect(page.locator("span[id='customer.address.city.errors']")).to_have_text(f"City is required.")
    expect(page.locator("span[id='customer.address.state.errors']")).to_have_text(f"State is required.")
    expect(page.locator("span[id='customer.address.zipCode.errors']")).to_have_text(f"Zip Code is required.")
    expect(page.locator("span[id='customer.ssn.errors']")).to_have_text(f"Social Security Number is required.")
    expect(page.locator("span[id='customer.username.errors']")).to_have_text(f"Username is required.")
    expect(page.locator("span[id='customer.password.errors']")).to_have_text(f"Password is required.")
    expect(page.locator("span[id='repeatedPassword.errors']")).to_have_text(f"Password confirmation is required.")
