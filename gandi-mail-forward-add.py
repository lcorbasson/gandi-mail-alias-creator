#!/usr/bin/env python
# TODO:
# - check for each destination if it already exists in the list

from __future__ import print_function
import sys
import xmlrpclib
import json

with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

destinations_default = settings['destinations_default']
domain_default = settings['domain_default']
apikey_prod = settings['apikey_prod']

if len(sys.argv) < 2:
        print("Usage: ", sys.argv[0], " redir dest(default = ", destinations_default, ") domain(default = ", domain_default, ")")
        exit()

if len(sys.argv) == 2:
        dest = destinations_default
        domain = domain_default
elif len(sys.argv) == 3:
        dest = sys.argv[2]
        domain = domain_default
else:
        dest = sys.argv[2]
        domain = sys.argv[3]

if not isinstance(dest, list):
	dest = [dest]

redir = sys.argv[1]

api = xmlrpclib.ServerProxy("https://rpc.gandi.net/xmlrpc/")

new_redir = False
destinations = api.domain.forward.list(apikey_prod, domain, {'source': redir})
if len(destinations) == 0:
	new_redir = True
if dest in destinations:
        print('Destination already present', file=sys.stderr)
        exit()

destinations += dest
destinations.sort()
if new_redir:
	api.domain.forward.create(apikey_prod, domain, redir, {'destinations': destinations})
else:	
	api.domain.forward.update(apikey_prod, domain, redir, {'destinations': destinations})
