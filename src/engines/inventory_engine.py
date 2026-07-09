import pandas as pd


class InventoryEngine:
    """
    Creates the planning table by combining
    January Forecast and Opening Inventory.
    """

    def __init__(self, forecast_df, inventory_df):

        # Make copies
        self.forecast = forecast_df.copy()
        self.inventory = inventory_df.copy()

        # Rename columns
        self.forecast.rename(
            columns={
                "Jan -2026 (in kL)": "Forecast"
            },
            inplace=True
        )

        self.inventory.rename(
            columns={
                "Jan -2026 (in kL)": "Opening Inventory"
            },
            inplace=True
        )

        self.planning_table = None

    # =====================================================
    # Create Planning Table
    # =====================================================

    def create_planning_table(self):

        self.planning_table = pd.merge(

            self.forecast,

            self.inventory,

            on=[
                "Product Name",
                "Pack size",
                "CFA region",
                "CFA"
            ],

            how="left"
        )

        # Calculate Net Requirement
        self.planning_table["Net Requirement"] = (

            self.planning_table["Forecast"]

            -

            self.planning_table["Opening Inventory"]

        ).clip(lower=0)

        return self.planning_table

    # =====================================================
    # Return Planning Table
    # =====================================================

    def get_planning_table(self):

        if self.planning_table is None:
            self.create_planning_table()

        return self.planning_table

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        table = self.get_planning_table()

        print("\n" + "=" * 70)
        print("INVENTORY PLANNING")
        print("=" * 70)

        print(f"Planning Records      : {len(table)}")
        print(f"Total Forecast        : {table['Forecast'].sum():,.2f} KL")
        print(f"Opening Inventory     : {table['Opening Inventory'].sum():,.2f} KL")
        print(f"Net Requirement       : {table['Net Requirement'].sum():,.2f} KL")

    # =====================================================
    # Shortage Report
    # =====================================================

    def shortage_report(self):

        table = self.get_planning_table()

        shortage = table[
            table["Net Requirement"] > 0
        ]

        return shortage

    # =====================================================
    # Surplus Report
    # =====================================================

    def surplus_report(self):

        table = self.get_planning_table()

        surplus = table[
            table["Net Requirement"] == 0
        ]

        return surplus

    # =====================================================
    # Export Planning Table
    # =====================================================

    def export_planning_table(self, file_path):

        table = self.get_planning_table()

        table.to_csv(file_path, index=False)

        print(f"\nPlanning table exported to: {file_path}")