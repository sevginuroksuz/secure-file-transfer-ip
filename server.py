import socket
import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import unpad

RSA_KEYPAIR = RSA.generate(2048)
PUBLIC_PEM = RSA_KEYPAIR.publickey().export_key()

USERS = {"admin": "1234", "user": "4321"}


def recv_exact(sock: socket.socket, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Beklenmedik bağlantı kopması")
        buf += chunk
    return buf


def start_server(host: str = "0.0.0.0", port: int = 5001) -> None:
    server = socket.socket()
    server.bind((host, port))
    server.listen(1)
    print(f"Sunucu dinliyor… ({host}:{port})")

    while True:
        conn, addr = server.accept()
        print(f"{addr} bağlandı.")

        try:
            # RSA handshake
            conn.sendall(len(PUBLIC_PEM).to_bytes(4, "big") + PUBLIC_PEM)
            enc_key = recv_exact(conn, 256)
            session_key = PKCS1_OAEP.new(RSA_KEYPAIR).decrypt(enc_key)

            # Kimlik doğrulama
            username = recv_exact(conn, 64).rstrip(b"\0").decode()
            password = recv_exact(conn, 64).rstrip(b"\0").decode()
            if USERS.get(username) != password:
                print(f"Yetkisiz giriş: {username}")
                conn.send(b"NO")
                conn.close()
                continue
            conn.send(b"OK")

            # Dosya adı + IV
            filename = recv_exact(conn, 128).rstrip(b"\0").decode()
            iv = recv_exact(conn, 16)
            cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)

            # --- Resume özelliği için mevcut dosya boyutu belirleniyor ---
            out_path = f"received_{filename}"
            if os.path.exists(out_path):
                current_size = os.path.getsize(out_path)
            else:
                current_size = 0
            conn.sendall(current_size.to_bytes(8, "big"))

            # --- Kalan şifreli veriyi alıp dosyaya ekle ---
            enc_data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                enc_data += chunk

            # Bu örnekte hash ve dosya, daha önceki gibi son blok olarak ayrılıyor:
            HASH_BLOCK = AES.block_size * 3  # 48 B (32 B hash + 16 B padding)
            if len(enc_data) < HASH_BLOCK + AES.block_size:
                print("Yetersiz veri — hash bloğu yok")
                conn.close()
                continue

            enc_tag = enc_data[-HASH_BLOCK:]
            enc_file = enc_data[:-HASH_BLOCK]

            # Kalan dosyayı çöz-pad
            try:
                file_bytes = unpad(cipher_aes.decrypt(enc_file), AES.block_size)
            except ValueError:
                print("Şifre çözüm/padding hatası")
                conn.close()
                continue

            # Var olan dosyayı "append" ile tamamla
            with open(out_path, "ab") as f:
                f.write(file_bytes)

            # Hash bloğunu çöz-pad
            try:
                tag_plain = unpad(cipher_aes.decrypt(enc_tag), AES.block_size)
            except ValueError:
                print("Hash bloğu çözülemedi")
                conn.close()
                continue

            # SHA-256 ile bütünlük kontrolü
            with open(out_path, "rb") as f:
                all_bytes = f.read()
            if hashlib.sha256(all_bytes).digest() != tag_plain:
                print("Integrity FAIL – SHA-256 eşleşmedi")
                conn.close()
                continue

            print(f"Dosya başarıyla alındı ✔  → {out_path}")

        except Exception as e:
            print(f"Hata oluştu: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    start_server()
