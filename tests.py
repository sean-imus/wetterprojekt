import sys
import os
import sqlite3

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Warmuplessons"))

from weather_db import WeatherDB
from Caesar_Chiffre import chiffre
from Distance_on_Globe import berechne_distanz


# ─── Caesar Chiffre ────────────────────────────────────────────────────────────


class TestCaesarChiffre:
    def test_roundtrip(self):
        assert chiffre(chiffre("Hallo Welt", 7), -7) == "Hallo Welt"

    def test_encrypt_lowercase(self):
        assert chiffre("abc", 1) == "bcd"

    def test_encrypt_uppercase(self):
        assert chiffre("ABC", 1) == "BCD"

    def test_wrap_lowercase(self):
        assert chiffre("xyz", 3) == "abc"

    def test_wrap_uppercase(self):
        assert chiffre("XYZ", 3) == "ABC"

    def test_zero_offset(self):
        assert chiffre("Hello", 0) == "Hello"

    def test_full_alphabet_offset(self):
        assert chiffre("abc", 26) == "abc"

    def test_preserves_special_chars(self):
        assert chiffre("Hallo, Welt!", 5) == "Mfqqt, Bjqy!"

    def test_negative_offset(self):
        assert chiffre("bcd", -1) == "abc"

    def test_mixed_case_and_spaces(self):
        result = chiffre("Hello World", 13)
        assert chiffre(result, -13) == "Hello World"


# ─── Haversine Distanz ─────────────────────────────────────────────────────────


class TestHaversineDistanz:
    def test_bochum_koeln(self):
        dist = berechne_distanz(51.4818, 7.2162, 50.9375, 6.9603)
        assert 60 < dist < 70

    def test_same_point_is_zero(self):
        assert berechne_distanz(51.0, 10.0, 51.0, 10.0) == pytest.approx(0.0)

    def test_symmetry(self):
        d1 = berechne_distanz(48.1, 11.6, 52.5, 13.4)
        d2 = berechne_distanz(52.5, 13.4, 48.1, 11.6)
        assert d1 == pytest.approx(d2)

    def test_result_is_positive(self):
        assert berechne_distanz(0, 0, 1, 1) > 0

    def test_known_equator_distance(self):
        # 1 degree of longitude on the equator ≈ 111.19 km
        dist = berechne_distanz(0, 0, 0, 1)
        assert 110 < dist < 113


# ─── WeatherDB ─────────────────────────────────────────────────────────────────


@pytest.fixture
def test_db(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE tbl_stationen (
            STATIONS_ID INTEGER PRIMARY KEY,
            Stationsname TEXT, Bundesland TEXT,
            Stationshoehe REAL, geoBreite REAL, geoLaenge REAL
        )
    """
    )
    cur.execute(
        """
        CREATE TABLE tbl_messwerte (
            Mid INTEGER PRIMARY KEY AUTOINCREMENT,
            STATIONS_ID INTEGER, MESS_DATUM TEXT,
            QN_3 INTEGER, FX REAL, FM REAL, QN_4 INTEGER,
            RSK REAL, RSKF REAL, SDK REAL, SHK_TAG REAL,
            NM REAL, VPM REAL, PM REAL, TMK REAL, UPM INTEGER,
            TXK REAL, TNK REAL, TGK REAL
        )
    """
    )
    cur.executemany(
        "INSERT INTO tbl_stationen VALUES (?, ?, ?, ?, ?, ?)",
        [
            (1, "Bochum", "Nordrhein-Westfalen", 100, 51.48, 7.22),
            (2, "Berlin", "Berlin", 50, 52.52, 13.40),
        ],
    )
    # Station 1: data across 2020 and 2021, various months
    measurements = [
        (1, "20200115", 2.0),
        (1, "20200215", -1.0),
        (1, "20200615", 18.0),
        (1, "20200915", 14.0),
        (1, "20201215", 1.0),
        (1, "20210115", 3.0),
        (1, "20210615", 20.0),
        (2, "20200615", 19.0),
    ]
    cur.executemany(
        "INSERT INTO tbl_messwerte (STATIONS_ID, MESS_DATUM, TMK) VALUES (?, ?, ?)",
        measurements,
    )
    conn.commit()
    conn.close()
    return str(db_file)


class TestWeatherDBInit:
    def test_states_contains_alle(self, test_db):
        db = WeatherDB(test_db)
        assert "Alle" in db.states

    def test_states_contains_bundeslaender(self, test_db):
        db = WeatherDB(test_db)
        assert "Nordrhein-Westfalen" in db.states
        assert "Berlin" in db.states

    def test_stations_data_loaded(self, test_db):
        db = WeatherDB(test_db)
        assert 1 in db.stations_data
        assert db.stations_data[1]["name"] == "Bochum"
        assert db.stations_data[1]["state"] == "Nordrhein-Westfalen"

    def test_year_range(self, test_db):
        db = WeatherDB(test_db)
        assert db.min_year == 2020
        assert db.max_year == 2021


class TestGetMeasurements:
    def test_returns_rows_in_range(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_measurements(1, "TMK", "20200101", "20201231")
        assert len(results) == 5

    def test_single_date(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_measurements(1, "TMK", "20200115", "20200115")
        assert len(results) == 1
        assert results[0][1] == pytest.approx(2.0)

    def test_no_results_outside_range(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_measurements(1, "TMK", "19000101", "19001231")
        assert results == []

    def test_station_filter_is_applied(self, test_db):
        db = WeatherDB(test_db)
        r1 = db.get_measurements(1, "TMK", "20200601", "20200630")
        r2 = db.get_measurements(2, "TMK", "20200601", "20200630")
        assert len(r1) == 1 and results_value(r1, 0) == pytest.approx(18.0)
        assert len(r2) == 1 and results_value(r2, 0) == pytest.approx(19.0)


def results_value(results, idx):
    return results[idx][1]


class TestGetYearlyAverages:
    def test_returns_one_row_per_year(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_yearly_averages("TMK", 2020, 2021, station_id=1)
        assert len(results) == 2
        years = [r[0] for r in results]
        assert "2020" in years and "2021" in years

    def test_average_value_correct(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_yearly_averages("TMK", 2021, 2021, station_id=1)
        assert len(results) == 1
        expected = (3.0 + 20.0) / 2
        assert results[0][1] == pytest.approx(expected)

    def test_all_stations(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_yearly_averages("TMK", 2020, 2020)
        assert len(results) == 1
        assert results[0][0] == "2020"

    def test_empty_range_returns_nothing(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_yearly_averages("TMK", 1800, 1801)
        assert results == []


class TestGetMonthlyAverages:
    def test_returns_correct_months(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_monthly_averages("TMK", 2020, station_id=1)
        months = [r[0] for r in results]
        assert "01" in months
        assert "06" in months

    def test_monthly_value_correct(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_monthly_averages("TMK", 2020, station_id=1)
        month_dict = {r[0]: r[1] for r in results}
        assert month_dict["06"] == pytest.approx(18.0)

    def test_all_stations_aggregates(self, test_db):
        # Both station 1 and 2 have June 2020 data → average of 18.0 and 19.0
        db = WeatherDB(test_db)
        results = db.get_monthly_averages("TMK", 2020)
        month_dict = {r[0]: r[1] for r in results}
        assert month_dict["06"] == pytest.approx(18.5)

    def test_wrong_year_returns_nothing(self, test_db):
        db = WeatherDB(test_db)
        results = db.get_monthly_averages("TMK", 1800)
        assert results == []
