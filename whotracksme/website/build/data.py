import json
from pathlib import Path
from whotracksme.data.loader import DataSource
from whotracksme.data.db import load_tracker_db, create_tracker_map
from whotracksme.website.utils import print_progress

def build_tracker_db():
    with open('_site/data/trackerdb.json', 'w') as output:
        db_map = create_tracker_map(load_tracker_db(), with_iab_vendors=True)
        db_map['about'] = 'WhoTracks.Me tracker database: whotracks.me'
        json.dump(db_map, output, indent=2, sort_keys=True)
    print_progress(text='Generate tracker DB')

def build_tracker_json(tracker_id, data):
    stats = data.trackers.get_tracker(tracker_id)
    stats['overview'] = dict(stats['overview'])
    # drop some columns
    for col in ['companies', 'month', 'trackers', 'tracker', 'id', 'company_id', 'category', 'country', 'site_reach']:
        del stats['overview'][col]
    stats['date_range'] = [date.strftime('%Y-%m') for date in stats['date_range']]
    # print(stats)
    with open(f'_site/data/trackers/global/{tracker_id}.json', 'w') as output:
        json.dump(stats, output)

def build_api(data):
    # tracker overviews
    data_dir = Path('_site/data/trackers/global')
    if not data_dir.exists():
        data_dir.mkdir(parents=True)

    for id, stats in data.trackers.iter():
        build_tracker_json(id, data)

    print_progress(text='Generate API data')

def build_api_batch(batch):
    data = DataSource(populate=False)

    data_dir = Path('_site/data/trackers/global')
    if not data_dir.exists():
        data_dir.mkdir(parents=True)

    for tracker_id in batch:
        build_tracker_json(tracker_id, data)
