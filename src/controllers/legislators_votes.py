from collections import defaultdict
from .file_handler import FileHandler


def legislators_votes():
    # Read files using the FileHandler.reader() method
    legislators = FileHandler.reader('legislators.csv')
    vote_results = FileHandler.reader('vote_results.csv')

    # Create a dictionary of legislators with their ID as the key and name
    # as the value
    legislator_dict = {
        legislator['id']: legislator['name'] for legislator in legislators}

    # Create a defaultdict with default values for the result items
    results = defaultdict(
        lambda: {'num_supported_bills': 0, 'num_opposed_bills': 0, 'name': ''})

    # Iterate over the vote results and update the results
    # dictionary accordingly
    for vote_result in vote_results:
        legislator_id = vote_result['legislator_id']
        vote_type = vote_result['vote_type']

        # Get the name of the legislator from the legislator_dict
        legislator_name = legislator_dict.get(legislator_id, '')
        # Update the name of the legislator in the results dictionary
        results[legislator_id]['name'] = legislator_name

        # Increment the number of supported or opposed bills for the
        # legislator in the results dictionary
        results[legislator_id][
            'num_supported_bills' if vote_type == 1
            else 'num_opposed_bills'] += 1

    # Define the fields to write to the CSV file, the filename,
    # and call the FileHandler.writer() method
    csv_fields = ['name', 'num_supported_bills', 'num_opposed_bills']
    filename = "legislators-support-oppose-count.csv"
    FileHandler.writer(dict(results), csv_fields, filename)
