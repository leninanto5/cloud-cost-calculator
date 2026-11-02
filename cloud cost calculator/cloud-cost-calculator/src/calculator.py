HOURS_PER_MONTH = 730


def calculate_cost(prices, usage):
    """
    Calculates the monthly cost for ONE provider.

    prices: pricing dictionary of the provider
    usage : dictionary with instances, instance_size, hours, storage_gb,
            transfer_gb, databases
    """
    size = usage["instance_size"]
    if size not in prices["compute"]:
        raise ValueError(f"Unknown instance size: {size}")

    compute = prices["compute"][size] * usage["hours"] * usage["instances"]
    storage = prices["storage_per_gb_month"] * usage["storage_gb"]

    billable_transfer = max(0, usage["transfer_gb"] - prices.get("free_transfer_gb", 0))
    transfer = billable_transfer * prices["transfer_out_per_gb"]

    database = prices["database_per_hour"] * HOURS_PER_MONTH * usage["databases"]

    total = compute + storage + transfer + database
    return {
        "compute": round(compute, 2),
        "storage": round(storage, 2),
        "transfer": round(transfer, 2),
        "database": round(database, 2),
        "monthly_total": round(total, 2),
        "yearly_total": round(total * 12, 2),
    }


def compare_providers(pricing, usage):
    """Calculates the cost for every provider, cheapest first."""
    results = []
    for name, prices in pricing["providers"].items():
        cost = calculate_cost(prices, usage)
        cost["provider"] = name
        results.append(cost)
    return sorted(results, key=lambda r: r["monthly_total"])
