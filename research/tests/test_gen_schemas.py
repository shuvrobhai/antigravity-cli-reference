"""Tests for the schema generator (issue #4 follow-up)."""

import json

import gen_schemas
from paths import knowledge_json, schemas_dir


def test_checked_in_schemas_match_generator_output():
    """The four checked-in schemas must equal the generator output, so the
    knowledge file stays the single source of truth for enum/default/type data."""
    data = json.loads(knowledge_json().read_text(encoding="utf-8"))
    for name, schema in gen_schemas.build_all(data).items():
        expected = gen_schemas.dump(schema)
        actual = (schemas_dir() / name).read_text(encoding="utf-8")
        assert actual == expected, (
            f"{name} is out of sync with the knowledge file; "
            "run `uv run python research/scripts/gen_schemas.py`"
        )
