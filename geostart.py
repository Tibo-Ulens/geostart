#!/usr/bin/env python3

"""
# geostart.py

## Utility to convert a start coordinate and offsets in meter to geocoordinates

LATITUDE is X
LONGITUDE is Y
(for some god forsaken reason)

Based on:
https://stackoverflow.com/questions/7477003/calculating-new-longitude-latitude-from-old-n-meters
"""


import sys
import csv
from os.path import exists
import math


#### These need to be modified if the location of 12ul changes
START_COORDINATES: list[float] = [51.042103, 3.725674]
"""LAT, LON of the start point"""

RADIUS_M: float = 6365264
"""radius of the earth at the latitude of the start point IN M

see https://rechneronline.de/earth-radius/ (must multiply by 1000)"""
####

USAGE: str = """Usage: geostart.py {location_file.csv} {output_file_name.csv}

Calculates station geocoordinates given the 12ul start coordinate"""

M_TO_DEG = 1 / ((2 * math.pi / 360) * RADIUS_M)
"""1 meter convert to degreees at a given radius"""


def get_new_lat_lon(old_lat_lon: tuple[float, float], dxy: tuple[float, float]) -> tuple[float, float]:
	"""Converts an old coordinate pair and an offset to a new coordinate pair"""

	dlat = dxy[0] * M_TO_DEG
	lat = old_lat_lon[0] + dlat

	# longitudinal degrees get closer together as latitude increases
	# (math.cos needs radians)
	dlon = (dxy[1] * M_TO_DEG) / math.cos(lat * (math.pi / 180))
	lon = old_lat_lon[1] + dlon

	return (lat, lon)


def get_files() -> tuple[str, str]:
	"""Read the filename from command line and verify it's correct"""

	infile: str = ""
	outfile: str = ""

	match len(sys.argv):
		case 1:
			print("Wrong number of arguments")
			print(USAGE)
			sys.exit(1)
		case 3:
			infile = sys.argv[1]
			outfile = sys.argv[2]
		case _:
			print("Wrong number of arguments")
			print(USAGE)
			sys.exit(1)

	if not exists(infile):
		print(f"'{infile}' is not a file")
		print(USAGE)
		sys.exit(1)

	return (infile, outfile)


def read_locations(file: str) -> dict[str, tuple[float, float]]:
	"""Read the location offsets from the file"""

	locations: dict[str, tuple[float, float]] = {}

	with open(file, "r") as f:
		reader = csv.reader(f)
		# Skip header row
		reader.__next__()
		try:
			locations = { row[0]: (float(row[1]), float(row[2])) for row in reader }
		except ValueError as err:
			print(err)
			sys.exit(1)

	return locations


def convert_locations(locations: dict[str, tuple[float, float]]) -> dict[str, tuple[float, float]]:
	"""Convert all the locations to (lat, lon)"""

	new_locations: dict[str, tuple[float, float]] = {}

	for name, offsets in locations.items():
		lat, lon = get_new_lat_lon(START_COORDINATES, offsets)

		print(f"{name}: {lat}° N, {lon}° E")
		new_locations[name] = (lat, lon)

	return new_locations


def write_new_locations(outfile: str, header: list[str], new_locations: dict[str, tuple[float, float]]) -> None:
	with open(outfile, "w+") as f:
		writer = csv.writer(f)
		writer.writerow(header)

		for name, (lat, lon) in new_locations.items():
			writer.writerow([name, lat, lon])


if __name__ == "__main__":
	print(f"start lat: {START_COORDINATES[0]}, start lon: {START_COORDINATES[1]}\n")

	infile, outfile = get_files()
	locations = read_locations(infile)
	new_locations = convert_locations(locations)

	write_new_locations(outfile, ["Puntnaam", "Latitude", "Longitude"], new_locations)
