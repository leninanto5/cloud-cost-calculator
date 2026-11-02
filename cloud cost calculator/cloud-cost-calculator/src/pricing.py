import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICING_FILE = os.path.join(BASE_DIR, "data", "pricing.json")


def load_pricing(path=PRICING_FILE):
    """Loads the pricing data for all cloud providers from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_instance_sizes(pricing):
    """Returns the list of instance sizes available (taken from the first provider)."""
    first = next(iter(pricing["providers"].values()))
    return list(first["compute"].keys())
