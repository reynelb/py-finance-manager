import os
import json
import pytest
from app.storage import Storage

TEST_FILE = "test_data.json"

def setup_function():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def teardown_function():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

def test_save_and_load():
    data = {"transactions": [{"amount": 100, "type": "income"}]}
    Storage.FILE_PATH = TEST_FILE
    Storage.save(data)
    loaded = Storage.load()
    assert loaded == data
