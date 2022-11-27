from requests import Response
import json

class Assertions:
    def assert_json_value_by_name(response: Response, name, expacted_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response is not JSON"
        assert name in response_as_dict, f"Response JSON doesen't have key {name}"
        assert response_as_dict[name] == expacted_value, error_message

