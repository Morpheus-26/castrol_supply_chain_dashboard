import pandas as pd


class NetworkAnalyzer:

    def __init__(self, plant_hub_df, hub_cfa_df):

        self.plant_hub = plant_hub_df.copy()
        self.hub_cfa = hub_cfa_df.copy()

    # ---------------------------------------------------------
    # Plant -> Hub
    # ---------------------------------------------------------

    def plant_hub_costs(self):

        return self.plant_hub

    # ---------------------------------------------------------
    # Hub -> CFA
    # ---------------------------------------------------------

    def hub_cfa_costs(self):

        return self.hub_cfa

    # ---------------------------------------------------------
    # Summary
    # ---------------------------------------------------------

    def summary(self):

        print("\n" + "="*70)
        print("NETWORK ANALYTICS")
        print("="*70)

        print(f"Plants : {len(self.plant_hub)}")

        print(f"CFAs : {len(self.hub_cfa)}")

        print("\nPlant → Hub Matrix")

        print(self.plant_hub)

        print("\nHub → CFA Matrix")

        print(self.hub_cfa)