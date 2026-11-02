# Cloud Cost Calculator

A Python command-line tool that estimates and compares the monthly and yearly cost of running the same workload on **AWS, Azure and Google Cloud (GCP)**. It shows a cost breakdown for each provider and tells you which one is cheapest.

## Features
- Compare AWS, Azure and GCP side by side
- Cost breakdown: compute, storage, data transfer and database
- Monthly and yearly totals
- Highlights the cheapest provider and the possible savings
- Works in interactive mode or with command-line arguments
- Export the report to a CSV file
- Prices stored in an editable JSON file

## Tech Stack
- Python 3
- tabulate (table output)
- JSON, CSV

## Project Structure
```
cloud-cost-calculator/
├── data/
│   └── pricing.json        # provider prices (editable)
├── src/
│   ├── pricing.py          # loads pricing data
│   ├── calculator.py       # cost calculation logic
│   └── report.py           # table output and CSV export
├── cost_calculator.py      # main program
├── requirements.txt
└── README.md
```

## How to Run

1. Clone the repository
```bash
git clone https://github.com/leninanto5/cloud-cost-calculator.git
cd cloud-cost-calculator
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run in interactive mode
```bash
python cost_calculator.py
```

4. Or run with arguments
```bash
python cost_calculator.py --instances 3 --size large --storage 1000 --transfer 500 --databases 1 --export
```

## Arguments
| Argument | Description | Default |
|---|---|---|
| `--instances` | Number of virtual machines | interactive mode if not given |
| `--size` | small, medium, large, xlarge | medium |
| `--hours` | Hours each VM runs per month | 730 |
| `--storage` | Storage in GB | 0 |
| `--transfer` | Data transfer out in GB | 0 |
| `--databases` | Number of managed databases | 0 |
| `--export` | Save report to `data/cost_report.csv` | off |

## Cost Formula
```
Compute  = price per hour x hours x instances
Storage  = price per GB x storage GB
Transfer = (transfer GB - free GB) x price per GB
Database = price per hour x 730 x databases
Total    = Compute + Storage + Transfer + Database
```

## Note
The prices in `data/pricing.json` are sample values for learning. Update them with the latest rates from the official AWS, Azure and GCP pricing pages.

## Author
**Leninanto**
GitHub: [leninanto5](https://github.com/leninanto5)
