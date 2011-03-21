#!/usr/bin/env python
# GPL
# Pablo

class RouterModelBase:

    def login(user, passw):
        raise NotImplemented

    def logout():
        raise NotImplemented

    def guess():
        raise NotImplemented

    def getClientsList():
        raise NotImplemented

    def forwardPort():
        raise NotImplemented

    def protocolsSupported():
        raise NotImplemented

