from scapy.all import *
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
from scapy.layers.netflow import NetflowHeader, NetflowHeaderV5, NetflowRecordV5

"""
IPField("src", "127.0.0.1"),
                   IPField("dst", "127.0.0.1"),
                   IPField("nexthop", "0.0.0.0"),
                   ShortField("input", 0),
                   ShortField("output", 0),
                   IntField("dpkts", 1),
                   IntField("dOctets", 60),
                   IntField("first", 0),
                   IntField("last", 0),
                   ShortField("srcport", 0),
                   ShortField("dstport", 0),
                   ByteField("pad1", 0),
                   FlagsField("tcpFlags", 0x2, 8, "FSRPAUEC"),
                   ByteEnumField("prot", socket.IPPROTO_TCP, IP_PROTOS),
                   ByteField("tos", 0),
                   ShortField("src_as", 0),
                   ShortField("dst_as", 0),
                   ByteField("src_mask", 0),
                   ByteField("dst_mask", 0),
                   ShortField("pad2", 0)]
"""

netflow = NetflowHeader()/NetflowHeaderV5(count=1)/NetflowRecordV5(dst="192.168.250.250",
                                                                   nexthop="192.168.250.1",
                                                                   input=1,
                                                                   output=2,
                                                                   dpkts=111,
                                                                   dOctets=222,
                                                                   first=0,
                                                                   last=0,
                                                                   srcport=6000,
                                                                   dstport=443,
                                                                   tcpFlags=1,
                                                                   prot=6)
pkt = Ether()/IP(dst="192.168.2.109", src="192.168.2.109")/UDP(sport=2055, dport=2055)/netflow

pkt.show()

sendp(pkt, iface='en0')