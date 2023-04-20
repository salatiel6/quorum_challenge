from collections import defaultdict
from .file_handler import FileHandler


def get_legislator_name(legislators, sponsor_id):
    legislator = next((legislator for legislator in legislators
                       if legislator['id'] == sponsor_id), None)
    return legislator['name'] if legislator else "Unknown"


def get_vote_type(vote_results, vote_id):
    vote_result = next((vr for vr in vote_results
                        if vr['vote_id'] == vote_id), None)
    return vote_result['vote_type'] if vote_result else None


def count_votes(votes, vote_results):
    vote_counts = defaultdict(
        lambda: {'supporter_count': 0, 'opposer_count': 0})

    for vote in votes:
        vote_id = vote['id']
        vote_type = get_vote_type(vote_results, vote_id)

        if vote_type is not None:
            bill_id = vote['bill_id']
            vote_counts[bill_id][
                'supporter_count' if vote_type == 1 else 'opposer_count'] += 1

    return vote_counts


def bills_details():
    bills = FileHandler.reader('bills.csv')
    vote_results = FileHandler.reader('vote_results.csv')
    votes = FileHandler.reader('votes.csv')
    legislators = FileHandler.reader('legislators.csv')

    results = defaultdict(lambda: {
        'title': " ",
        'supporter_count': 0,
        'opposer_count': 0,
        'primary_sponsor': " "
    })

    legislator_names = {legislator['id']: legislator['name']
                        for legislator in legislators}

    for bill in bills:
        bill_id = bill['id']
        results[bill_id]['title'] = bill['title']
        results[bill_id]['primary_sponsor'] = legislator_names.get(
            bill['sponsor_id'], "Unknown")

    vote_counts = count_votes(votes, vote_results)

    for bill_id, vote_count in vote_counts.items():
        results[bill_id]['supporter_count'] = vote_count['supporter_count']
        results[bill_id]['opposer_count'] = vote_count['opposer_count']

    csv_fields = [
        'title', 'supporter_count', 'opposer_count', 'primary_sponsor']
    filename = "bills.csv"
    FileHandler.writer(dict(results), csv_fields, filename)
