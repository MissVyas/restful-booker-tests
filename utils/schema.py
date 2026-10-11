import json
from pathlib import Path
from jsonschema import validate
from genson import SchemaBuilder

SCHEMA_DIR = Path(__file__).parent.parent / "schemas"

def assert_matches_schema(data, schema_name: str):
    schema = json.loads((SCHEMA_DIR / f"{schema_name}.json").read_text())
    validate(instance=data, schema=schema)

def generate_schema(data, schema_name: str, overwrite: bool = False):
    path = SCHEMA_DIR / f"{schema_name}.json"
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; pass overwrite=True to replace it")

    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()

    SCHEMA_DIR.mkdir(exist_ok=True)
    path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    return path