from unittest.mock import patch

import pytest

from ..controllers import legislators_votes


# Define fixture to mock file reader and writer functions
@pytest.fixture
def mock_file_handler():
    # Use patch to replace FileHandler.reader and FileHandler.writer
    # with mock functions
    with patch(
            'src.controllers.bills_details.FileHandler.reader'
    ) as mock_reader, \
            patch(
                'src.controllers.bills_details.FileHandler.writer'
            ) as mock_writer:

        # Yield both mock functions as a tuple
        yield mock_reader, mock_writer


def test_legislators_votes(mock_file_handler):
    # Setup mock file handler and reader
    mock_reader, mock_writer = mock_file_handler
    # Set the reader's side effect to return legislators
    # data and vote results data
    mock_reader.side_effect = [
        [
            {'id': '1', 'name': 'John'},
            {'id': '2', 'name': 'Jane'}
        ],
        [
            {'legislator_id': '1', 'vote_type': 1},
            {'legislator_id': '1', 'vote_type': 2},
            {'legislator_id': '2', 'vote_type': 1}
        ],
    ]

    # Test
    legislators_votes()

    # Assertions
    # Assert that the mock writer was called once
    assert mock_writer.call_count == 1

    # Get the arguments passed to the mock writer
    writer_args, _ = mock_writer.call_args
    # Assert that the expected data was written to the file
    assert writer_args[0] == {
        '1': {
            'name': 'John', 'num_opposed_bills': 1, 'num_supported_bills': 1},
        '2': {
            'name': 'Jane', 'num_opposed_bills': 0, 'num_supported_bills': 1}}
    # Assert that the expected header was written to the file
    assert writer_args[1] == [
        'name', 'num_supported_bills', 'num_opposed_bills']


def test_legislators_votes_missing_legislator(mock_file_handler):
    # Set up mock file handler and reader
    mock_reader, mock_writer = mock_file_handler
    # Setup side effects for the reader to return
    # data with a missing legislator
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}],
        [{'legislator_id': '2', 'vote_type': 1}],
    ]

    # Test
    legislators_votes()

    # Assertions
    writer_args, _ = mock_writer.call_args
    assert writer_args[0] == {
        '2': {'name': '', 'num_opposed_bills': 0, 'num_supported_bills': 1}}
    # The missing legislator should have been added to the output with
    # default values for their name and vote counts


def test_legislators_votes_output_headers(mock_file_handler):
    # Set up mock file handler and reader
    mock_reader, mock_writer = mock_file_handler
    # Set the reader's side effect to return the expected data
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}],
        [{'legislator_id': '1', 'vote_type': '1'}],
    ]

    # Test
    legislators_votes()

    # Assertions
    # Ensure that the function call wrote to the writer once
    assert mock_writer.call_count == 1
    # Get the arguments passed to the writer on the first call
    writer_args, _ = mock_writer.call_args
    # Ensure that the expected output headers are present
    # in the writer arguments
    assert writer_args[1] == [
        'name', 'num_supported_bills', 'num_opposed_bills']


def test_legislators_votes_output_rows(mock_file_handler):
    # Setup mock file handler and reader
    mock_reader, mock_writer = mock_file_handler
    # Set the reader's side effect to return mock
    # data for legislators and votes
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}, {'id': '2', 'name': 'Jane'}],
        [{'legislator_id': '1', 'vote_type': 1},
         {'legislator_id': '1', 'vote_type': 2},
         {'legislator_id': '2', 'vote_type': 1}],
    ]

    # Test
    legislators_votes()

    # Assertions
    # Check that the writer was called once
    assert mock_writer.call_count == 1

    # Check the contents of the writer's arguments
    writer_args, _ = mock_writer.call_args

    # Check that there are two rows in the writer arguments
    assert len(writer_args[0]) == 2

    # Check the row for John
    john_row = writer_args[0]['1']
    assert john_row['name'] == 'John'
    assert john_row['num_supported_bills'] == 1
    assert john_row['num_opposed_bills'] == 1

    # Check the row for Jane
    jane_row = writer_args[0]['2']
    assert jane_row['name'] == 'Jane'
    assert jane_row['num_supported_bills'] == 1
    assert jane_row['num_opposed_bills'] == 0
