import pandas as pd


class FileHandler:
    @staticmethod
    def reader(csv_file):
        data_frame = pd.read_csv(csv_file)
        return data_frame.to_dict(orient='records')
