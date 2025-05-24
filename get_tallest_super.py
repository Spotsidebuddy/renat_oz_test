import requests


def get_tallest_super(gender: str, has_job: bool) -> str:
    check_data(gender, has_job)
    all_supers = get_all_supers()
    assert_response(all_supers)
    tallest_super = get_tallest(all_supers, gender, has_job)
    if not tallest_super:
        raise ValueError('No such superhero found!')
    return tallest_super['name']


def check_data(gender: str, has_job: bool) -> None:
    if gender not in ['Male', 'Female']:
        raise ValueError('Gender should be "Male" or "Female".')
    if not isinstance(has_job, bool):
        raise TypeError("Argument 'has_job' should be boolean type")

def get_all_supers() -> list[dict]:
    url = "https://akabab.github.io/superhero-api/api/all.json"
    all_supers = requests.get(url)
    status_code = all_supers.status_code
    check_connection(status_code)
    supers_list = all_supers.json()
    return supers_list


def check_connection(status_code) -> None:
    if status_code != 200:
        raise ConnectionError("Request could not be completed!")


def assert_response(data: list[dict]) -> None:
    if not isinstance(data, list):
        raise TypeError("Wrong data recieved. Could not process")

    if not data:
        raise ValueError("Empty response body")

    if not all(isinstance(item, dict) for item in data):
        raise TypeError("Wrong data structure in response body")

    if not all(item for item in data):
        raise ValueError("Empty entries in response.")

def get_tallest(all_supers: list[dict], gender: str, has_job: bool) -> dict:
    tallest = None
    top_height = 0
    for supe in all_supers:

        job = supe['work']['occupation']
        if job == '-':
            job = False
        else:
            job = True

        gender_curr = supe['appearance']['gender']

        if job == has_job and gender == gender_curr:
            height_str = supe['appearance']['height'][1]
            height, units = height_str.split()
            height = float(height)

            if units == 'meters':
                height *= 100

            if height > top_height:
                tallest = supe
                top_height = height

    if tallest is None:
        return dict()
    return tallest