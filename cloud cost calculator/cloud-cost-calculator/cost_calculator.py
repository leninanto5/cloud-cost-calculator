import argparse

from src.pricing import load_pricing, get_instance_sizes
from src.calculator import compare_providers, HOURS_PER_MONTH
from src.report import print_usage, print_report, export_csv


def ask_number(prompt, default, cast=int, minimum=0):
    """Asks the user for a number; pressing Enter keeps the default."""
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if value == "":
            return default
        try:
            number = cast(value)
            if number < minimum:
                print(f"  Please enter a value of {minimum} or more.")
                continue
            return number
        except ValueError:
            print("  Please enter a valid number.")


def ask_size(sizes, default):
    while True:
        value = input(f"Instance size {sizes} [{default}]: ").strip().lower()
        if value == "":
            return default
        if value in sizes:
            return value
        print(f"  Choose one of: {', '.join(sizes)}")


def interactive_usage(sizes):
    print("=== Cloud Cost Calculator ===")
    print("Press Enter to keep the value shown in [brackets].\n")
    return {
        "instances": ask_number("Number of virtual machines", 2, minimum=1),
        "instance_size": ask_size(sizes, "medium"),
        "hours": ask_number("Hours each VM runs per month", HOURS_PER_MONTH, minimum=1),
        "storage_gb": ask_number("Storage needed (GB)", 500, float),
        "transfer_gb": ask_number("Data transfer out per month (GB)", 300, float),
        "databases": ask_number("Managed databases", 1),
    }


def parse_args(sizes):
    parser = argparse.ArgumentParser(description="Compare monthly cloud costs for AWS, Azure and GCP.")
    parser.add_argument("--instances", type=int, help="number of virtual machines")
    parser.add_argument("--size", choices=sizes, default="medium", help="instance size")
    parser.add_argument("--hours", type=int, default=HOURS_PER_MONTH, help="hours per month each VM runs")
    parser.add_argument("--storage", type=float, default=0, help="storage in GB")
    parser.add_argument("--transfer", type=float, default=0, help="data transfer out in GB")
    parser.add_argument("--databases", type=int, default=0, help="number of managed databases")
    parser.add_argument("--export", action="store_true", help="save the report to data/cost_report.csv")
    return parser.parse_args()


def main():
    pricing = load_pricing()
    sizes = get_instance_sizes(pricing)
    args = parse_args(sizes)

    if args.instances is None:
        usage = interactive_usage(sizes)
        export = input("\nSave report as CSV? (y/n) [n]: ").strip().lower() == "y"
    else:
        usage = {
            "instances": args.instances,
            "instance_size": args.size,
            "hours": args.hours,
            "storage_gb": args.storage,
            "transfer_gb": args.transfer,
            "databases": args.databases,
        }
        export = args.export

    results = compare_providers(pricing, usage)
    print_usage(usage, pricing["currency"])
    print_report(results, pricing["currency"])
    print(f"\nNote: {pricing['note']}")

    if export:
        export_csv(results)


if __name__ == "__main__":
    main()
