from scapy.all import IP, TCP

ip = IP(
    src="192.168.1.101",
    dst="192.168.1.1",
    ttl=44,
    flags="DF",
    id=1234,
    frag=0
)
tcp = TCP(sport=4444, dport=80, flags="S", seq=123456)
pkt = ip / tcp

# Paketi build ettirip yeniden parse ettiriyoruz
pkt = pkt.__class__(bytes(pkt))  # Bu satırdan sonra tüm otomatik alanlar (chksum dahil) kesinlikle dolu olur

# Scapy checksum'u
print("Scapy'nin hesapladığı checksum:", hex(pkt[IP].chksum))

# Header'ı al
header_bytes = bytes(pkt)[:20]

# Elle hesaplamak için checksum alanını sıfırla
header_bytes_for_manual = bytearray(header_bytes)
header_bytes_for_manual[10] = 0
header_bytes_for_manual[11] = 0


def ip_checksum(header_bytes):
    s = 0
    for i in range(0, len(header_bytes), 2):
        w = (header_bytes[i] << 8) + (header_bytes[i+1])
        s = s + w
    s = (s >> 16) + (s & 0xffff)
    s = ~s & 0xffff
    return s

chksum = ip_checksum(header_bytes_for_manual)
print(f"Elle hesaplanan checksum: {hex(chksum)}")
