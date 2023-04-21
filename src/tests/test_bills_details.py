import json

from unittest.mock import patch
from pytest import fixture
from collections import defaultdict

from ..controllers import bills_details


@fixture
def bills_data():
    return [
        {'id': '1', 'title': 'Bill 1', 'sponsor_id': '1'},
        {'id': '2', 'title': 'Bill 2', 'sponsor_id': '2'},
        {'id': '3', 'title': 'Bill 3', 'sponsor_id': '3'}
    ]


@fixture
def vote_results_data():
    return [
        {'id': '1', 'legislator_id': '1', 'vote_id': '1', 'vote_type': 1},
        {'id': '2', 'legislator_id': '1', 'vote_id': '2', 'vote_type': 1},
        {'id': '3', 'legislator_id': '1', 'vote_id': '3', 'vote_type': 2},
        {'id': '4', 'legislator_id': '2', 'vote_id': '1', 'vote_type': 2},
        {'id': '5', 'legislator_id': '2', 'vote_id': '2', 'vote_type': 2},
        {'id': '6', 'legislator_id': '2', 'vote_id': '3', 'vote_type': 1},
        {'id': '7', 'legislator_id': '3', 'vote_id': '1', 'vote_type': 1},
        {'id': '8', 'legislator_id': '3', 'vote_id': '2', 'vote_type': 1},
        {'id': '9', 'legislator_id': '3', 'vote_id': '3', 'vote_type': 2}
    ]


@fixture
def votes_data():
    return [
        {'id': '1', 'bill_id': '1'},
        {'id': '2', 'bill_id': '2'},
        {'id': '3', 'bill_id': '3'}
    ]


@fixture
def legislators_data():
    return [
        {'id': '1', 'name': 'Legislator 1'},
        {'id': '2', 'name': 'Legislator 2'},
        {'id': '3', 'name': 'Legislator 3'}
    ]


@fixture
def mock_file_handler():
    with patch(
            'src.controllers.bills_details.FileHandler.reader'
    ) as mock_reader, \
            patch(
                'src.controllers.bills_details.FileHandler.writer'
            ) as mock_writer:
        yield mock_reader, mock_writer


def test_bills_details(mock_file_handler, bills_data, vote_results_data,
                       votes_data, legislators_data):
    mock_reader, mock_writer = mock_file_handler

    mock_reader.side_effect = [
        bills_data, vote_results_data, votes_data, legislators_data
    ]

    bills_details()

    writer_args, _ = mock_writer.call_args

    expected_results = {
        '1': {'title': 'Bill 1', 'supporter_count': 2, 'opposer_count': 1,
              'primary_sponsor': 'Legislator 1'},
        '2': {'title': 'Bill 2', 'supporter_count': 2, 'opposer_count': 1,
              'primary_sponsor': 'Legislator 2'},
        '3': {'title': 'Bill 3', 'supporter_count': 1, 'opposer_count': 2,
              'primary_sponsor': 'Legislator 3'}}

    assert json.dumps(writer_args[0], sort_keys=True) == json.dumps(
        expected_results, sort_keys=True)


def test_bills_details_no_bills(mock_file_handler):
    mock_reader, mock_writer = mock_file_handler
    mock_reader.side_effect = [[], [], [], []]

    # Test
    bills_details()

    # Assertions
    mock_reader.assert_called_with('legislators.csv')
    mock_writer.assert_called_once_with(defaultdict(
        lambda: {
            'title': " ",
            'supporter_count': 0,
            'opposer_count': 0,
            'primary_sponsor': " "
        }), ['title', 'supporter_count', 'opposer_count', 'primary_sponsor'],
        'bills.csv')


def test_bills_details_no_votes(mock_file_handler,
                                bills_data, legislators_data):
    mock_reader, mock_writer = mock_file_handler
    mock_reader.side_effect = [bills_data, [], [], legislators_data]

    # Expected results
    expected_results = defaultdict(
        lambda: {
            'title': " ",
            'supporter_count': 0,
            'opposer_count': 0,
            'primary_sponsor': " "
        })
    expected_results['1']['title'] = 'Bill 1'
    expected_results['1']['primary_sponsor'] = 'Legislator 1'
    expected_results['2']['title'] = 'Bill 2'
    expected_results['2']['primary_sponsor'] = 'Legislator 2'
    expected_results['3']['title'] = 'Bill 3'
    expected_results['3']['primary_sponsor'] = 'Legislator 3'

    # Test
    bills_details()

    # Assertions
    mock_reader.assert_called_with('legislators.csv')
    mock_writer.assert_called_once_with(
        expected_results, ['title', 'supporter_count', 'opposer_count',
                           'primary_sponsor'], 'bills.csv')
