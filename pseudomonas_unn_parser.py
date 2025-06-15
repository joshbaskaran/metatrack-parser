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


def get_projects():
    projects_req = client.get(f"{API_BASE_URL}/projects")
    projects_req.raise_for_status()
    return projects_req.json()


def get_investigation(project_id):
    investigations_req = client.get(
        f"{API_BASE_URL}/projects/{project_id}/investigations"
    )
    investigations_req.raise_for_status()
    return investigations_req.json()


def get_study(project_id, investigation_id):
    study_req = client.get(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/studies"
    )
    study_req.raise_for_status()
    return study_req.json()


def get_assay(project_id, investigation_id, study_id):
    assay_req = client.get(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/studies/{study_id}/assays"
    )
    assay_req.raise_for_status()
    return assay_req.json()


def create_base_ontology(project_id, investigation_id):
    create_ontology_source_req = client.post(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/ontologySources/",
        headers={"Content-Type": "application/json"},
        json={
            "file": "pseudomonas_unn_ontologies.tsx",
            "version": "-1.1.0",
            "name": "pseudomonas_unn_ontologies",
            "description": "custom ontology source for the pseudomonas unn project",
        },
    )
    create_ontology_source_req.raise_for_status()
    return create_ontology_source_req.json()


def add_new_annotation(
    project_id,
    investigation_id,
    source_id,
    term_source,
    term_accession,
    annotation_value,
):
    new_annotation_req = client.post(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/ontology/{source_id}/ontologyAnnotations/",
        headers={"Content-Type": "application/json"},
        json={
            "annotationValue": annotation_value,
            "termSource": term_source,
            "termAccession": term_accession,
        },
    )
    new_annotation_req.raise_for_status()
    return new_annotation_req.json()


def populate_ontologies(project_id, investigation_id):
    # create a custom ontology source
    get_ontologies_req = client.get(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/ontologySources/"
    )
    get_ontologies_req.raise_for_status()

    ontology_source = None
    for source in get_ontologies_req.json():
        if source["name"] == "pseudomonas_unn_ontologies":
            ontology_source = source

    if ontology_source is None:
        ontology_source = create_base_ontology(project_id, investigation_id)
        ontology_source = ontology_source[0]

    pprint(ontology_source)

    # get existing annotations
    annotations_req = client.get(
        f"{API_BASE_URL}/projects/{project_id}/investigations/{investigation_id}/ontologySources/"
    )
    annotations_req.raise_for_status()
    annotations = annotations_req.json()

    pprint(annotations)

    # loop through annotations to add
    new_annotations = [
        {
            1: [
                "Pseudomonas aeruginosa",
            ]
        }
    ]
    # check if annotation already exists
    # add if not


def main():
    sing_in()

    projects = get_projects()
    pseudomonas_proj_id = projects[0]["id"]
    print("Project ID:", pseudomonas_proj_id)

    investigations = get_investigation(pseudomonas_proj_id)
    pseudomonas_investigation_id = investigations[0]["id"]
    print("Investigation ID:", pseudomonas_investigation_id)

    studies = get_study(pseudomonas_proj_id, pseudomonas_investigation_id)
    study_id = studies[0]["id"]
    print("Study ID:", study_id)

    assays = get_assay(
        pseudomonas_proj_id, pseudomonas_investigation_id, studies[0]["id"]
    )
    print("Assay ID:", assays[0]["id"])

    populate_ontologies(pseudomonas_proj_id, pseudomonas_investigation_id)

    sign_out()


if __name__ == "__main__":
    main()
