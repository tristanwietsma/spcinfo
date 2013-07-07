#!/usr/bin/python

import os, json
from string import join

import argparse
parser = argparse.ArgumentParser(description='Fetch state plane coordinate system projection parameters for PROJ4')
parser.add_argument('--fips', default=None, help="Search by county FIPS code")
parser.add_argument('--nad83', default=None, help="Search by NAD83 zone")

##########################
# Parse us-counties.json #
##########################

LOCATION = join(os.path.realpath(__file__).split('/')[:-1], '/')
json_data = open(LOCATION + '/us_counties.json')
data = json.load(json_data)
json_data.close()

#################
# Execute Query #
#################

def _q(d):
	for k in d.keys():
		print '%s: %s'%(k, d[k])

def Query(fips=None, nad83=None):
	if fips is not None:
		for s in data.keys():
			for c in data[s]['COUNTIES'].keys():
				if data[s]['COUNTIES'][c]['FIPS'] == fips:
					_q(data[s]['COUNTIES'][c]['PROJ4'])
					return
	if nad83 is not None:
		for s in data.keys():
			for c in data[s]['COUNTIES'].keys():
				if data[s]['COUNTIES'][c]['NAD83 ZONE'] == nad83:
					_q(data[s]['COUNTIES'][c]['PROJ4'])
					return

if __name__ == '__main__':

	args = parser.parse_args()
	if args.fips is not None:
		Query(fips=args.fips)
	elif args.nad83 is not None:
		Query(nad83=args.nad83)
