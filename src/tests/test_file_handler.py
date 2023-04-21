import os
import pytest
import pandas as pd
from unittest import mock
from ..controllers import FileHandler


@pytest.fixture
def mock_csv_file(tmpdir):
    csv_file = tmpdir.join('test_file.csv')
    csv_file.write('id,name\n1,John\n2,Jane\n')
    return csv_file


def test_reader(mock_csv_file):
    expected = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
    actual = FileHandler.reader(mock_csv_file)
    assert actual == expected


def test_writer(mock_csv_file):
    base_dict = {'1': {'name': 'John'}, '2': {'name': 'Jane'}}
    fields = ['name']
    filename = 'test_output.csv'

    with mock.patch('pandas.DataFrame.to_csv') as mock_to_csv:
        FileHandler.writer(base_dict, fields, mock_csv_file)

        # Check that to_csv was called with the expected arguments
        expected_df = pd.DataFrame.from_dict(base_dict, orient='index')
        expected_df = expected_df[fields]
        expected_df.index.name = 'id'

        dir_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir))
        file1_path = os.path.join(dir_path, "controllers")
        expected_path = os.path.join(
            file1_path, '..', 'deliverables', mock_csv_file)


        mock_to_csv.assert_called_once_with(expected_path)

        file_path = mock_to_csv.call_args[0][0]
        df = pd.read_csv(file_path)
        df = df.to_dict(orient='records')
        expected = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Jane'}]
        assert df == expected


