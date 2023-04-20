from collections import defaultdict
from .file_handler import FileHandler


def legislators_votes():
    legislators = FileHandler.reader('legislators.csv')
    vote_results = FileHandler.reader('vote_results.csv')

    legislator_dict = {legislator['id']: legislator['name'] for legislator in
                       legislators}

    results = defaultdict(
        lambda: {'num_supported_bills': 0, 'num_opposed_bills': 0, 'name': ''})

    for vote_result in vote_results:
        legislator_id = vote_result['legislator_id']
        vote_type = vote_result['vote_type']

        legislator_name = legislator_dict.get(legislator_id, '')
        results[legislator_id]['name'] = legislator_name

        results[legislator_id][
            'num_supported_bills' if vote_type == 1 \
                else 'num_opposed_bills'] += 1

    FileHandler.writer(dict(results))