#!/usr/bin/env python

import sys
import xmlrpclib

login_default='';
domain_default='';
apikey_prod='';

if len(sys.argv) < 2:
        print "Usage: %s alias login(default = %s) domain(default = %s)" % (sys.argv[0],login_default,domain_default);
        exit();

if len(sys.argv) == 2:
        login=login_default;
        domain=domain_default;
elif len(sys.argv) == 3:
        login=sys.argv[2];
        domain=domain_default;
else:
        login=sys.argv[2];
        domain=sys.argv[3];

alias=sys.argv[1];

api=xmlrpclib.ServerProxy("https://rpc.gandi.net/xmlrpc/");

aliases=api.domain.mailbox.info(apikey_prod,domain,login)['aliases'];
if alias in aliases:
        print 'Alias already present';
        exit();

aliases+=[alias];
aliases.sort();
api.domain.mailbox.alias.set(apikey_prod,domain,login,aliases);

