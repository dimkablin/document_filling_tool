"""File for working with data"""

import os
import pandas as pd


class Data:
    """Class for working with data"""
    def __init__(self):
        pass

    @staticmethod
    def create_excel_from_json(json_data):
        """Create excel from json data"""
        df_list = []
        for idx, inner_list in enumerate(json_data, start=1):
            data = []
            for entry in inner_list:
                row = {}
                for key, value in entry.items():
                    content = value.get('content', '')
                    row[key] = content
                data.append(row)
            df = pd.DataFrame(data)
            df_list.append(df)

        path = "./data/"
        path = os.path.join(path, 'output.xlsx')

        with pd.ExcelWriter(path) as writer:
            for idx, df in enumerate(df_list, start=1):
                df.to_excel(writer, sheet_name=f'Лист{idx}', index=False)

        # Return the file path and temporary directory
        return path
