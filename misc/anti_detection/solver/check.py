import requests

TARGET_URL = 'http://localhost:31516'

def main():
    res = requests.get(TARGET_URL)
    return res.status_code == 200

if __name__ == "__main__":
    main()