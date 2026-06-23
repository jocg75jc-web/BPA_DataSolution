from core.parameter_validator import ParameterValidator


def test_parameter_validator_required_and_defaults():
    definition = {
        "query": {"type": "select", "required": True, "default": "all", "options": {"all": {}, "q1": {}}},
        "database": {"type": "text", "required": False, "default": None},
    }

    validator = ParameterValidator(definition)
    ok, errors, cleaned = validator.validate({})

    assert ok
    assert errors == []
    assert cleaned["query"] == "all"


def test_parameter_validator_rejects_unknown_parameter():
    definition = {
        "model": {"type": "select", "required": True, "default": "all", "options": {"all": {}, "modelo3": {}}}
    }
    validator = ParameterValidator(definition)

    ok, errors, _ = validator.validate({"other": "x"})

    assert not ok
    assert any("Unknown parameter" in e for e in errors)
