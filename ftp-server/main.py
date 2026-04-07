import sys
import os
from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm
from twisted.python import log

PORT = 2121
PUBLIC_DIR = './public'
USERS_DIR = './myusers'

def directories_exist():
    for directory in [PUBLIC_DIR, USERS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            log.msg(f"Created directory: {directory}")

def main():
    log.startLogging(sys.stdout)

    directories_exist()

    # InMemoryUsernamePasswordDatabaseDontUse is for testing only
    checker = InMemoryUsernamePasswordDatabaseDontUse()
    checker.addUser('someuser', '1234')

    portal = Portal(FTPRealm(PUBLIC_DIR, USERS_DIR), [AllowAnonymousAccess(), checker])
    factory = FTPFactory(portal)

    log.msg(f"Starting FTP server on port {PORT}...")
    try:
        reactor.listenTCP(PORT, factory)
        reactor.run()
    except Exception as e:
        log.err(f"Critical error during server startup: {e}")

if __name__ == '__main__':
    main()