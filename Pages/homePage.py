import logging
import time
import allure


class HomePage:
    def __init__(self, page):
        self.page = page
        self.logger = logging.getLogger(__name__)
        
    @allure.step("Navigating to Parabank home page")
    def navigate(self):
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.logger.info("Navigated to Parabank home page")

    @allure.step("Logging in with username: {username}")
    def login(self, username, password):
        self.page.locator("input[name='username']").fill(username)
        self.page.locator("input[name='password']").fill(password)
        self.page.locator("input[value='Log In']").click()
        self.logger.info("Inserted credentials and clicked Log In")

    @allure.step("Clicking on Register link to go to registration form")
    def click_go_to_register_form(self):
        self.page.get_by_role("link", name="Register").click()
        self.logger.info("Clicked on Register link to go to registration form")

    @allure.step("Registering new user with username: {username}")
    def register(self, firstName, lastName, street, city, state, zipCode, phoneNumber, ssn, username, password, confirmPassword):       
        self.page.locator("input[id='customer.firstName']").fill(firstName)
        self.page.locator("input[id='customer.lastName']").fill(lastName)
        self.page.locator("input[id='customer.address.street']").fill(street)
        self.page.locator("input[id='customer.address.city']").fill(city)
        self.page.locator("input[id='customer.address.state']").fill(state)
        self.page.locator("input[id='customer.address.zipCode']").fill(zipCode)
        self.page.locator("input[id='customer.phoneNumber']").fill(phoneNumber)
        self.page.locator("input[id='customer.ssn']").fill(ssn)
        self.page.locator("input[id='customer.username']").fill(username)
        self.page.locator("input[id='customer.password']").fill(password)
        self.page.locator("input[id='repeatedPassword']").fill(confirmPassword)
        self.page.get_by_role("button", name="Register").click()
        self.logger.info("Filled registration form and clicked Register")
