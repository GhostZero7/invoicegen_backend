
import requests
import json

def test_login():
    url = "http://localhost:8080/auth/login"
    payload = {
        "email": "accountant1@invoicegen.com",
        "password": "Account123!"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Attempting login to {url}...")
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_login()
