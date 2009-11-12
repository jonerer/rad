import sys
import chilkat

sshTunnel = chilkat.CkSshTunnel()

success = sshTunnel.UnlockComponent("30-day trial")
if (success != True):
    print sshTunnel.lastErrorText()
    sys.exit()

#  The destination host/port is the database server.
#  The DestHostname may be the domain name or
#  IP address (in dotted decimal notation) of the database
#  server.
sshTunnel.put_DestPort(1433)
sshTunnel.put_DestHostname("myDbServer.com")

#  Provide information about the location of the SSH server,
#  and the authentication to be used with it. This is the
#  login information for the SSH server (not the database server).
sshTunnel.put_SshHostname("192.168.1.108")
sshTunnel.put_SshPort(22)
sshTunnel.put_SshLogin("mySshLogin")
sshTunnel.put_SshPassword("mySshPassword")

#  Start accepting connections in a background thread.
#  The SSH tunnels are autonomously run in a background
#  thread.  There is one background thread for accepting
#  connections, and another for managing the tunnel pool.
listenPort = 3316
success = sshTunnel.BeginAccepting(listenPort)
if (success != True):
    print sshTunnel.lastErrorText()
    sys.exit()

#  At this point you may connect to the database server through
#  the SSH tunnel.  Your database connection string would
#  use "localhost" for the hostname and 3316 for the port.
#  We're not going to show the database coding here,
#  because it can vary depending on the API you're using
#  (ADO, ODBC, OLE DB, etc. )

#  This is where your database code would go...

#  When you're finished with the database connection, you may
#  stop the background tunnel threads:
#  Stop the background thread that accepts new connections:
success = sshTunnel.StopAccepting()
if (success != True):
    print sshTunnel.lastErrorText()
    sys.exit()

#  If any background tunnels are still in existence (and managed
#  by a single SSH tunnel pool background thread), stop them...
maxWaitMs = 1000
success = sshTunnel.StopAllTunnels(maxWaitMs)
if (success != True):
    print sshTunnel.lastErrorText()
    sys.exit()

