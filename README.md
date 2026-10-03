# UDP_ping_application using mininet
## Mininet Resources

- Introduction: https://github.com/safiqul/2410/blob/main/docs/intro/mininet-intro.md
- Creating Topologies: https://github.com/safiqul/2410/blob/main/docs/creating-topologies/mininet-2.md
- Running Your Own Program: https://github.com/safiqul/2410/blob/main/docs/running-your-own-program/mininet-app.md

download all file and store in one single directory.
open terminal on that directory.
now run --> 
```
sudo python3 topology.py
```
it will run mininet automatically.

then inside mininet--> 
```
xterm h1 h2 r1
```
3 terminal will be open

if h2 is your server node run in h2 --> 
```
python3 UDP_server.py
````
if h1 is your client node run in h1 --> 
```
python3 UDP_client.py
```
in middle from any of switch/router collect the data for wireshark --> 
```
sudo tcpdump -i r2-eth0 -tttt -w traces.pcap
```
