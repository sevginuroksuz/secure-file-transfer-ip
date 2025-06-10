# Secure File Transfer IP

[![Demo Video](https://img.youtube.com/vi/MlyJfbbCGqg/0.jpg)](https://youtu.be/MlyJfbbCGqg?t=4s)

**Secure File Transfer IP**, endüstriyel ve kurumsal ortamlarda güvenli dosya teslimi sağlamak için geliştirilmiş, Python tabanlı bir uygulamadır. Uçtan uca şifreleme, bütünlük kontrolü, MITM senaryoları ve gerçek dünya ağ koşullarında performans ölçümlerini bir araya getirir.

---

## 📑 İçindekiler

1. [Proje Hakkında](#proje-hakkında)  
2. [Özellikler](#özellikler)  
3. [Kullanılan Teknolojiler](#kullanılan-teknolojiler)  
4. [Klasör Yapısı](#klasör-yapısı)  
5. [Kurulum & Çalıştırma](#kurulum--çalıştırma)  
6. [Örnek Kullanım Senaryoları](#örnek-kullanım-senaryoları)  
7. [Performans Raporu](#performans-raporu)  
8. [Dokümantasyon Raporu](#dokümantasyon-raporu)  
9. [Katkıda Bulunanlar](#katkıda-bulunanlar)  
10. [Lisans](#lisans)  
11. [İletişim](#iletişim)  

---

## 🔍 Proje Hakkında

Günümüzde hassas veriler ağ üzerinden aktarılırken hem güvenlik hem de performans kritik. “Secure File Transfer IP”:
- **Gizlilik**: Dosyalar AES-256-CBC ile şifrelenir  
- **Bütünlük**: SHA-256 tabanlı HMAC ile veri bütünlüğü kontrolü  
- **Dayanıklılık Testi**: MITM (Ortadaki Adam) saldırı senaryoları  
- **Performans Ölçümleri**: Ethernet, Wi-Fi, gecikme ve paket kaybı simülasyonları  

---

## ✨ Özellikler

- Uçtan uca şifreleme (AES-256-CBC, RSA-2048)  
- SHA-256 tabanlı bütünlük kontrolü  
- MITM simülasyonu ve paket enjeksiyonu  
- CLI ve GUI (Tkinter) arayüzü  
- Performans ölçümleri (iPerf3, Clumsy senaryoları)  
- Kapsamlı ağ analizi (Wireshark)  
- Esnek konfigürasyon: port, buffer boyutu, şifreleme anahtar uzunluğu vb.  

---

## 🛠️ Kullanılan Teknolojiler

- **Programlama Dili:** Python 3.x  
- **Kullanıcı Arayüzü:** Tkinter (GUI)  
- **Ağ Katmanı:** Python socket programlama (TCP, örnek UDP)  
- **Şifreleme:** PyCryptodome (AES-256-CBC, RSA-2048)  
- **Bütünlük Kontrolü:** hashlib (SHA-256)  
- **Ağ Analizi/Test:** iPerf3, Wireshark, Clumsy  
- **Düşük Seviyeli Paket İşleme:** Scapy  
- **İşletim Sistemi:** Windows 10 (testler için zaman zaman Linux)  
- **Ek Kütüphaneler:** threading, datetime, os, pandas, matplotlib  

---

## 📁 Klasör Yapısı

```
secure-file-transfer-ip/
├── client/
│   ├── client_cli.py
│   ├── client_gui.py
│   ├── protocol.py
│   └── __init__.py
├── docs/
│   └── ProjeDokumantasyonRaporu.pdf
├── examples/
├── server.py
├── mitm.py
├── measure_net.py
├── graph.py
├── requirements.txt
└── README.md
```

---

## 🚀 Kurulum & Çalıştırma

1. **Depoyu klonla**  
   ```bash
   git clone https://github.com/sevginuroksuz/secure-file-transfer-ip.git
   cd secure-file-transfer-ip
   ```
2. **Sanal ortam oluştur & etkinleştir**  
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat    # Windows
   source venv/bin/activate       # macOS/Linux
   ```
3. **Bağımlılıkları yükle**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Sunucuyu başlat**  
   ```bash
   python server.py --port 9000
   ```
5. **Client ile dosya gönder**  
   - **CLI:**  
     ```bash
     python client/client_cli.py --host 127.0.0.1 --port 9000 --file örnek.txt
     ```
   - **GUI:**  
     ```bash
     python client/client_gui.py
     ```

---

## 🎯 Örnek Kullanım Senaryoları

- **Ethernet**  
- **Loss=5%, Delay=50 ms** (WAN simulasyonu)  
- **Wi-Fi (5 GHz)**  

Senaryo sonrası otomatik raporlama ve grafik:  
```bash
python measure_net.py --scenario loss5_delay50
python graph.py --input results.csv --output performance.png
```

---

## 📊 Performans Raporu

| Senaryo               | Gönderme (Mbps) | Alma (Mbps) |
|-----------------------|-----------------|-------------|
| Ethernet              | 6452.42         | 6452.10     |
| Loss=5%, Delay=50 ms  | 4540.70         | 4540.55     |
| Wi-Fi (5 GHz)         | 1373.23         | 1373.13     |

---

## 📚 Dokümantasyon Raporu

Detaylı tasarım, mimari ve test sonuçlarını içeren PDF rapor:  
[docs/proje-dokumantasyon-raporu.pdf](docs/proje-dokumantasyon-raporu.pdf)

---

## 🤝 Katkıda Bulunanlar

- Sevgi Nur Öksüz  

---

## 📄 Lisans

MIT Lisansı — detaylar için [LICENSE](LICENSE)

---

## 📬 İletişim

- **GitHub:** https://github.com/sevginuroksuz/secure-file-transfer-ip  
- **YouTube Demo:** https://youtu.be/MlyJfbbCGqg?t=4s  
