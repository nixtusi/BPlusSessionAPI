#beefplus_login_api.py
# This script provides a Flask API to log in to the Beefplus system and retrieve session information.

from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

app = Flask(__name__)
BASE_URL = "https://beefplus.center.kobe-u.ac.jp"
LOGIN_PATH = "/saml/loginyu?disco=true"
TARGET_PATH = "/lms/timetable"

def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

@app.route('/login', methods=['POST'])
def login_and_get_session():
    data = request.get_json()
    number = data.get('student_number')
    password = data.get('password')
    if not number or not password:
        return jsonify({'error': 'student_number and password required'}), 400

    driver = create_driver()
    try:
        driver.get(BASE_URL + LOGIN_PATH)
        time.sleep(1)
        driver.find_element(By.ID, 'username').send_keys(number)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'kc-login').click()
        time.sleep(1)
        driver.get(BASE_URL + TARGET_PATH)
        time.sleep(1)
        return jsonify({
            'session_url': driver.current_url,
            'cookies': driver.get_cookies()
        })
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
