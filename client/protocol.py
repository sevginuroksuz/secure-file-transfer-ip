import os
import socket
import hashlib
from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes


def _recv_exact(sock: socket.socket, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Bağlantı koptu")
        data += chunk
    return data


def _rsa_handshake(sock: socket.socket) -> Tuple[AES, bytes]:
    pem_len = int.from_bytes(_recv_exact(sock, 4), "big")
    server_pub = RSA.import_key(_recv_exact(sock, pem_len))
    session_key = get_random_bytes(32)
    enc_key = PKCS1_OAEP.new(server_pub).encrypt(session_key)
    sock.sendall(enc_key)
    iv = get_random_bytes(16)
    cipher = AES.new(session_key, AES.MODE_CBC, iv)
    return cipher, iv


def secure_send(
    file_path: str,
    username: str,
    password: str,
    server_ip: str = "127.0.0.1",
    port: int = 5001,
    progress_callback=None
) -> None:
    with socket.socket() as s:
        s.connect((server_ip, port))
        cipher, iv = _rsa_handshake(s)
        s.sendall(username.encode().ljust(64, b"\0"))
        s.sendall(password.encode().ljust(64, b"\0"))
        if _recv_exact(s, 2) != b"OK":
            raise PermissionError("Kimlik doğrulama başarısız!")

        filename = os.path.basename(file_path)
        s.sendall(filename.encode().ljust(128, b"\0"))
        s.sendall(iv)

        # --- Resume için sunucudan mevcut offseti al ---
        offset = int.from_bytes(s.recv(8), "big")

        with open(file_path, "rb") as f:
            raw_data = f.read()
        tag = hashlib.sha256(raw_data).digest()
        padded_file = pad(raw_data, AES.block_size)
        enc_file = cipher.encrypt(padded_file)
        enc_tag = cipher.encrypt(pad(tag, AES.block_size))

        # --- Yalnızca kalan kısmı gönder (resume logic) ---
        total = len(enc_file)
        sent = offset
        chunk_size = 4096

        if offset >= total:
            # Zaten dosya tam olarak gönderilmiş
            if progress_callback:
                progress_callback(1.0)
            return

        for i in range(offset, total, chunk_size):
            s.sendall(enc_file[i:i+chunk_size])
            sent += min(chunk_size, total - i)
            if progress_callback:
                progress_callback(sent / total)
        s.sendall(enc_tag)
        if progress_callback:
            progress_callback(1.0)
