#!/usr/bin/env python
#
# extract permissions and features from Android manifest
# put this script into the androguard directory
# fixed from : https://gist.github.com/geekman on 23.12.2022
# to run in terminal: sudo python3 extract.py output.csv input-file-apk/dir
 

import os
import sys
import csv
import traceback

import androguard.core.apk as apk

def process_apk(filename):
	results = {'_file': os.path.basename(filename)}

	try:
		a = apk.APK(filename)
		features = a.get_elements('uses-feature', 'name')
		perms = a.get_permissions()

		# if uses-feature describes a GL version, there will be no name
		if '' in features:
			features.remove('')

		results.update(dict(('p_' + p, 1) for p in perms))
		results.update(dict(('f_' + f, 1) for f in features))
	except:
		traceback.print_exc()
		results['_error'] = 1
		
	return results

if __name__ == '__main__':
	output_file = sys.argv[1]
	assert not os.path.exists(output_file), 'output file %s already exists!' % output_file

	files = []
	for f in sys.argv[2:]:
		if os.path.isfile(f):
			files.append(f)
		elif os.path.isdir(f):
			files.extend(os.listdir(f))

	results = []
	columns = set()
	for f in files:
		r = process_apk(f)
		results.append(r)
		columns.update(r.keys())

	columns = sorted(list(columns))

	# write data into output file
	outf = open(output_file, 'w')
	outf_csv = csv.writer(outf)
	outf_csv.writerow(columns)
	for row in results:
		outf_csv.writerow([row.get(k, '') for k in columns])
	outf.close()

