import pandas as pd
import os


class FileHandler:
    @staticmethod
    def reader(csv_file):
        # Get the directory path of this file
        module_dir = os.path.dirname(__file__)

        # Read the CSV file using Pandas and return its records as a dictionary
        # This follows the ADAPTER design pattern
        # Every data that comes from outside,
        # should be transformed into a dictionary
        data_frame = pd.read_csv((os.path.join(
            module_dir, '..', 'dataset', csv_file)))
        return data_frame.to_dict(orient='records')

    @staticmethod
    def writer(base_dict, fields, filename):
        # Get the directory path of this file
        module_dir = os.path.dirname(__file__)

        # Create a directory for output files if it doesn't exist
        deliverables_dir = os.path.join(module_dir, '..', 'deliverables')
        if not os.path.exists(deliverables_dir):
            os.makedirs(deliverables_dir)

        # Create a Pandas DataFrame from the input dictionary, select only
        # the specified fields,
        # set the index name to 'id', and write the DataFrame to a CSV file
        df = pd.DataFrame.from_dict(base_dict, orient='index')
        df = df[fields]
        df.index.name = 'id'
        df.to_csv((os.path.join(deliverables_dir, filename)))
