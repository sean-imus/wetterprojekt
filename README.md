# Wetterprojekt

## Setup

### Prerequisites

1. **Python 3.10+** required
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Installation

```bash
git clone https://github.com/sean-imus/wetterprojekt.git
cd wetterprojekt
```

## Quick Start

Run the scripts in order:

```bash
python 1-downloader.py
python 2-extractor.py
python 3-create_db.py
python 4-csv_to_sql.py
python 5-fix_values.py
python 6-main.py
```

## License

This project is free to use. Do whatever you want with it.

## Data Source

Weather data from [Deutscher Wetterdienst (DWD)](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/)
