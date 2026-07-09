import pandas as pd


class SupplyChainData:

    def __init__(self, raw_data):

        self.raw_data = raw_data

        # Business DataFrames
        self.plants = None
        self.plant_hub = None
        self.hub_cfa = None
        self.products = None
        self.source_lt = None
        self.service = None
        self.sales = None
        self.forecast = None
        self.inventory = None
        self.jan_forecast = None

    def clean_sheet(
        self,
        df,
        header_row,
        data_start_row,
        remove_footer=True
    ):
        """
        Generic function to clean one Excel sheet.
        """

        # Make a copy
        df = df.copy()

        # Set column names
        df.columns = df.iloc[header_row]

        # Keep only data
        df = df.iloc[data_start_row:]

        # Remove blank rows
        df = df.dropna(how="all")

        # Remove footer rows (if any)
        if remove_footer:

            first_col = df.columns[0]

            df = df[
                ~df[first_col]
                .astype(str)
                .str.contains(
                    "All|Any|Forecast",
                    case=False,
                    na=False
                )
            ]

        # Reset index
        df = df.reset_index(drop=True)

        # Remove the column index name
        df.columns.name = None

        return df

    def clean(self):

        # Plants
        self.plants = self.clean_sheet(
            self.raw_data["A - Plants & Production"],
            2, 3
        )

        # Plant -> Hub
        self.plant_hub = self.clean_sheet(
            self.raw_data["B - Plant-Hub Transport"],
            2, 3
        )

        # Hub -> CFA
        self.hub_cfa = self.clean_sheet(
            self.raw_data["C -Hub-CFA Transport"],
            2, 3
        )

        # Product Master
        self.products = self.clean_sheet(
            self.raw_data["D -SKU Portfolio+Penalty matrix"],
            2, 3,
            remove_footer=False
        )

        # Source + Lead Time
        self.source_lt = self.clean_sheet(
            self.raw_data["E - Source + LT data"],
            2, 3,
            remove_footer=False
        )

        # Service Levels
        self.service = self.clean_sheet(
            self.raw_data["F - Service Levels"],
            2, 3
        )

        # Sales History
        self.sales = self.clean_sheet(
            self.raw_data["G - Sales History"],
            2, 3,
            remove_footer=False
        )

        # Forecast History
        self.forecast = self.clean_sheet(
            self.raw_data["H - Forecast History"],
            3, 4,
            remove_footer=False
        )

        # Opening Inventory
        self.inventory = self.clean_sheet(
            self.raw_data["I - Expected opening Inventory"],
            3, 4,
            remove_footer=False
        )

        # January Forecast
        self.jan_forecast = self.clean_sheet(
            self.raw_data["J - Jan Forecast"],
            3, 4,
            remove_footer=False
        )

        return self