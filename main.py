import os

from src.data.data_loader import DataLoader
from src.data.supply_chain_data import SupplyChainData

from src.analyzer.plant_analyzer import PlantAnalyzer
from src.analyzer.demand_analyzer import DemandAnalyzer
from src.analyzer.network_analyzer import NetworkAnalyzer
from src.analyzer.cost_analyzer import CostAnalyzer
from src.analyzer.dashboard_analyzer import DashboardAnalyzer

from src.engines.inventory_engine import InventoryEngine

from src.optimizer.production_optimizer import ProductionOptimizer


# ==========================================================
# CONFIGURATION
# ==========================================================

FILE_PATH = "data/supply_chain_datasheet.xlsx"

OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================================
# CASTROL SUPPLY CHAIN PLANNING TOOL
# ==========================================================

print("=" * 80)
print("CASTROL SUPPLY CHAIN PLANNING TOOL")
print("=" * 80)


# ==========================================================
# STEP 1 : LOAD DATA
# ==========================================================

loader = DataLoader(FILE_PATH)
raw_data = loader.load_data()


# ==========================================================
# STEP 2 : CLEAN DATA
# ==========================================================

sc = SupplyChainData(raw_data)
sc.clean()

print("\n✅ Data Loaded & Cleaned Successfully")


# ==========================================================
# STEP 3 : PLANT ANALYTICS
# ==========================================================

plant = PlantAnalyzer(sc.plants)
plant.summary()


# ==========================================================
# STEP 4 : DEMAND ANALYTICS
# ==========================================================

demand = DemandAnalyzer(sc.jan_forecast)
demand.summary()


# ==========================================================
# STEP 5 : INVENTORY PLANNING
# ==========================================================

inventory = InventoryEngine(
    sc.jan_forecast,
    sc.inventory
)

inventory.summary()

planning_table = inventory.get_planning_table()

print("\n" + "=" * 80)
print("PLANNING TABLE")
print("=" * 80)

print(planning_table.head())


# ==========================================================
# STEP 6 : NETWORK ANALYTICS
# ==========================================================

network = NetworkAnalyzer(
    sc.plant_hub,
    sc.hub_cfa
)

network.summary()


# ==========================================================
# STEP 7 : PRODUCTION OPTIMIZATION
# ==========================================================

optimizer = ProductionOptimizer(
    planning_table,
    sc.plants
)

production_summary = optimizer.summary()
optimizer.capacity_vs_demand()


# ==========================================================
# STEP 8 : COST ANALYSIS
# ==========================================================

#cost = CostAnalyzer(
 #   planning_table,
 #   sc.plants,
 #   sc.source_lt,
 #   sc.plant_hub,
  #  sc.hub_cfa
#)

#cost.summary()

#cost_table = cost.build_cost_table()


# ==========================================================
# STEP 9 : EXECUTIVE DASHBOARD KPIs
# ==========================================================

dashboard = DashboardAnalyzer(
    planning_table,
    sc.plants
)

dashboard.generate_kpis()


# ==========================================================
# STEP 10 : EXPORT FILES FOR DASHBOARD
# ==========================================================

print("\nExporting processed files...")

planning_table.to_csv(
    os.path.join(OUTPUT_DIR, "planning_table.csv"),
    index=False
)

sc.plants.to_csv(
    os.path.join(OUTPUT_DIR, "plants.csv"),
    index=False
)

sc.jan_forecast.to_csv(
    os.path.join(OUTPUT_DIR, "jan_forecast.csv"),
    index=False
)

sc.inventory.to_csv(
    os.path.join(OUTPUT_DIR, "inventory.csv"),
    index=False
)

sc.plant_hub.to_csv(
    os.path.join(OUTPUT_DIR, "plant_hub.csv"),
    index=False
)

sc.hub_cfa.to_csv(
    os.path.join(OUTPUT_DIR, "hub_cfa.csv"),
    index=False
)

#cost_table.to_csv(
 #   os.path.join(OUTPUT_DIR, "cost_table.csv"),
  #  index=False
#)

if production_summary is not None:
    production_summary.to_csv(
        os.path.join(OUTPUT_DIR, "production_summary.csv"),
        index=False
    )

print("✅ All CSV files exported successfully.")


# ==========================================================
# PIPELINE COMPLETED
# ==========================================================

print("\n" + "=" * 80)
print("CASTROL SUPPLY CHAIN ANALYSIS COMPLETED")
print("=" * 80)

print("""
Modules Executed Successfully
-----------------------------
✔ Data Loading
✔ Data Cleaning
✔ Plant Analytics
✔ Demand Analytics
✔ Inventory Planning
✔ Network Analytics
✔ Production Optimization
✔ Cost Analysis
✔ Dashboard KPI Generation
✔ CSV Export for Dashboard
""")