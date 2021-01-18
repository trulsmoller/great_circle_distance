### Date created
2021-01-18

### Great Circle Distance
Command line program that calculates "Great Circle Distance" based on latitude/longitude.

### Description
This command line program calculates "Great Circle Distance" based on latitude/longitude, ie. the distance between two points on the surface of the Earth following the curvature.

Please note: In the program the shape of the Earth is viewed in a simplified manner, namely as a perfect sphere with radius of 6,371 km.

The user can specify the number of locations. If not specified, a default data file with ten REAL locations will be used. If specified, the given number of locations will be generated randomly. The names will then just be generic (Location1, Location2, etc.) and the locations will spread randomly around the surface of the Earth.

The minimum numeric argument is 2 since we are looking at distances.

The result is printed to the command line and will contain:
- All distinct combinations of two locations and the distance between them. The list of combinations is sorted in ascending order on distance.
- The average distance. And the two locations with distance closest to the average distance.

### Dependencies

- Python 3.7+
- Libraries: pandas, numpy

### Installation

1. Clone this repo
2. (Optional) Activate your virtual env. Run: pip install -r requirements.txt

### Running the Program

Run one of the following commands in the root directory:

```python
python main.py
```
OR

```python
python main.py 10
```

In the first command the locations will be the ten REAL locations in the file ´places.csv´.

In the second command generic places randomly located around the Earth will be generated. The number of places is based on the input argument, whether that is 5, 10 or 50. The minimum numeric argument is 2.
