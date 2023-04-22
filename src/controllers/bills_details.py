from collections import defaultdict
from .file_handler import FileHandler


def bills_details():
    # Read files using the FileHandler.reader() method
    bills = FileHandler.reader('bills.csv')
    vote_results = FileHandler.reader('vote_results.csv')
    votes = FileHandler.reader('votes.csv')
    legislators = FileHandler.reader('legislators.csv')

    # create a dictionary of legislator names, keyed by their ID
    legislator_names = {
        legislator['id']: legislator['name'] for legislator in legislators}

    # Create a defaultdict with default values for the result items
    results = defaultdict(
        lambda: {
            'title': " ",
            'supporter_count': 0,
            'opposer_count': 0,
            'primary_sponsor': " "
        })

    # iterate over the bills
    for bill in bills:
        bill_id = bill['id']
        results[bill_id]['title'] = bill['title']
        sponsor_id = bill['sponsor_id']

        # set the name of the primary sponsor of the current bill
        # in the results dictionary
        results[bill_id]['primary_sponsor'] = legislator_names.get(
            sponsor_id, "Unknown")

        # iterate over the votes
        for vote in votes:
            if bill_id == vote['bill_id']:
                vote_id = vote['id']

                # iterate over the vote results
                for vote_result in vote_results:
                    if vote_id == vote_result['vote_id']:
                        # get the type of the vote (1=support, 2=oppose)
                        vote_type = vote_result['vote_type']
                        # increment the supporter or opposer count of the
                        # current bill in the results dictionary
                        results[bill_id][
                            'supporter_count' if vote_type == 1
                            else 'opposer_count'] += 1

    # Define the fields to write to the CSV file, the filename,
    # and call the FileHandler.writer() method
    csv_fields = [
        'title', 'supporter_count', 'opposer_count', 'primary_sponsor']
    filename = "bills.csv"
    FileHandler.writer(dict(results), csv_fields, filename)
