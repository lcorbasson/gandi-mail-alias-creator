#!/usr/bin/env python

import sys
import xmlrpclib
import json

with open('settings.json', 'r') as settings_file:
        settings=json.load(settings_file);

mailbox_default=settings['mailbox_default'];
domain_default=settings['domain_default'];
apikey_prod=settings['apikey_prod'];

if len(sys.argv) < 2:
        print "Usage: %s alias login(default = %s) domain(default = %s)" % (sys.argv[0],login_default,domain_default);
        exit();

if len(sys.argv) == 2:
        mailbox=mailbox_default;
        domain=domain_default;
elif len(sys.argv) == 3:
        mailbox=sys.argv[2];
        domain=domain_default;
else:
        mailbox=sys.argv[2];
        domain=sys.argv[3];

alias=sys.argv[1];

api=xmlrpclib.ServerProxy("https://rpc.gandi.net/xmlrpc/");

aliases=api.domain.mailbox.info(apikey_prod,domain,mailbox)['aliases'];
if alias in aliases:
        print 'Alias already present';
        exit();

aliases+=[alias];
aliases.sort();
api.domain.mailbox.alias.set(apikey_prod,domain,mailbox,aliases);

