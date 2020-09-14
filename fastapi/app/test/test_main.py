from starlette.testclient import TestClient

from main import app
from routers import pb_pyscripts, pb_atv

client = TestClient(app)

def test_default_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "For Usage:/scripts/upload_file : To upload file, /execute_script/{filename}{function}{arguments} : Adhoc running of script, /atv/---POST([treats events JSON, rule YML]) : Parse yml to steps, iterate through steps with treats events and output status"

def test_scripts_catalog():
    response = client.get("/scripts")
    assert response.status_code == 200
    assert response.json() == "['/app/python_scripts/base.py']"

def test_scripts_base():
    response = client.get("/scripts/base.py")
    assert response.status_code == 200
    assert response.json() == "def unhex(hexfield):\n\treturn bytes.fromhex(hexfield).decode('utf-8')\n\n\nimport re\ndef regmatch(decryptfield, matchstring):\n\tp = re.compile(matchstring)\n\tif p.findall(decryptfield):\n\t\tstatus = \"validated\"\n\telse:\n\t\tstatus = \"not validated\"\n\treturn status\n\n\ndef sum(a,b):\n\treturn str(a+b)\n"

def test_scripts_unknown():
    response = client.get("/scripts/unknown.py")
    assert response.status_code == 200
    assert response.json() == "Script not found"

def test_execute_function():
    response = client.post("/atv/execute_func", json={"mod":"base","func":"unhex","func_input":["6461626469626972623233347273657373696f6e"]})
    assert response.status_code == 200
    assert response.json() == "dabdibirb234rsession"
    
def test_execute_function_not_found():
    response = client.post("/atv/execute_func", json={"mod":"nosuchmod","func":"unhex","func_input":["6461626469626972623233347273657373696f6e"]})
    assert response.status_code == 200
    assert response.json() == "Module/Function not available to execute"

def test_execute_function_error():
    response = client.post("/atv/execute_func", json={"mod":"base","func":"unhex","func_input":["!@#@!!$!]"]})
    assert response.status_code == 200
    assert response.json() == "Error while executing function"

def test_execute_function_multiple_args():
    response = client.post("/atv/execute_func", json={"mod":"base","func":"sum","func_input":(1,3)})
    assert response.status_code == 200
    assert response.json() == "4"

def test_execute_function_multiple_args_error():
    response = client.post("/atv/execute_func", json={"mod":"base","func":"sum","func_input":(1,"3")})
    assert response.status_code == 200
    assert response.json() == "Error while executing function"

def test_atv_steps():
    treat_event = '{"uuid": "22FDSF43", "sig": {"id": "12345678"}, "hexfield": "6461626469626972623233347273657373696f6e"}'
    atv_rule = [{"function":"unhex","input":["hexfield"],"output":["decryptfield"]},{"function":"regmatch","input":["decryptfield","session"],"output":["status"]}]
    response = client.post("/atv/execute_steps", json={"event":treat_event, "steps":atv_rule})
    assert response.status_code == 200
    assert response.json() == '{"uuid": "22FDSF43", "status": "validated"}'

def test_atv_missing_event():
    treat_event = None
    atv_rule = [{"function":"base.unhex","input":["hexfield"],"output":["decryptfield"]},{"function":"base.regmatch","input":["decryptfield",".*session"],"output":["valid_treat"]}]
    response = client.post("/atv/execute_steps", json={"event":treat_event, "steps":atv_rule})
    assert response.status_code == 422

def test_atv_missing_rule():
    treat_event = '{"uuid": "22FDSF43", "sig": {"id": "12345678"}, "hexfield": "6461626469626972623233347273657373696f6e", "easy": "dabdibirb234rsession" }'
    atv_rule = None
    response = client.post("/atv/execute_steps", json={"event":treat_event, "steps":atv_rule})
    assert response.status_code == 422

def test_atv_append_keyvalue():
    treat_event = {"uuid": "22FDSF43", "sig": {"id": "12345678"}, "hexfield": "6461626469626972623233347273657373696f6e", "easy": "dabdibirb234rsession" }
    output_field = "decryptfield"
    atv_steps_response = "dabdibirb234rsession"
    assert pb_atv.atv_append_keyvalue(treat_event,output_field,atv_steps_response) == {'uuid': '22FDSF43', 'sig': {'id': '12345678'}, 'hexfield': '6461626469626972623233347273657373696f6e', 'easy': 'dabdibirb234rsession', 'decryptfield': 'dabdibirb234rsession'}

def test_atv_return_response():
    treat_event = '{"uuid": "22FDSF43", "sig": {"id": "12345678"}, "hexfield": "6461626469626972623233347273657373696f6e", "easy": "dabdibirb234rsession", "status": "validated"}'
    assert pb_atv.atv_return_response (treat_event) == '{"uuid": "22FDSF43", "status": "validated"}'
