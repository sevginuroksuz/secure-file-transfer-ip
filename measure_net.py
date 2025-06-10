#!/usr/bin/env python
"""
measure_net.py
--------------
Basit ağ-performansı ölçüm aracı.

• Ping ile ort. RTT
• iperf3 ile gönderim/alış hızları (Mbit/s)
• Sonuçlar results.csv’ye eklenir

Kullanım:
  python measure_net.py 127.0.0.1 -d 10 -l "VPN_50ms_loss5"

Ön Koşullar:
  * iperf3 kurulu
  * Hedef makinede `iperf3 -s` dinliyor
  * (İsteğe bağlı) tc/netem senaryosu ayrı terminalde uygulanabilir
"""

import argparse
import csv
import datetime as dt
import subprocess
import sys
from pathlib import Path
from statistics import mean


def run(cmd: list[str]) -> tuple[int, str]:
    """Komutu çalıştır, (çıkış_kodu, çıktı) döndür."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip()


import re, subprocess, sys

import re, subprocess, sys
from statistics import mean

def measure_ping(host: str, count: int = 20) -> float:
    """
    Dil-bağımsız ortalama RTT (ms). Her satırdaki 'time=' veya 'time<' değerini toplar.
    Windows:  ping -n N
    Unix   :  ping -c N
    """
    flag = "-n" if sys.platform.startswith("win") else "-c"
    proc = subprocess.run(
        ["ping", flag, str(count), host],
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise RuntimeError("ping komutu başarısız (hedef ulaşılamıyor)")
    out = proc.stdout

    # time=23ms  |  time<1ms  |  time=23.5 ms  → hepsini yakalar
    times = [float(m.group(1)) for m in re.finditer(r"time[=<]\s*([\d.]+)", out)]
    if not times:
        raise RuntimeError("RTT değeri yakalanamadı – ping çıktısını paylaşır mısın?")
    return round(mean(times), 2)


def measure_iperf(host: str, duration: int = 10) -> tuple[float, float]:
    """iperf3 ile (sender, receiver) Mbps döndür."""
    code, out = run(["./iperf3.exe" if sys.platform.startswith("win") else "iperf3",
                 "-c", host, "-t", str(duration), "--json"])
    if code != 0:
        raise RuntimeError("iperf3 başarısız (server açık mı?)")
    import json

    j = json.loads(out)
    sender = j["end"]["sum_sent"]["bits_per_second"] / 1e6
    receiver = j["end"]["sum_received"]["bits_per_second"] / 1e6
    return round(sender, 2), round(receiver, 2)


def append_csv(row: dict, csv_path: Path = Path("results.csv")) -> None:
    """Sonuç satırını CSV'ye ekle (başlık yoksa oluştur)."""
    write_header = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ping+iperf3 ölçümü (CSV çıktılı)"
    )
    parser.add_argument("host", help="iperf3 sunucu IP'si / hostname'i")
    parser.add_argument("-d", "--duration", type=int, default=10,
                        help="iperf süresi (s, varsayılan 10)")
    parser.add_argument("-c", "--count", type=int, default=20,
                        help="ping paketi sayısı (varsayılan 20)")
    parser.add_argument("-l", "--label", default="baseline",
                        help="Senaryo etiketi (ör. WiFi_5GHz)")
    args = parser.parse_args()

    print("▶️  Ping ölçülüyor …")
    rtts = [measure_ping(args.host, 1) for _ in range(args.count)]
    avg_rtt = round(mean(rtts), 2)
    print(f"   RTT ≈ {avg_rtt} ms")

    print("▶️  iperf3 ölçülüyor …")
    send_mbps, recv_mbps = measure_iperf(args.host, args.duration)
    print(f"   Gönderim {send_mbps} Mbps | Alış {recv_mbps} Mbps")

    row = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "label": args.label,
        "host": args.host,
        "ping_count": args.count,
        "avg_rtt_ms": avg_rtt,
        "iperf_duration_s": args.duration,
        "send_Mbps": send_mbps,
        "recv_Mbps": recv_mbps,
    }
    append_csv(row)
    print("✅  Sonuçlar results.csv dosyasına eklendi.")


if __name__ == "__main__":
    main()