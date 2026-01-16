from pathlib import Path

import pytest


@pytest.fixture
def test_data_path():
    current_file = Path(__file__).resolve()
    parent_dir = current_file.parent
    
    return parent_dir / "test_data"
