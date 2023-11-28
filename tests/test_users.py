import json
import requests

def test_index():
    ## Testing the index of users api
    res = requests.get('http://localhost:8080/')
    assert res.status_code == 200
    expected = {'status': 200}
    assert expected == json.loads(res._content)

