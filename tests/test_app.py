import pytest
import csv
from app import write_to_csv, fetch_users, get_api_data_keys, app

api_url = "https://tech-interview-api-ultramed.vercel.app/users"


@pytest.fixture
def test_client():
    # test client using Flask's test client
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test fetch_users function
def test_fetch_users(test_client):
    data = fetch_users(api_url)
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "email" in data[0]
    assert "status" in data[0]


# Test get_api_data_keys function
# Parametrize data structured as: data in API example, expected output, pytest identifier
@pytest.mark.parametrize(
    "data, expected_keys, test_label",
    [
        (
            [
                {"name": "Mia Bear", "email": "Mia@email.com", "status": "inactive"},
                {"name": "Jazzy Bear", "email": "jazzy@email.com", "status": "active"}
            ],
            ["name", "email", "status"],
            "Valid input: List of dictionaries"
        ),
        # Empty list
        ([], [], "Empty list"),
        # Invalid input: None
        (None, [], "Invalid input: None"),
        # Invalid input: String
        ("Random string input", [], "Invalid input: Dictionary"),
        # Invalid input: Dictionary
        ({"key": "value"}, [], "Invalid input: Dictionary, not list"),
        # List with an empty dictionary
        ([{}], [], "List with an empty dictionary"),
    ],
)
def test_get_api_data_keys(data, expected_keys, test_label):
    keys = get_api_data_keys(data)
    assert keys == expected_keys


def test_write_csv_success(tmp_path):
    # Temporary file for the test
    temp_file = tmp_path / "user_list.csv"

    # Call the function with the temp file path
    result = write_to_csv(file_name=str(temp_file))

    # Verify the result
    assert result == "Data successfully written to user_list.csv."
    assert temp_file.exists()  # Ensure the file was created

    # Verify file contents
    with open(temp_file, "r") as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Check header and data
    assert rows[0] == ["id","name", "email", "status"]  # Header row
    assert rows[1] == ['14', 'Aayat Phelps', 'aayat_phelps@ultramed.tech', 'active'] # First data row
    assert rows[-1] == ["22","Zander Fischer","zander_fischer@ultramed.tech","active"]  # last data row
