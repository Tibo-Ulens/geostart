# GeoStart

Utility to convert a start coordinate and offsets in meter to geocoordinates

## Usage

```bash
./geostart.py {location_file.csv} {output_file_name.csv}
```

location_file.csv should have the following format:
```csv
HEADER
name,dx,dy
```
where dx is latitudinal offset in m and dy is longitudinal offset in m (yes it's reversed, blame 12urenloop)
