SPC: State Plane Coordinates
===========================

Working with the state plane coordinate system can be a pain, so I've compiled some useful information (like NAD83 zones and PROJ4 parameters) on a county basis. To allow rapid search, I've wrapped the data with a couple Python scripts.

Prerequisites
-------------

* Python 2.7.X

county-lookup
-------------

*county-lookup* provides high level access to the data stored in us_counties.json. You can filter on state (either abbreviation or full name) and/or county name (including partial matches). Filtering is not case sensitive.

The following information is returned:

* 5-digit FIPS code

* NAD27 zone

* NAD83 zone, with common name and the projection used (the PROJ4 name)

For parameter information, try "help":

    $ ./county-lookup --help
    usage: county-lookup [-h] [--state STATE] [--county COUNTY]

    Lookup U.S. counties (with FIPS) by state.

    optional arguments:
      -h, --help       show this help message and exit
      --state STATE    Filter by state. Full name, abbreviation, or partial. Case insensitive.
      --county COUNTY  Filter by county name. Case insensitive and partial matches.

Example usage:

    $ ./county-lookup --state Illinois --county Cl
    STATE     COUNTY     FIPS   NAD27  NAD83 (NAME & PROJ)        
    Illinois  McLean     17113  1201   1201 (Illinois East, tmerc)
    Illinois  Clay       17025  1201   1201 (Illinois East, tmerc)
    Illinois  Clinton    17027  1202   1202 (Illinois West, tmerc)
    Illinois  Clark      17023  1201   1201 (Illinois East, tmerc)
    Illinois  St. Clair  17163  1202   1202 (Illinois West, tmerc)

proj4-params
------------

*proj4-params* retrieves the PROJ4 projection parameters given either the FIPS code or NAD83 zone. Currently, the only projection available is in US survey feet.

Command-line help:

    $ ./proj4-params --help
    usage: proj4-params [-h] [--fips FIPS] [--nad83 NAD83]

    Fetch state plane coordinate system projection parameters for PROJ4

    optional arguments:
      -h, --help     show this help message and exit
      --fips FIPS    Search by county FIPS code
      --nad83 NAD83  Search by NAD83 zone

Example usage:

First, we look up the county of interest (in this case, Champaign, Illinois):

    $ ./county-lookup --state IL --county Champaign
    STATE     COUNTY     FIPS   NAD27  NAD83 (NAME & PROJ)        
    Illinois  Champaign  17019  1201   1201 (Illinois East, tmerc)

We can search using either the FIPS or NAD83.

    $ ./proj4-params --nad83 1201
    NAD83(97) US SURVEY FEET: +proj=tmerc +lat_0=36.66666666666666 +lon_0=-88.33333333333333 +k=0.9999749999999999 +x_0=300000.0000000001 +y_0=0 +ellps=GRS80 +to_meter=0.3048006096012192 +no_defs

