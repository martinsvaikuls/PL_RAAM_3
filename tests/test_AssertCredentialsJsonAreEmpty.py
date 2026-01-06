import json
from pathlib import Path
import pytest

JSON_FILES = [
    Path("PL_RAAM_v2/credentials/client_cred.json"),
    Path("PL_RAAM_v2/credentials/google_id.json")
]

@pytest.mark.parametrize("file_path", JSON_FILES)
def test_AssertCredentialsJsonAreEmpty(file_path):
    assert file_path.exists, f"Fails {file_path} neeksistē!"
    with file_path.open("r", encoding = "utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Fails {file_path} nesatur derīgu JSON")
    assert data == {}, f"Fails {file_path} nav tukšs!"
