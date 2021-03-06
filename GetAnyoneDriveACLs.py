#!/usr/bin/env python
"""
# Purpose: For a Google Drive User(s), delete all drive file ACls for files shared with anyone
# Note: This script can use basic GAM: https://github.com/jay0lee/GAM or advanced GAM: https://github.com/taers232c/GAMADV-X
# Usage:
# 1: Get ACLS for all files, if you don't want all users, replace all users with your user selection in the command below
#  $ Basic: gam all users print filelist id title permissions > filelistperms.csv
#  $ Advanced: gam config auto_batch_min 1 redirect csv ./filelistperms.csv multiprocess all users print filelist id title permissions
# 2: From that list of ACLs, output a CSV file with headers "Owner,driveFileId,driveFileTitle,permissionId,role"
#    that lists the driveFileIds and permissionIds for all ACls shared with anyone
#    (n.b., role and title are not used in the next step, they are included for documentation purposes)
#  $ python GetAnyoneDriveACLs.py filelistperms.csv deleteperms.csv
# 3: Inspect deleteperms.csv, verify that it makes sense and then proceed
# 4: Delete the ACLS
#  $ gam csv deleteperms.csv gam user "~Owner" delete drivefileacl "~driveFileId" "~permissionId"
"""

import csv
import re
import sys

id_n_type = re.compile(r"permissions.(\d+).type")

if (len(sys.argv) > 2) and (sys.argv[2] != '-'):
  outputFile = open(sys.argv[2], 'wb')
else:
  outputFile = sys.stdout
outputCSV = csv.DictWriter(outputFile, ['Owner', 'driveFileId', 'driveFileTitle', 'permissionId', 'role'], lineterminator='\n')
outputCSV.writeheader()

if (len(sys.argv) > 1) and (sys.argv[1] != '-'):
  inputFile = open(sys.argv[1], 'rb')
else:
  inputFile = sys.stdin

for row in csv.DictReader(inputFile):
  for k, v in row.iteritems():
    mg = id_n_type.match(k)
    if mg:
      perm_group = mg.group(1)
      if v:
        if row['permissions.{0}.type'.format(perm_group)] == 'anyone':
          outputCSV.writerow({'Owner': row['Owner'],
                              'driveFileId': row['id'],
                              'driveFileTitle': row['title'],
                              'permissionId': 'id:{0}'.format(row['permissions.{0}.id'.format(perm_group)]),
                              'role': row['permissions.{0}.role'.format(perm_group)]})

if inputFile != sys.stdin:
  inputFile.close()
if outputFile != sys.stdout:
  outputFile.close()
