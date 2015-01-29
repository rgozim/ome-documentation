#!/usr/bin/env bash
# This script is used by a Continuous Integration job to auto-generate
# some components of the OMERO documentation from its deliverables (server,
# clients). To run it locally, download the server and the linux clients
# containing the importer-cli and name them OMERO.server and OMERO.clients.

set -u
set -e
set -x
WORKSPACE=${WORKSPACE:-$(pwd)}

echo "Copying history"
cp $WORKSPACE/OMERO.server/history.txt omero/users/

echo "Generating configuration properties page"
$WORKSPACE/OMERO.server/bin/omero config parse --rst | sed "s|$WORKSPACE|/home/omero|" > omero/sysadmins/config.txt

echo "Generating ldap setdn usage page"
mkdir -p omero/downloads/ldap
$WORKSPACE/OMERO.server/bin/omero ldap setdn -h | sed "s|$WORKSPACE|/home/omero|" > omero/downloads/ldap/setdn.out

echo "Generating advanced CLI help"
$WORKSPACE/OMERO.server/bin/omero import --advanced-help 2> advanced-help.txt || echo "Dumped"
sed 1,3d advanced-help.txt > omero/downloads/inplace/advanced-help.txt
$WORKSPACE/OMERO.clients/importer-cli -h 2> omero/downloads/cli/help.out || echo "Dumped"

echo "Generating Web configuration templates"
$WORKSPACE/OMERO.server/bin/omero web config nginx | sed "s|$WORKSPACE|/home/omero|" > omero/sysadmins/unix/nginx-omero.conf
$WORKSPACE/OMERO.server/bin/omero web config apache | sed "s|$WORKSPACE|/home/omero|" > omero/sysadmins/unix/apache-omero.conf
$WORKSPACE/OMERO.server/bin/omero web config apache-fcgi | sed "s|$WORKSPACE|/home/omero|" > omero/sysadmins/unix/apache-fcgi-omero.conf

echo "Cleanup"
rm advanced-help.txt
