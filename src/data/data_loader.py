import pandas as pd
from pathlib import Path


class DataLoader:
    """
    Loads all sheets from the Excel workbook.
    No cleaning is performed here.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = {}

    def load_data(self):

        excel = pd.ExcelFile(self.file_path)

        for sheet in excel.sheet_names:

            print(f"Loading: {sheet}")

            # Read the sheet exactly as it exists in Excel
            self.data[sheet] = pd.read_excel(
                self.file_path,
                sheet_name=sheet,
                header=None
            )

        print("\n✅ Workbook Loaded Successfully!")

        return self.data