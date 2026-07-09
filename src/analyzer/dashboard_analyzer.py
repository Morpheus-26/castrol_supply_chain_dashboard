import pandas as pd


class DashboardAnalyzer:

    def __init__(
        self,
        planning_table,
        plants_df
    ):

        self.plan = planning_table.copy()
        self.plants = plants_df.copy()

    # ---------------------------------------------------------
    # Dashboard KPIs
    # ---------------------------------------------------------

    def generate_kpis(self):

        capacity_cols = [
            "Line Capacity \n<=1.5 LT (kl / month)",
            "Line Capacity \n3- 5 LT (kl / month)",
            "Line Capacity \n7- 20 LT (kl / month)",
            "Line Capacity \n50 LT (kl / month)",
            "Line Capacity \n180- 210LT (kl / month)"
        ]

        self.plants[capacity_cols] = self.plants[
            capacity_cols
        ].apply(pd.to_numeric)

        total_capacity = self.plants[
            capacity_cols
        ].sum().sum()

        total_forecast = self.plan["Forecast"].sum()

        opening_inventory = self.plan["Opening Inventory"].sum()

        net_requirement = self.plan["Net Requirement"].sum()

        inventory_coverage = (
            opening_inventory / total_forecast
        ) * 100

        utilization = (
            net_requirement / total_capacity
        ) * 100

        print("\n" + "="*70)
        print("EXECUTIVE DASHBOARD KPI")
        print("="*70)

        print(f"Total Forecast          : {total_forecast:,.2f} KL")
        print(f"Opening Inventory       : {opening_inventory:,.2f} KL")
        print(f"Net Requirement         : {net_requirement:,.2f} KL")
        print(f"Total Plant Capacity    : {total_capacity:,.2f} KL")
        print(f"Inventory Coverage      : {inventory_coverage:.2f}%")
        print(f"Capacity Utilization    : {utilization:.2f}%")