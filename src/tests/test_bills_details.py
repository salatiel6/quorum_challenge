import os
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


@fixture
def mock_writer_args(mock_file_handler, bills_data, vote_results_data,
                       votes_data, legislators_data):
    mock_reader, mock_writer = mock_file_handler

    mock_reader.side_effect = [
        bills_data, vote_results_data, votes_data, legislators_data
    ]

    bills_details()

    writer_args, _ = mock_writer.call_args
    yield writer_args


def test_bills_details(mock_writer_args):
    expected_results = {
        '1': {'title': 'Bill 1', 'supporter_count': 2, 'opposer_count': 1,
              'primary_sponsor': 'Legislator 1'},
        '2': {'title': 'Bill 2', 'supporter_count': 2, 'opposer_count': 1,
              'primary_sponsor': 'Legislator 2'},
        '3': {'title': 'Bill 3', 'supporter_count': 1, 'opposer_count': 2,
              'primary_sponsor': 'Legislator 3'}}

    assert json.dumps(mock_writer_args[0], sort_keys=True) == json.dumps(
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


def test_1(mock_writer_args):
    # Test that the function writes a file with the correct fields
    module_dir = os.path.dirname(__file__)
    deliverables_dir = os.path.join(module_dir, '..', 'deliverables')
    with open(os.path.join(deliverables_dir, 'bills.csv')) as f:
        fields = set(f.readline().strip().split(','))

    expected_result = {'title', 'supporter_count', 'opposer_count',
                      'primary_sponsor', 'id'}
    assert sorted(fields) == sorted(expected_result)

def test_2():
    # Test that the function writes the correct number of rows to the file
    rows = []
    with open('bills.csv') as f:
        rows = f.readlines()[1:]
    assert len(rows) == 3  # or whatever the expected number of rows is

# def test_3():
#     # Test that the function calculates the supporter and opposer counts correctly
#     expected_counts = {'bill1': {'supporter_count': 2, 'opposer_count': 1},
#                        'bill2': {'supporter_count': 1, 'opposer_count': 2},
#                        'bill3': {'supporter_count': 0, 'opposer_count': 3}}
#     with open('bills.csv') as f:
#         f.readline()
#         for row in f:
#             row_values = row.strip().split(',')
#             bill_id = row_values[0]
#             supporter_count = int(row_values[1])
#             opposer_count = int(row_values[2])
#             assert supporter_count == expected_counts[bill_id][
#                 'supporter_count']
#             assert opposer_count == expected_counts[bill_id]['opposer_count']
#
# def test_4():
#     # Test that the function handles unknown primary sponsors correctly
#     expected_sponsors = {'bill1': 'Legislator A', 'bill2': 'Unknown',
#                          'bill3': 'Legislator C'}
#     with open('bills.csv') as f:
#         f.readline()
#         for row in f:
#             row_values = row.strip().split(',')
#             bill_id = row_values[0]
#             primary_sponsor = row_values[3]
#             assert primary_sponsor == expected_sponsors[bill_id]
#
#
# def test_bills_details_no_bills(mocker):
#     # Setup
#     mocker.patch.object(FileHandler, 'reader', side_effect=[[], [], [], []])
#     mocker.patch.object(FileHandler, 'writer')
#
#     # Test
#     bills_details()
#
#     # Assertions
#     FileHandler.reader.assert_called_with('legislators.csv')
#     FileHandler.writer.assert_called_once_with(defaultdict(
#         lambda: {
#             'title': " ",
#             'supporter_count': 0,
#             'opposer_count': 0,
#             'primary_sponsor': " "
#         }), ['title', 'supporter_count', 'opposer_count', 'primary_sponsor'],
#         'bills.csv')
#
#
# def test_bills_details_no_votes(mocker, bills_data, legislators_data):
#     # Setup
#     mocker.patch.object(FileHandler, 'reader',
#                         side_effect=[bills_data, [], [], legislators_data])
#     mocker.patch.object(FileHandler, 'writer')
#
#     # Expected results
#     expected_results = defaultdict(
#         lambda: {
#             'title': " ",
#             'supporter_count': 0,
#             'opposer_count': 0,
#             'primary_sponsor': " "
#         })
#     expected_results['1']['title'] = 'Bill 1'
#     expected_results['1']['primary_sponsor'] = 'Legislator 1'
#     expected_results['2']['title'] = 'Bill 2'
#     expected_results['2']['primary_sponsor'] = 'Legislator 2'
#     expected_results['3']['title'] = 'Bill 3'
#     expected_results['3']['primary_sponsor'] = 'Legislator 3
#
#     # Test
#     bills_details()
#
#     # Assertions
#     FileHandler.reader.assert_called_with('votes.csv')
#     FileHandler.writer.assert_called_once_with(expected_results,
#                                                ['title', 'supporter_count',
#                                                 'opposer_count',
#                                                 'primary_sponsor'],
#                                                'bills.csv')
