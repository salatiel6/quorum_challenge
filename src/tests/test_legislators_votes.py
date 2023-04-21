from collections import defaultdict
from unittest.mock import patch

import pytest

from ..controllers import legislators_votes


@pytest.fixture
def mock_file_handler():
    with patch('src.controllers.legislators_votes.FileHandler.reader') as mock_reader, \
         patch('src.controllers.legislators_votes.FileHandler.writer') as mock_writer:
        yield mock_reader, mock_writer


def test_legislators_votes(mock_file_handler):
    mock_reader, mock_writer = mock_file_handler
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

    legislators_votes()

    assert mock_writer.call_count == 1

    writer_args, _ = mock_writer.call_args
    assert len(writer_args) == 3
    assert writer_args[0] == {'1': {'name': 'John', 'num_opposed_bills': 1, 'num_supported_bills': 1},
                              '2': {'name': 'Jane', 'num_opposed_bills': 0, 'num_supported_bills': 1}}
    assert writer_args[1] == ['name', 'num_supported_bills', 'num_opposed_bills']


def test_legislators_votes_missing_legislator(mock_file_handler):
    mock_reader, mock_writer = mock_file_handler
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}],
        [{'legislator_id': '2', 'vote_type': 1}],
    ]

    legislators_votes()

    writer_args, _ = mock_writer.call_args
    assert writer_args[0] == {'2': {'name': '', 'num_opposed_bills': 0, 'num_supported_bills': 1}}


def test_legislators_votes_output_headers(mock_file_handler):
    mock_reader, mock_writer = mock_file_handler
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}],
        [{'legislator_id': '1', 'vote_type': '1'}],
    ]

    legislators_votes()

    writer_args, _ = mock_writer.call_args
    assert writer_args[1] == ['name', 'num_supported_bills', 'num_opposed_bills']


def test_legislators_votes_output_rows(mock_file_handler):
    mock_reader, mock_writer = mock_file_handler
    mock_reader.side_effect = [
        [{'id': '1', 'name': 'John'}, {'id': '2', 'name': 'Jane'}],
        [{'legislator_id': '1', 'vote_type': 1},
         {'legislator_id': '1', 'vote_type': 2},
         {'legislator_id': '2', 'vote_type': 1}],
    ]

    legislators_votes()

    writer_args, _ = mock_writer.call_args
    assert len(writer_args[0]) == 2

    john_row = writer_args[0]['1']
    assert john_row['name'] == 'John'
    assert john_row['num_supported_bills'] == 1
    assert john_row['num_opposed_bills'] == 1

    jane_row = writer_args[0]['2']
    assert jane_row['name'] == 'Jane'
    assert jane_row['num_supported_bills'] == 1
    assert jane_row['num_opposed_bills'] == 0
