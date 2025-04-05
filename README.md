# Secure File Transfer over IP

🔐 A secure file transfer system with low-level IP packet manipulation, developed as a semester project for the Computer Networks course.

## 🚀 Features

- AES & RSA encryption for secure transmission
- SHA-256 hashing for integrity verification
- Manual IP header manipulation (TTL, checksum, fragmentation)
- File fragmentation and reassembly
- Network performance analysis (latency, bandwidth, packet loss) using:
  - Wireshark
  - iPerf
  - `tc` (traffic control)
- MITM attack simulation and defense

## 🛠️ Technologies

- Python
- Scapy
- PyCrypto / OpenSSL
- Wireshark, iPerf, tc

## 📦 Setup

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

1. Start the server:
```bash
python server.py
```

2. Start the client:
```bash
python client.py
```

3. Follow the terminal prompts to authenticate and transfer files.

## 📊 Sample Outputs

Packet capture from Wireshark:
> Shows encrypted content and custom IP header fields

Terminal output:
> File transfer logs, encryption verification, and performance metrics

## 📁 Project Structure

```
secure-file-transfer-ip/
├── client.py
├── server.py
├── crypto_utils.py
├── packet_utils.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎓 Developed For

Computer Networks (Spring 2025) – Semester Project
