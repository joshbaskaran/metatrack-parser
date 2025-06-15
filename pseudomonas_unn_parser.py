import os
from pprint import pprint

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


# create pseudomonas project
def create_pseudomans_project():
    # read all projects
    projects = client.get(f"{API_BASE_URL}/projects/")

    if not projects.json():
        create_project = client.post(
            f"{API_BASE_URL}/projects/",
            headers={"Content-Type": "application/json"},
            json={"name": "pseudomonas", "description": "pseudomonas data from UNN"},
        )
        create_project.raise_for_status()
        return create_project.json()

    if projects.json():
        # check if pseudomonas already exists
        found = False
        for proj in projects.json():
            if proj["name"] == "pseudomonas":
                found = True
                return proj

        if not found:
            create_project = client.post(
                f"{API_BASE_URL}/projects/",
                headers={"Content-Type": "application/json"},
                json={
                    "name": "pseudomonas",
                    "description": "pseudomonas data from UNN",
                },
            )
            create_project.raise_for_status()
            return create_project.json()
    return {}


def create_investigation_if_not_exists(project_id):
    investigations = client.get(f"{API_BASE_URL}/projects/{project_id}/investigations/")
    investigations.raise_for_status()

    def create_investigation():
        invest = client.post(
            f"{API_BASE_URL}/projects/{project_id}/investigations/",
            headers={"Content-Type": "application/json"},
            json={
                "filename": "pseudomonas_unn.xlxs",
                "identifier": "pseudomonas",
                "title": "pseudomonas",
                "submissionDate": "",
                "publicReleaseDate": "",
                "ontologySourceReferences": "",
                "publications": [""],
                "people": [""],
                "studies": [""],
            },
        )
        invest.raise_for_status()
        return invest.json()

    if not investigations.json():
        return create_investigation()

    for inv in investigations.json():
        if inv["identifier"] == "pseudomonas":
            return inv

    return create_investigation()


if __name__ == "__main__":
    sing_in()

    project = create_pseudomans_project()
    investigation = create_investigation_if_not_exists(project["id"])

    pprint(investigation)

    sign_out()
