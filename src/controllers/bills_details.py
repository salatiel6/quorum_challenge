from collections import defaultdict
from .file_handler import FileHandler


def bills_details():
    bills = FileHandler.reader('bills.csv')
    vote_results = FileHandler.reader('vote_results.csv')
    votes = FileHandler.reader('votes.csv')
    legislators = FileHandler.reader('legislators.csv')

    legislator_names = {legislator['id']: legislator['name'] for legislator in
                        legislators}

    results = defaultdict(
        lambda: {
            'title': " ",
            'supporter_count': 0,
            'opposer_count': 0,
            'primary_sponsor': " "
        })

    for bill in bills:
        bill_id = bill['id']
        results[bill_id]['title'] = bill['title']
        sponsor_id = bill['sponsor_id']

        results[bill_id]['primary_sponsor'] = legislator_names.get(
            sponsor_id, "Unknown")

        for vote in votes:
            if bill_id == vote['bill_id']:
                vote_id = vote['id']

                for vote_result in vote_results:
                    if vote_id == vote_result['vote_id']:
                        vote_type = vote_result['vote_type']
                        results[bill_id][
                            'supporter_count' if vote_type == 1
                            else 'opposer_count'] += 1

    csv_fields = [
        'title', 'supporter_count', 'opposer_count', 'primary_sponsor']
    filename = "bills.csv"
    FileHandler.writer(dict(results), csv_fields, filename)
