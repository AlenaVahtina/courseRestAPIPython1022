class TestExample:
    def test_size(self):
        expected_result = 15
        phrase = input("Set a phrase: ")
        assert len(phrase) == expected_result, f"expected size of phrase is {expected_result}"
