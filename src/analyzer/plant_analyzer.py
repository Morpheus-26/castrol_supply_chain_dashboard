import pandas as pd


class PlantAnalyzer:
    """
    Performs business analytics on the Plant Master data.
    """

    def __init__(self, plants_df):

        self.df = plants_df.copy()

        # Capacity columns
        self.capacity_cols = [
            "Line Capacity \n<=1.5 LT (kl / month)",
            "Line Capacity \n3- 5 LT (kl / month)",
            "Line Capacity \n7- 20 LT (kl / month)",
            "Line Capacity \n50 LT (kl / month)",
            "Line Capacity \n180- 210LT (kl / month)"
        ]

        # Convert capacities to numeric
        self.df[self.capacity_cols] = self.df[self.capacity_cols].apply(
            pd.to_numeric,
            errors="coerce"
        )

        # Convert production cost
        self.df["Production Cost (₹/kl)"] = pd.to_numeric(
            self.df["Production Cost (₹/kl)"],
            errors="coerce"
        )

        # Create Total Capacity column
        self.df["Total Capacity"] = self.df[self.capacity_cols].sum(axis=1)

    # ---------------------------------------------------------
    # BASIC METRICS
    # ---------------------------------------------------------

    def total_plants(self):
        return len(self.df)

    def total_capacity(self):
        return self.df["Total Capacity"].sum()

    def average_cost(self):
        return self.df["Production Cost (₹/kl)"].mean()

    # ---------------------------------------------------------
    # PLANT INSIGHTS
    # ---------------------------------------------------------

    def cheapest_plant(self):

        return self.df.loc[
            self.df["Production Cost (₹/kl)"].idxmin()
        ]

    def most_expensive_plant(self):

        return self.df.loc[
            self.df["Production Cost (₹/kl)"].idxmax()
        ]

    def highest_capacity_plant(self):

        return self.df.loc[
            self.df["Total Capacity"].idxmax()
        ]

    # ---------------------------------------------------------
    # TABLES
    # ---------------------------------------------------------

    def capacity_table(self):

        table = self.df[
            [
                "Plant Code",
                "Location",
                "Production Cost (₹/kl)",
                "Total Capacity"
            ]
        ].copy()

        total = table["Total Capacity"].sum()

        table["Capacity Share (%)"] = (
            table["Total Capacity"] / total * 100
        ).round(2)

        table = table.sort_values(
            by="Total Capacity",
            ascending=False
        )

        return table

    def capacity_by_packaging(self):

        summary = self.df[self.capacity_cols].sum()

        return summary

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def summary(self):

        cheapest = self.cheapest_plant()
        expensive = self.most_expensive_plant()
        highest = self.highest_capacity_plant()

        print("\n" + "=" * 70)
        print("PLANT ANALYTICS DASHBOARD")
        print("=" * 70)

        print(f"Total Plants               : {self.total_plants()}")

        print(f"Total Network Capacity     : {self.total_capacity():,.0f} KL/month")

        print(f"Average Production Cost    : ₹{self.average_cost():,.2f} / KL")

        print("\nCheapest Plant")
        print("-" * 30)
        print(f"{cheapest['Location']} ({cheapest['Plant Code']})")
        print(f"Production Cost : ₹{cheapest['Production Cost (₹/kl)']:,} / KL")

        print("\nMost Expensive Plant")
        print("-" * 30)
        print(f"{expensive['Location']} ({expensive['Plant Code']})")
        print(f"Production Cost : ₹{expensive['Production Cost (₹/kl)']:,} / KL")

        print("\nHighest Capacity Plant")
        print("-" * 30)
        print(f"{highest['Location']} ({highest['Plant Code']})")
        print(f"Capacity : {highest['Total Capacity']:,} KL/month")

        print("\n" + "=" * 70)
        print("PLANT CAPACITY TABLE")
        print("=" * 70)

        print(self.capacity_table())

        print("\n" + "=" * 70)
        print("CAPACITY BY PACKAGING LINE")
        print("=" * 70)

        print(self.capacity_by_packaging())