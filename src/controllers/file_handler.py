import pandas as pd
import os

class FileHandler:
    @staticmethod
    def reader(csv_file):
        module_dir = os.path.dirname(__file__)

        data_frame = pd.read_csv((os.path.join(
        module_dir, '..', 'dataset', csv_file)))

        return data_frame.to_dict(orient='records')
