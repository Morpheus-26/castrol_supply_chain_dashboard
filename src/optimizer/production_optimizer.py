import pandas as pd


class ProductionOptimizer:

    def __init__(self, planning_table, plants_df):

        self.plan = planning_table.copy()
        self.plants = plants_df.copy()

        self.capacity_cols = [
            "Line Capacity \n<=1.5 LT (kl / month)",
            "Line Capacity \n3- 5 LT (kl / month)",
            "Line Capacity \n7- 20 LT (kl / month)",
            "Line Capacity \n50 LT (kl / month)",
            "Line Capacity \n180- 210LT (kl / month)"
        ]

        self.prepare_capacity()

    # ----------------------------------------------------
    # Prepare Plant Capacity
    # ----------------------------------------------------

    def prepare_capacity(self):

        self.plants[self.capacity_cols] = (
            self.plants[self.capacity_cols]
            .apply(pd.to_numeric, errors="coerce")
        )

        self.plants["Available Capacity"] = (
            self.plants[self.capacity_cols].sum(axis=1)
        )

    # ----------------------------------------------------
    # Summary
    # ----------------------------------------------------

    def summary(self):

        print("\n" + "=" * 70)
        print("PLANT CAPACITY")
        print("=" * 70)

        print(
            self.plants[
                [
                    "Plant Code",
                    "Location",
                    "Available Capacity",
                    "Production Cost (₹/kl)"
                ]
            ]
        )

    # ----------------------------------------------------
    # Capacity vs Demand
    # ----------------------------------------------------

    def capacity_vs_demand(self):

        total_capacity = self.plants[
            "Available Capacity"
        ].sum()

        total_requirement = self.plan[
            "Net Requirement"
        ].sum()

        print("\n" + "=" * 70)
        print("CAPACITY VS DEMAND")
        print("=" * 70)

        print(f"Available Capacity : {total_capacity:,.2f} KL")
        print(f"Net Requirement    : {total_requirement:,.2f} KL")

        gap = total_capacity - total_requirement

        print(f"Remaining Capacity : {gap:,.2f} KL")

        if gap >= 0:
            print("\n✅ Capacity is sufficient.")
        else:
            print("\n❌ Capacity is NOT sufficient.")