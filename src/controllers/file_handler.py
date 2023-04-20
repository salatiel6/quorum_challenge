import pandas as pd
import os


class FileHandler:
    @staticmethod
    def reader(csv_file):
        module_dir = os.path.dirname(__file__)

        data_frame = pd.read_csv((os.path.join(
            module_dir, '..', 'dataset', csv_file)))

        return data_frame.to_dict(orient='records')

    @staticmethod
    def writer(base_dict, fields, filename):
        module_dir = os.path.dirname(__file__)

        deliverables_dir = os.path.join(module_dir, '..', 'deliverables')
        if not os.path.exists(deliverables_dir):
            os.makedirs(deliverables_dir)

        df = pd.DataFrame.from_dict(base_dict, orient='index')
        df = df[fields]
        df.index.name = 'id'
        df.to_csv((os.path.join(deliverables_dir, filename)))
