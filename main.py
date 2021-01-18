import sys
import pandas as pd
import numpy as np
from math import cos, asin, sqrt, pi
import itertools


# global variable R is the average radius of planet Earth in kilometres.
R = 6371

def great_circle_distance(lat1, lon1, lat2, lon2):
    '''
    This function calculates the great circle distance between two points
    on Earth using the haversine formula and law of cosines.

    Please note that the formula uses a fixed radius of Earth, which is an
    approximation as the Earth is not a perfect sphere. Due to this the
    error rate can be up to 0.5%.

    Args:
    lat1 (float) - latitude of the first point between -90 and 90.
    lon1 (float) - longitude of the first point between -180 and 180.
    lat2 (float) - latitude of the second point between -90 and 90.
    lon2 (float) - longitude of the second point between -180 and 180.

    Returns:
    The number of kilometres between the two points as a float
    '''
    p = pi/180
    a = 0.5 - cos((lat2 - lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) \
        * (1 - cos((lon2 - lon1)*p))/2
    return 2 * R * asin(sqrt(a)) #R is avg. radius of the Earth in kilometres


def get_random_places(n):
    '''
    This function generates random places on the surface of the Earth.

    The naming will be generic: Location1, Location2, etc.
    The coordinates will be latitude and longitude.

    Args:
    n - integer indicating the number of random places to generate.

    Returns:
    df - DataFrame with three columns: place (names), latitude (-90, 90) and
        longitude (-180, 180).
    '''
    # create (generic) place names and add to the first column of new df
    prefix = 'Location'

    place_names = [(prefix + str(x)) for x in range(1, n + 1)]

    df = pd.DataFrame(place_names, columns=['Name'])

    # Use a coordinate system (z,phi) where z is an axis that runs from
    # south pole to north pole (z = -R to +R, where R is the sphere's radius),
    # and where phi is the longitude (-180 to 180). Then drawing uniformly
    # values for z and phi.

    z = np.random.uniform(-R, R, n)
    phi = np.random.uniform(-180, 180, n)

    # Then based on the fact that the area of a sphere's surface contained
    # between two parallel planes that both cut the sphere depends only on
    # the distance between the planes, not on where they cut it.
    # It can then be derived that the latitute 'theta' can be calculated by:

    theta = np.arcsin(z/R)*180/pi  # Factor 180/pi converts from radians to degrees

    # Add latitude and longitude to the df, then return df
    df['Latitude'] = pd.Series(theta)
    df['Longitude'] = pd.Series(phi)

    return df

def create_distances_df(places_df):
    '''
    This function creates a dataframe of pairs of places and the distance
    between them.

    Args:
    places_df - DataFrame with places, latitudes and longitudes

    Returns:
    distances_df - DataFrame with pairs of places and the distance between
    them, sorted on distance from shortest to longest.

    '''
    # set Name column as index
    places_df.set_index('Name', drop=True, inplace=True)

    # create dict with place as key and lat/lon as value (tuple)
    places_dict = places_df.T.apply(tuple).to_dict()

    # get all combinations of two distinct place names in a list
    # like: [('London', 'Alta'), ('Vardø', 'Oslo'), ... etc.]
    pairs = list(itertools.combinations(set(places_dict.keys()), 2))

    # ititialize list_of_dicts from which distances_df will be created
    list_of_dicts = []

    for pair in pairs:

        # get place names
        place_a = pair[0]
        place_b = pair[1]

        # get lat/lon values from places_dict
        a_lat = places_dict[place_a]['Latitude']
        a_lon = places_dict[place_a]['Longitude']
        b_lat = places_dict[place_b]['Latitude']
        b_lon = places_dict[place_b]['Longitude']

        # calculate distance in km utilizing 'great_circle_distance' function
        dist = great_circle_distance(a_lat, a_lon, b_lat, b_lon)

        # append data to list_of_dicts
        list_of_dicts.append(
            {
                'place A': place_a,
                'place B': place_b,
                'distance': dist
            }
        )

    # create df from list of dicts in ascending order by distance.
    distances_df = pd.DataFrame(list_of_dicts).sort_values(by='distance')

    return distances_df


def print_results(distances_df):
    '''
    This function prints the results to the command line.

    The results consist of two parts:
    1. Pairs of locations/places and the distance between them, sorted from
        shortest to longest.
    2. Average distance and places with distance between them closest to this
        average distance.

    Args:
    distances_df - DataFrame

    Returns:
    This function does not return anything.
    '''

    # printing the each row of data (no headers)
    print()
    for index, row in distances_df.iterrows():
        a = row["place A"]
        b = row["place B"]
        c = row["distance"]
        print("{:<25}{:<25}{:>10.1f} km".format(a, b, c))

    # calculate average distance
    avg_distance = distances_df.distance.mean()

    # add column with absolute difference to average distance
    distances_df['diff_mean'] = abs(distances_df['distance'] - avg_distance)

    # sort ascending based on 'diff_mean' and reset index
    distances_df.sort_values(by='diff_mean', inplace=True)
    distances_df.reset_index(drop=True, inplace=True)

    # printing average distance and closest pair to this average distance.
    place_a = distances_df['place A'][0]
    place_b = distances_df['place B'][0]
    dist = distances_df['distance'][0]
    print()
    print("Average distance: {:.1f} km. Closest pair: {} – {} {:.1f} km.\n".format(avg_distance, place_a, place_b, dist))


def main():

    if len(sys.argv) == 1:

        # no arguments given when running main.py

        # read data from file
        places_df = pd.read_csv('places.csv')

        # create dataframe of distances
        distances_df = create_distances_df(places_df)

        # print results
        print_results(distances_df)


    elif len(sys.argv) == 2:

        # exactly one argument given when running main.py

        if sys.argv[1].isdigit():

            # the argument is integer-like. For example 'python main.py 12'

            # store value of argument given as integer
            n = int(sys.argv[1])

            if n >= 2:

                # the argument is required to be at least 2.
                # (otherwise there are no distances possible)

                places_df = get_random_places(n)

                # create dataframe of distances
                distances_df = create_distances_df(places_df)

                # print results
                print_results(distances_df)

            else:
                print('The provided (whole number) argument has to be at least 2. Please try again')

        else:
            print('The provided argument is not an integer. Please try again')
    else:
        print('Too many arguments prodvided. Please provide 0 or 1 argument')



if __name__ == '__main__':
    main()
