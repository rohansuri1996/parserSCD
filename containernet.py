#!/usr/bin/python

from mininet.net import Containernet
#from mininet.node import RemoteController
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from parser import foo

setLogLevel('info')
net = Containernet(controller=Controller)
#net = Containernet(controller=RemoteController)
info('*** Adding controller\n')
net.addController('c0' )

info('*** Adding docker containers\n')
access_points = []

json = foo()

port = 5000
mac = 1
for name,ip in zip(list(json.keys()),list(json.values())):

    mac = ":02".format(mac)
    d_temp = net.addDocker(str(name), ip=ip, dimage="container_service1",dcmd="python main.py", ports=[port], port_bindings={port:port},publish_all_ports=True, mac='00:00:00:00:00:'+mac)
    access_points.append(d_temp)
    port+=1
    mac+=1

'''
d2 = net.addDocker('d2', ip='10.0.2.16', dimage="container_service2",dcmd="python main.py", ports=[5001], port_bindings={5001:5001},publish_all_ports=True, mac='00:00:00:00:00:02')
d3 = net.addDocker('d3', ip='10.0.2.17', dimage="container_service3",dcmd="python main.py", ports=[5002], port_bindings={5002:5002},publish_all_ports=True, mac='00:00:00:00:00:03')
d4 = net.addDocker('d4', ip='10.0.2.18', dimage="container_kalicontainer",dcmd="/init", ports=[5900, 6080], port_bindings={5900: 5900, 6080: 6080}, publish_all_ports=True, mac='00:00:00:00:00:04')
'''

info('*** Adding switches\n')
s1 = net.addSwitch('s1')

info('*** Creating links\n')

for each in access_points:
    net.addLink(s1, each, cls=TCLink, delay='100ms', bw=1)

'''net.addLink(s1, d2, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, d3, cls=TCLink, delay='100ms', bw=1)
net.addLink(s1, d4, cls=TCLink, delay='100ms', bw=1)
'''
info('*** Starting network\n')
net.start()
info('*** Testing connectivity\n')
net.ping(access_points)

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()

