
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


URL = "http://localhost:5001"


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,800")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


def test_registration_page(driver):
    driver.get(URL)

    assert driver.title == "Registration Form"
    assert driver.find_element(By.ID, "name").is_displayed()
    assert driver.find_element(By.ID, "email").is_displayed()
    assert driver.find_element(By.ID, "password").is_displayed()


def test_valid_registration(driver):
    driver.get(URL)

    driver.find_element(By.ID, "name").send_keys("Greeshma")
    driver.find_element(By.ID, "email").send_keys(
        "greeshma@example.com"
    )
    driver.find_element(By.ID, "password").send_keys("secret123")
    driver.find_element(By.ID, "submit").click()

    assert "Welcome, Greeshma!" in driver.find_element(
        By.ID, "message"
    ).text


def test_empty_fields(driver):
    driver.get(URL)

    driver.find_element(By.ID, "submit").click()

    valid = driver.execute_script(
        "return document.querySelector('form').checkValidity()"
    )

    assert valid is False


def test_invalid_email(driver):
    driver.get(URL)

    driver.find_element(By.ID, "name").send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("invalid-email")
    driver.find_element(By.ID, "password").send_keys("secret123")

    valid = driver.execute_script(
        "return document.getElementById('email').checkValidity()"
    )

    assert valid is False
