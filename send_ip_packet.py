from scapy.all import IP, TCP, send

ip = IP(
    src="127.0.0.1",
    dst="127.0.0.1",
    ttl=44,
    flags="DF",
    id=1234,
    frag=0
)
tcp = TCP(
    sport=4444,
    dport=80,
    flags="S",
    seq=123456
)
pkt = ip / tcp
send(pkt, verbose=True)
pkt.show()
