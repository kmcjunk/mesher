# mesher
Script used to troubleshoot networking issues on an OS level. The idea is
fairly simple. Run a 5 count ping to all IPs/hostnames specified in hlist
(line 16), if ping returns a non zero (timeout / packetloss) then it will
create a dictionary of useful debugging information and then create a 90
second capture on the problem interface.

The goal of this project is to gather evidence of small, intermittent networking
issues. It is fairly sensitive in nature due to the fact that if even one packet
gets dropped, it will start diagnosing.

## Known Issues
The script will create a process for every hostname/IP in hlist. There are three
notable issues with this logic. The first being, if you throw a /8 into it,
you're not gonna have a good time. The second and larger issue is that since
it utilizes multiprocessing instead of multithreading - if one host detects
packet loss, the rest of your host will need to wait on that I/O operation
until they can start pinging again. :) It's 90 seconds, I should have threaded,
I messed up, forgive pls. In my head this isn't
a game breaking issue as the pings stop *during* the capture. Meaning that if you
load into wireshark, you still see the larger picture of network failure. The
biggest downside is that the source server running the script is no longer
pinging outbound. The third issue is that it was wrote for CentOS 6, so it was
designed with python 2 in mind. It works on python3, but man...redhat really
messed up w/ this whole bury & ruin centos thing.
