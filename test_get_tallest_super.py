import pytest


import get_tallest_super

mock_data = [
    {
        'name': 'Batman',
        'appearance': {
            'gender': 'Male',
            'height': ["6'2", '187 cm']
        },
        'work': {'occupation': 'CEO of Wayne Industries'}
    },
    {
        'name': 'Spiderman',
        'appearance': {
            'gender': 'Male',
            'height': ["5'8", '173 cm']
        },
        'work': {'occupation': '-'}
    },
    {
        'name': 'Wonder Woman',
        'appearance': {
            'gender': 'Female',
            'height': ["6'2", "187 cm"]
        },
        'work': {'occupation': '-'}
    }
]

@pytest.fixture()
def patch_get_all_supers(monkeypatch):
    def mock_get_all_supers():
        return mock_data
    monkeypatch.setattr('get_tallest_super.get_all_supers', mock_get_all_supers)

#Позитивные тесты:
# Male True
def test_get_tallest_super_male_job(patch_get_all_supers):
    supe = get_tallest_super.get_tallest_super('Male', True)
    assert supe == 'Batman'

# Male False
def test_get_tallest_super_male_jobless(patch_get_all_supers):
    supe = get_tallest_super.get_tallest_super('Male', False)
    assert supe == 'Spiderman'

# Female False
def test_get_tallest_super_female_jobless(patch_get_all_supers):
    supe = get_tallest_super.get_tallest_super('Female', False)
    assert supe == 'Wonder Woman'

#Негативные
#отсутствуют данные по заданным параметрам
def test_get_tallest_super_female_job(patch_get_all_supers):
    with pytest.raises(ValueError):
        get_tallest_super.get_tallest_super('Female', True)

#неверный аргумент gender
def test_wrong_gender(patch_get_all_supers):
    with pytest.raises(ValueError):
        get_tallest_super.get_tallest_super('Dolly The Sheep', True)

# неверный аргумент has_job
def test_wrong_has_job_type(patch_get_all_supers):
    with pytest.raises(TypeError):
        get_tallest_super.get_tallest_super('Male', 'Yes')
        get_tallest_super.get_tallest_super('Female', "no")

#Тест реакций на Response
def bad_response(status_code, data):
    class MockResponse:
        def __init__(self, status_code, data):
            self.status_code = status_code
            self.data = data
        def json(self):
            return self.data

    return MockResponse(status_code, data)

#Код ответа не 200
def test_status_code(monkeypatch):
    def mock_get(url):
        return bad_response(404, mock_data)
    monkeypatch.setattr("get_tallest_super.requests.get", mock_get)
    with pytest.raises(ConnectionError):
        get_tallest_super.get_tallest_super('Male', True)

# Пустые записи в теле ответа
def test_empty_entries(monkeypatch):
    bad_data = [
    {
        'name': 'Batman',
        'appearance': {
            'gender': 'Male',
            'height': ["6'2", '187 cm']
        },
        'work': {'occupation': 'CEO of Wayne Industries'}
    },
    {}
    ]
    def mock_get(url):
        return bad_response(200, bad_data)
    monkeypatch.setattr("get_tallest_super.requests.get", mock_get)

    with pytest.raises(ValueError):
        get_tallest_super.get_tallest_super('Male', True)

#Неверный тип данных в теле
def test_wrong_response_type(monkeypatch):
    bad_mock_data = {'Hero': {'name': 'Batman'}}
    def mock_get(url):
        return bad_response(200, bad_mock_data)
    monkeypatch.setattr('get_tallest_super.requests.get', mock_get)
    with pytest.raises(TypeError):
        get_tallest_super.get_tallest_super('Male', True)

#Пустой список в ответе
def test_empty_response(monkeypatch):
    bad_mock_data = list()
    def mock_get(url):
        return bad_response(200, bad_mock_data)
    monkeypatch.setattr('get_tallest_super.requests.get', mock_get)
    with pytest.raises(ValueError):
        get_tallest_super.get_tallest_super('Male', True)

