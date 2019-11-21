from mininet.log import setLogLevel
from mininet.node import UserSwitch, OVSKernelSwitch # , KernelSwitch
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os

def topos():
	os.system('mn -c')
	net = Mininet(link=TCLink, host=CPULimitedHost)

	#Add Host
	h1 = net.addHost('server', mac='00:00:00:00:00:01', ip='192.168.1.2/24')
	h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='192.168.2.3/24')
	#addrouter
	r1 = net.addHost('r1', ip='192.168.1.1/24')
	#add link
	net.addLink(r1,h1, bw=2, max_queue_size=100)
	net.addLink(r1,h2, bw=1000, max_queue_size=100)
	net.build()
	#Build interface
	r1.cmd("ifconfig r1-eth0 0") #diset 0 maka remove ip address
	r1.cmd("ifconfig r1-eth1 0") #diset 0 maka remove ip address
	#Assign mac address
	r1.cmd("ifconfig r1-eth0 hw ether 00:00:00:00:00:01")
	r1.cmd("ifconfig r1-eth1 hw ether 00:00:00:00:00:02")
	#Assign IP Address
	r1.cmd("ip addr add 192.168.1.1/24 brd + dev r1-eth0")
	r1.cmd("ip addr add 192.168.2.1/24 brd + dev r1-eth1")
	r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
	#Assign Default Reoute
	h1.cmd("ip route add default via 192.168.1.1")
	h2.cmd("ip route add default via 192.168.2.1")
	#set congestion control
	os.system('sysctl -w net.ipv4.tcp_congestion_control=cubic')
	#starting program
	print("--Start Mininet--")
	CLI(net)
	print("--Mininet Stopped--")
	net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topos()	
