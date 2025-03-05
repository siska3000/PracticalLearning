import argparse
import ast
import json

from ExcelSWAPIClient import ExcelSWAPIClient
from FetchClass import SWAPIClient
from Processors.FilmsProcessor import FilmsProcessor
from Processors.PeopleProcessor import PeopleProcessor
from Processors.PlanetsProcessor import PlanetsProcessor
from SWAPIDataManager import SWAPIDataManager


parser = argparse.ArgumentParser(description='My simple echo')
parser.add_argument('--source', '-s', help='Source of data (api or excel)', default='api')
parser.add_argument('--endpoint', '-e', help='Endpoints to fetch', default='people,planets')
parser.add_argument('--filters', '-f', help='Filters for data', default='{"people": ["films", "species"], "planets": ["films", "residents"]}')
parser.add_argument('--output', '-o', help='Output Excel file', default='swapi_data.xlsx')

args = parser.parse_args()
endpoints = args.endpoint.split(',')

if "https://swapi.dev/api/" in args.source:
    client = SWAPIClient(base_url=args.source)
elif "C:" in args.source:
    client = ExcelSWAPIClient(file_path=args.source)
else:
    raise ValueError("Invalid source")


manager = SWAPIDataManager(client)


manager.register_processor("people", PeopleProcessor())
manager.register_processor("planets", PlanetsProcessor())
manager.register_processor("films", FilmsProcessor())

try:
    some_dict = ast.literal_eval(args.filters)
    print("Parsed dictionary:", some_dict)

    for endpoint in endpoints:
        manager.fetch_entity(endpoint)
        if endpoint in some_dict:
            manager.apply_filter(endpoint, some_dict[endpoint])

    manager.save_to_excel(args.output)

except json.JSONDecodeError as e:
    print("Invalid JSON format:", e)
except Exception as e:
    print(f"Error: {e}")

"""
Example of using:
py main.py --source api --endpoint people,planets --filters "{'people': ['films', 'species'], 'planets': ['films', 'residents']}" --output swapi_data.xlsx
"""
