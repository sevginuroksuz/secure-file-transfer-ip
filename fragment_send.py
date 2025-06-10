#!/usr/bin/env python
# fragment_send.py
"""
Scapy ile IP Fragmentasyonu Örneği
• Dosyayı 1480 B payload’lı paketlere böl
• Her pakete MF bayrağı ve offset uygula
• Checksum=0 bırak, Scapy yeniden hesaplasın
• En son pakette MF=0
"""

from scapy.all import IP, UDP, Raw, send
import os


def fragment_and_send(
    file_path: str,
    dst_ip: str,
    dst_port: int = 5001,
    mtu: int = 1500
):
    # IP başlığı + UDP başlığı toplam 20 + 8 = 28 B, 
    # payload = mtu - 28 = 1472 B (bize 1480'lik yuvarlak kısım uygundu)
    frag_size = mtu - 28

    with open(file_path, "rb") as f:
        data = f.read()

    total_len = len(data)
    offset = 0

    while offset < total_len:
        chunk = data[offset:offset+frag_size]
        # MF bayrağı: eğer bu son paket değilse 1, son paketse 0
        mf_flag = 1 if (offset + frag_size) < total_len else 0

        pkt = (
            IP(dst=dst_ip, flags=mf_flag, frag=(offset // 8), chksum=0)
            / UDP(dport=dst_port, sport=40000)
            / Raw(chunk)
        )
        # Scapy checksum yeniden hesaplansın
        del pkt[IP].chksum
        send(pkt, verbose=False)
        print(f"Sent fragment offset={offset//8}, size={len(chunk)}, MF={mf_flag}")
        offset += frag_size


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(
        description="Scapy ile IP fragmentasyon testi"
    )
    p.add_argument("file", help="Gönderilecek dosya")
    p.add_argument("dst",  help="Hedef IP")
    p.add_argument("-p", "--port", type=int, default=5001,
                   help="Hedef UDP port")
    p.add_argument("--mtu", type=int, default=1500,
                   help="MTU boyutu (vars:1500)")
    args = p.parse_args()

    fragment_and_send(args.file, args.dst, args.port, args.mtu)
