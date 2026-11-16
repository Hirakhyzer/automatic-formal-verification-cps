"""CLI regression tests for explicit verifier configuration and evidence export."""
import json

import pytest

from cpsverify.cli import main


def test_cli_selects_property_index_and_generator_cap(capsys):
    main(["battery", "--method", "zonotope", "--property-index", "0",
          "--max-generators", "2", "--steps", "2", "--json"])
    result = json.loads(capsys.readouterr().out)
    assert result["method"] == "zonotope"
    assert result["steps"] == 2


def test_cli_creates_nested_evidence_directory(tmp_path):
    path = tmp_path / "nested" / "evidence.json"
    main(["battery", "--steps", "1", "--evidence-manifest", str(path)])
    assert path.exists()
    assert isinstance(json.loads(path.read_text()), dict)


@pytest.mark.parametrize("option,value", [
    ("--property-index", "-1"),
    ("--max-generators", "0"),
    ("--steps", "0"),
    ("--attack-scale", "nan"),
])
def test_cli_rejects_invalid_request_with_usage_error(option, value):
    with pytest.raises(SystemExit) as exc:
        main(["battery", option, value])
    assert exc.value.code == 2
