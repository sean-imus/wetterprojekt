1. Run downloader.py to download all zip files with Wetterdata included
2. Run extractor.py to extract the zip files
3. Run create_db.py to create the empty sqlite database with a provided schema
4. Run csv_to_sql.py to copy the contents of all the extracted csv files into the database
5. Run main.py to use the sqlite database to view certain stats
