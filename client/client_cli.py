import argparse, client.protocol as protocol

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Güvenli dosya gönderici (CLI)")
    ap.add_argument("file", help="Gönderilecek dosya")
    ap.add_argument("-u", "--user", required=True, help="Kullanıcı adı")
    ap.add_argument("-p", "--password", required=True, help="Şifre")
    ap.add_argument("--host", default="127.0.0.1", help="Sunucu IP")
    ap.add_argument("--port", type=int, default=5001, help="Sunucu portu")
    args = ap.parse_args()

    protocol.secure_send(
        file_path=args.file,
        username=args.user,
        password=args.password,
        server_ip=args.host,
        port=args.port,
    )
    print("✔ Dosya gönderildi")
