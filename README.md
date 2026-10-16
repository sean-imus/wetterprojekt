# Wetterprojekt

Downloads historical daily weather data from the German Weather Service (DWD), loads it into a SQLite database and lets you query and chart it in a small Python GUI.

## Installation

```bash
git clone https://github.com/sean-imus/wetterprojekt.git
cd wetterprojekt
```

## Requirements

1. **Python 3.10+**
2. Install the dependencies:
```bash
pip install -r requirements.txt
```
3. About 7 GB of free disk space

## Usage

Run the scripts in order:

```bash
python 1-downloader.py
python 2-extractor.py
python 3-create_db.py
python 4-import_to_db.py
python 5-fix_values.py
python 6-main.py
```

## Scripts

| Script | Description |
|--------|-------------|
| 1-downloader.py | Downloads weather data from the DWD |
| 2-extractor.py | Unpacks the ZIP files |
| 3-create_db.py | Creates the SQLite database and tables |
| 4-import_to_db.py | Imports station metadata and CSV data into the database |
| 5-fix_values.py | Replaces -999 with NULL and creates indexes |
| 6-main.py | GUI for querying and visualizing the data |

## Features

- Pick stations by federal state or for all of Germany
- Filter stations by typing
- Multiple weather metrics (temperature, precipitation, snow depth, wind, etc.)
- Custom time range (day, month and year input fields)
- Charts with Matplotlib
- Statistics: average, minimum, maximum

## Database schema

- `tbl_stationen`: station metadata (ID, name, federal state, elevation, coordinates)
- `tbl_messwerte`: weather measurements, with a foreign key to `tbl_stationen`

## Data source

Weather data from the [German Weather Service (Deutscher Wetterdienst, DWD)](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/)
