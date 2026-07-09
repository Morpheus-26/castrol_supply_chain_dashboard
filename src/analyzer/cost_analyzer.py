import pandas as pd


class CostAnalyzer:

    def __init__(
        self,
        planning_table,
        plants_df,
        source_df,
        plant_hub_df,
        hub_cfa_df
    ):

        self.plan = planning_table.copy()
        self.plants = plants_df.copy()
        self.source = source_df.copy()
        self.plant_hub = plant_hub_df.copy()
        self.hub_cfa = hub_cfa_df.copy()

        self.cost_table = None

    # ======================================================
    # Build Cost Table
    # ======================================================

    def build_cost_table(self):

        # Add Source Plant
        source_cols = [
            "Product Name",
            "Pack size",
            "CFA region",
            "CFA",
            "Source"
        ]

        self.plan = pd.merge(

            self.plan,

            self.source[source_cols],

            on=[
                "Product Name",
                "Pack size",
                "CFA region",
                "CFA"
            ],

            how="left"
        )

        # Add Production Cost
        self.plan = pd.merge(

            self.plan,

            self.plants[
                [
                    "Plant Code",
                    "Production Cost (₹/kl)"
                ]
            ],

            left_on="Source",
            right_on="Plant Code",

            how="left"
        )

        # Production Cost
        self.plan["Production Cost"] = (

            self.plan["Net Requirement"]

            *

            self.plan["Production Cost (₹/kl)"]

        )

        self.cost_table = self.plan

        return self.cost_table

    # ======================================================
    # Summary
    # ======================================================

    def summary(self):

        table = self.build_cost_table()

        total = table["Production Cost"].sum()

        print("\n" + "=" * 70)
        print("COST ANALYSIS")
        print("=" * 70)

        print(f"Total Production Cost : ₹{total:,.2f}")

        print("\nCost by Plant")

        print(

            table.groupby("Source")["Production Cost"]

            .sum()

            .sort_values(ascending=False)

        )