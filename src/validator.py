import pandas as pd


class DataValidator:

    def __init__(self, data):
        self.data = data

    def validate(self):

        print("\n" + "="*60)
        print("DATA VALIDATION REPORT")
        print("="*60)

        for sheet_name, df in self.data.items():

            print(f"\n📄 {sheet_name}")

            print(f"Rows    : {df.shape[0]}")
            print(f"Columns : {df.shape[1]}")

            missing = df.isnull().sum().sum()
            print(f"Missing Values : {missing}")

            duplicates = df.duplicated().sum()
            print(f"Duplicate Rows : {duplicates}")