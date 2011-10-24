#!/usr/bin/env python

import os
import sys
import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u', '--unmount', action='store_true', dest='unmount', default=False)

(options, args) = parser.parse_args()

if len(args) != 1:
	print 'Missing alias name.'
	exit(0)

alias = args[0]

alias_pattern = re.compile(r'\s*'+alias.lower())
#match_pattern = re.compile(r'\s*(?P<alias>\w+)\s+(?P<remote_path>)')

#file format: <alias> <remote path> <mount point> <options>

for line in open(os.environ['HOME']+'/.fuseconfig'):
	if alias_pattern.match(line.lower()):
		#print alias_pattern, alias, line
		
		pieces = line.split()
		
		if len(pieces) < 3:
			print 'Not enough values: ' + pieces
			
		(alias, remote_path, mount_point) = (pieces[0], pieces[1], pieces[2])
		volname = ''
			
		if len(pieces) > 3:
			optstr = pieces[3]
		else:	
			volname = mount_point.split('/')[-1]
			optstr = '-oauto_cache,reconnect,volname=' + volname
		
		print 'fusing ' + volname + ' <' + alias + '>'

		if not(options.unmount):
			os.system('mkdir -p ' + mount_point)
			os.system('sshfs ' + remote_path + ' ' + mount_point + ' ' + optstr)
			exit(0)
		else:
			os.system('umount ' + mount_point)
			#os.system('rmdir ' + mount_point)
			exit(0)

print 'alias ' + alias + ' not found in ' + os.environ['HOME'] + '/.fuseconfig'
exit(1)
