import csv
import os
from tabulate import tabulate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPORT_FILE = os.path.join(BASE_DIR, "data", "cost_report.csv")


def print_usage(usage, currency):
    print("\nUsage summary")
    print("-" * 40)
    print(f"Instances        : {usage['instances']} x {usage['instance_size']}")
    print(f"Hours per month  : {usage['hours']}")
    print(f"Storage          : {usage['storage_gb']} GB")
    print(f"Data transfer out: {usage['transfer_gb']} GB")
    print(f"Databases        : {usage['databases']}")
    print(f"Currency         : {currency}")


def print_report(results, currency):
    headers = ["Provider", "Compute", "Storage", "Transfer", "Database", "Monthly", "Yearly"]
    rows = [
        [r["provider"], r["compute"], r["storage"], r["transfer"],
         r["database"], r["monthly_total"], r["yearly_total"]]
        for r in results
    ]
    print(f"\nCost comparison ({currency})")
    print(tabulate(rows, headers=headers, tablefmt="grid", floatfmt=".2f"))

    cheapest, costliest = results[0], results[-1]
    saving = costliest["monthly_total"] - cheapest["monthly_total"]
    print(f"\nCheapest option : {cheapest['provider']} at {cheapest['monthly_total']:.2f} {currency}/month")
    print(f"You save up to  : {saving:.2f} {currency}/month "
          f"({saving * 12:.2f} {currency}/year) compared to {costliest['provider']}")


def export_csv(results, path=EXPORT_FILE):
    fields = ["provider", "compute", "storage", "transfer", "database",
              "monthly_total", "yearly_total"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    print(f"\nReport saved to {path}")
