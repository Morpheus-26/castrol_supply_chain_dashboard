import pandas as pd


class DemandAnalyzer:
    """
    Performs demand analytics using January Forecast.
    """

    def __init__(self, demand_df):

        self.df = demand_df.copy()

        # Convert demand column to numeric
        self.df["Jan -2026 (in kL)"] = pd.to_numeric(
            self.df["Jan -2026 (in kL)"],
            errors="coerce"
        )

    # ---------------------------------------------------------
    # BASIC METRICS
    # ---------------------------------------------------------

    def total_records(self):
        return len(self.df)

    def total_demand(self):
        return self.df["Jan -2026 (in kL)"].sum()

    def total_skus(self):
        return self.df["Product Name"].nunique()

    def total_cfas(self):
        return self.df["CFA"].nunique()

    def total_regions(self):
        return self.df["CFA region"].nunique()

    # ---------------------------------------------------------
    # DEMAND ANALYSIS
    # ---------------------------------------------------------

    def demand_by_region(self):

        return (
            self.df
            .groupby("CFA region")["Jan -2026 (in kL)"]
            .sum()
            .sort_values(ascending=False)
        )

    def demand_by_cfa(self):

        return (
            self.df
            .groupby("CFA")["Jan -2026 (in kL)"]
            .sum()
            .sort_values(ascending=False)
        )

    def demand_by_sku(self):

        return (
            self.df
            .groupby("Product Name")["Jan -2026 (in kL)"]
            .sum()
            .sort_values(ascending=False)
        )

    # ---------------------------------------------------------
    # TOP INSIGHTS
    # ---------------------------------------------------------

    def highest_demand_region(self):

        demand = self.demand_by_region()

        return demand.idxmax(), demand.max()

    def highest_demand_cfa(self):

        demand = self.demand_by_cfa()

        return demand.idxmax(), demand.max()

    def highest_demand_sku(self):

        demand = self.demand_by_sku()

        return demand.idxmax(), demand.max()

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def summary(self):

        region, region_demand = self.highest_demand_region()
        cfa, cfa_demand = self.highest_demand_cfa()
        sku, sku_demand = self.highest_demand_sku()

        print("\n" + "=" * 70)
        print("DEMAND ANALYTICS DASHBOARD")
        print("=" * 70)

        print(f"Forecast Records          : {self.total_records()}")

        print(f"Unique SKUs              : {self.total_skus()}")

        print(f"Unique CFAs              : {self.total_cfas()}")

        print(f"Regions                  : {self.total_regions()}")

        print(f"Total January Demand     : {self.total_demand():,.2f} KL")

        print("\nHighest Demand Region")
        print("------------------------------")
        print(f"{region} : {region_demand:,.2f} KL")

        print("\nHighest Demand CFA")
        print("------------------------------")
        print(f"{cfa} : {cfa_demand:,.2f} KL")

        print("\nHighest Demand SKU")
        print("------------------------------")
        print(f"{sku} : {sku_demand:,.2f} KL")