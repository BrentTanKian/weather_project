from ETL_Functions.functions import clean_extract_two_hour, clean_extract_one_day, clean_extract_four_day
import json


def test_clean_extract_two_hour(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    with open('../weatherProject/test/fixtures/two_hour.json') as f:
        d = json.load(f)
    snapshot.assert_match(clean_extract_two_hour(d).to_csv().encode('utf-8'), 'two_hour_output.csv')


def test_clean_extract_one_day(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    with open('../weatherProject/test/fixtures/one_day.json') as f:
        d = json.load(f)
    snapshot.assert_match(clean_extract_one_day(d).to_csv().encode('utf-8'), 'one_day_output.csv')


def test_clean_extract_four_day(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    with open('../weatherProject/test/fixtures/four_day.json') as f:
        d = json.load(f)
    snapshot.assert_match(clean_extract_four_day(d).to_csv().encode('utf-8'), 'four_day_output.csv')