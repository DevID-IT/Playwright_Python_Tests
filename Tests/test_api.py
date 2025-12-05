import datetime
import json
import os
from faker import Faker



class TestAPI:
    def setup_method(self):
        self.faker = Faker()

    def test_register_user(self, api_request_context):
        email = self.faker.email()
        new_user_payload = {
            "email": email,
            "password": self.faker.password(),
        }

        response = api_request_context.anonim.post("auth/register", data=json.dumps(new_user_payload))
        assert response.status == 201
        json_data = response.json()
        assert json_data["id"] > 0
        assert json_data["email"] == email
        assert json_data["is_active"] == True
        assert datetime.datetime.now().strftime("%Y-%m-%d") in json_data["created_at"]


    def test_login_user(self, api_request_context):
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")
        new_user_payload = {
            "email": email,
            "password":password,
        }

        response = api_request_context.anonim.post("auth/login", data=json.dumps(new_user_payload))
        assert response.status == 200

    def test_create_car(self, api_request_context):
        make = self.faker.word()
        model = self.faker.word()
        year = self.faker.year()
        price = self.faker.random_number(digits=5)
        description = self.faker.sentence()

        new_car_payload = {
            "make": make,
            "model": model,
            "year": year,
            "price": price,
            "description": description
        }   
        response = api_request_context.auth.post("cars", data=json.dumps(new_car_payload))
        assert response.status == 201
        json_data = response.json()
        assert json_data["make"] == make
        assert json_data["model"] == model
        assert str(json_data["year"]) == year
        assert json_data["status"] == "available"
        assert json_data["description"] == description
        assert json_data["owner_id"] == None
        assert json_data["price"] == price
        assert json_data["damages"] == []
        assert datetime.datetime.now().strftime("%Y-%m-%d") in json_data["created_at"]
    