import os
import sqlite3
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Warmuplessons"))

from Caesar_Chiffre import chiffre
from Distance_on_Globe import berechne_distanz

from weather_db import WeatherDB


def test_caesar_verschluesselung():
    assert chiffre("abc", 1) == "bcd"


def test_caesar_entschluesselung():
    assert chiffre("bcd", -1) == "abc"


def test_caesar_roundtrip():
    verschluesselt = chiffre("Hallo Welt", 5)
    entschluesselt = chiffre(verschluesselt, -5)
    assert entschluesselt == "Hallo Welt"


def test_caesar_grossbuchstaben():
    assert chiffre("ABC", 1) == "BCD"


def test_caesar_umbruch():
    assert chiffre("xyz", 3) == "abc"


def test_caesar_offset_null():
    assert chiffre("Hallo", 0) == "Hallo"


def test_caesar_volles_alphabet():
    assert chiffre("abc", 26) == "abc"


def test_caesar_sonderzeichen_unveraendert():
    assert chiffre("Hallo, Welt!", 5) == "Mfqqt, Bjqy!"


def test_caesar_negativer_offset():
    assert chiffre("bcd", -1) == "abc"


def test_distanz_bochum_koeln():
    distanz = berechne_distanz(51.4818, 7.2162, 50.9375, 6.9603)
    assert 60 < distanz < 70


def test_distanz_gleicher_punkt():
    assert berechne_distanz(51.0, 10.0, 51.0, 10.0) == pytest.approx(0.0)


def test_distanz_symmetrie():
    d1 = berechne_distanz(48.1, 11.6, 52.5, 13.4)
    d2 = berechne_distanz(52.5, 13.4, 48.1, 11.6)
    assert d1 == pytest.approx(d2)


def test_distanz_positiv():
    assert berechne_distanz(0, 0, 1, 1) > 0


def test_distanz_aequator():
    distanz = berechne_distanz(0, 0, 0, 1)
    assert 110 < distanz < 113


@pytest.fixture
def test_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE tbl_stationen (
            STATIONS_ID INTEGER PRIMARY KEY,
            Stationsname TEXT, Bundesland TEXT,
            Stationshoehe REAL, geoBreite REAL, geoLaenge REAL
        )
    """
    )
    cursor.execute(
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

    cursor.execute(
        "INSERT INTO tbl_stationen VALUES (1, 'Bochum', 'Nordrhein-Westfalen', 100, 51.48, 7.22)"
    )
    cursor.execute(
        "INSERT INTO tbl_stationen VALUES (2, 'Berlin', 'Berlin', 50, 52.52, 13.40)"
    )

    messwerte = [
        (1, "20200115", 2.0),
        (1, "20200215", -1.0),
        (1, "20200615", 18.0),
        (1, "20200915", 14.0),
        (1, "20201215", 1.0),
        (1, "20210115", 3.0),
        (1, "20210615", 20.0),
        (2, "20200615", 19.0),
    ]
    for station_id, datum, tmk in messwerte:
        cursor.execute(
            "INSERT INTO tbl_messwerte (STATIONS_ID, MESS_DATUM, TMK) VALUES (?, ?, ?)",
            (station_id, datum, tmk),
        )

    conn.commit()
    conn.close()
    return db_path


def test_db_enthaelt_alle(test_db):
    db = WeatherDB(test_db)
    assert "Alle" in db.states


def test_db_bundeslaender_geladen(test_db):
    db = WeatherDB(test_db)
    assert "Nordrhein-Westfalen" in db.states
    assert "Berlin" in db.states


def test_db_stationen_geladen(test_db):
    db = WeatherDB(test_db)
    assert 1 in db.stations_data
    assert db.stations_data[1]["name"] == "Bochum"


def test_db_jahresbereich(test_db):
    db = WeatherDB(test_db)
    assert db.min_year == 2020
    assert db.max_year == 2021


def test_messwerte_im_zeitraum(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_measurements(1, "TMK", "20200101", "20201231")
    assert len(ergebnisse) == 5


def test_messwerte_einzelner_tag(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_measurements(1, "TMK", "20200115", "20200115")
    assert len(ergebnisse) == 1
    assert ergebnisse[0][1] == pytest.approx(2.0)


def test_messwerte_leer_ausserhalb(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_measurements(1, "TMK", "19000101", "19001231")
    assert ergebnisse == []


def test_messwerte_stationsfilter(test_db):
    db = WeatherDB(test_db)
    ergebnisse_1 = db.get_measurements(1, "TMK", "20200601", "20200630")
    ergebnisse_2 = db.get_measurements(2, "TMK", "20200601", "20200630")
    assert ergebnisse_1[0][1] == pytest.approx(18.0)
    assert ergebnisse_2[0][1] == pytest.approx(19.0)


def test_jahreswerte_anzahl(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_yearly_averages("TMK", 2020, 2021, station_id=1)
    assert len(ergebnisse) == 2


def test_jahreswerte_durchschnitt(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_yearly_averages("TMK", 2021, 2021, station_id=1)
    erwartet = (3.0 + 20.0) / 2
    assert ergebnisse[0][1] == pytest.approx(erwartet)


def test_jahreswerte_alle_stationen(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_yearly_averages("TMK", 2020, 2020)
    assert len(ergebnisse) == 1


def test_jahreswerte_leer(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_yearly_averages("TMK", 1800, 1801)
    assert ergebnisse == []


def test_monatswerte_richtige_monate(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_monthly_averages("TMK", 2020, station_id=1)
    monate = [r[0] for r in ergebnisse]
    assert "01" in monate and "06" in monate


def test_monatswerte_wert_korrekt(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_monthly_averages("TMK", 2020, station_id=1)
    monat_dict = {r[0]: r[1] for r in ergebnisse}
    assert monat_dict["06"] == pytest.approx(18.0)


def test_monatswerte_alle_stationen(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_monthly_averages("TMK", 2020)
    monat_dict = {r[0]: r[1] for r in ergebnisse}
    assert monat_dict["06"] == pytest.approx(18.5)


def test_monatswerte_falsches_jahr(test_db):
    db = WeatherDB(test_db)
    ergebnisse = db.get_monthly_averages("TMK", 1800)
    assert ergebnisse == []
