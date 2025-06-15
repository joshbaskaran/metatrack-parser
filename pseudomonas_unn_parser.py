import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

client = httpx.Client()


# Sing in to metatrack
def sing_in():
    sing_in_req = client.post(
        f"{API_BASE_URL}/api/auth/sign-in/email",
        headers={"Content-Type": "application/json"},
        json={
            "email": USERNAME,
            "password": PASSWORD,
            "callbackURL": "/",
            "rememberMe": True,
        },
    )
    sing_in_req.raise_for_status()


def sign_out():
    sign_out_req = client.post(
        f"{API_BASE_URL}/api/auth/sign-out",
        headers={"Content-Type": "application/json"},
        json={},
    )
    sign_out_req.raise_for_status()


def main():
    sing_in()

    sign_out()


if __name__ == "__main__":
    main()
