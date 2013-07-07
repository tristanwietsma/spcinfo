#!/usr/bin/python

import os, json
from string import join

import argparse
parser = argparse.ArgumentParser(description='Lookup U.S. counties (with FIPS) by state.')
parser.add_argument('--state', default="*", help="Filter by state. Full name, abbreviation, or partial. Case insenstitive.")
parser.add_argument('--county', default="*", help="Filter by county name. Case insensitive and partial matches.")

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

def Query(state='*', cnty='*', display_proj4_params=False):
	results = []
	params = []
	max_proj4_name = 0
	for abbr in data.keys():

		###################
		# filter by state #
		###################

		if not (state == '*' or abbr == state 
				or data[abbr]['NAME'].upper() == state):
			continue

		####################
		# filter by county #
		####################

		counties = data[abbr]['COUNTIES']
		if cnty == '*':
			cnty_keys = data[abbr]['COUNTIES'].keys()
		else:
			cnty_keys = [c for c in data[abbr]['COUNTIES'].keys() if cnty.upper() in c.upper()]
			if len(cnty_keys) == 0:
				continue

		results += [(data[abbr]['NAME'], c, counties[c]['FIPS'], counties[c]['NAD27 ZONE'],
			'%s (%s, %s)'%(counties[c]['NAD83 ZONE'], counties[c]['NAD83 NAME'], counties[c]['NAD83 PROJ'])) for c in cnty_keys]

	# formatting
	widths = []
	headers = 'STATE,COUNTY,FIPS,NAD27,NAD83 (NAME & PROJ)'.split(',')
	for idx in range(len(results[0])):
		widths.append(max([len(r[idx]) for r in results] + [len(headers[idx])]))

	# display
	print join([headers[i].ljust(widths[i]) for i in range(len(headers))], '  ')
	for ri in range(len(results)):
		r = results[ri]
		print join([r[i].ljust(widths[i]) for i in range(len(r))], '  ')

if __name__ == '__main__':

	args = parser.parse_args()
	Query(args.state.upper(), args.county.upper())
