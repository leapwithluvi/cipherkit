#!/usr/bin/env 
"""
╔═══════════════════════════════════════════════════════════╗
║           CTF CRYPTOGRAPHY TOOLKIT - @leapwithluvi        ║
║         Encode & Decode Tool untuk Persiapan Lomba        ║
╚═══════════════════════════════════════════════════════════╝
Dibuat untuk persiapan lomba CTF - Offline, no internet needed!

Cara pakai:
  python3 crypto_ctf.py                    → Menu interaktif
  python3 crypto_ctf.py --list             → Tampilkan semua cipher
  python3 crypto_ctf.py -c caesar -e "Hello" --shift 3
  python3 crypto_ctf.py -c base64 -d "SGVsbG8="
"""

import sys
import argparse
import base64
import codecs
import string
# import binascii
# import struct
import math
# from itertools import cycle


# ═══════════════════════════════════════════════════════════
# WARNA TERMINAL (ANSI)
# ═══════════════════════════════════════════════════════════
class C:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'

def banner():
    print(f"""
{C.CYAN}{C.BOLD}
 ██████╗████████╗███████╗     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
██╔════╝╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║        ██║   █████╗      ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║        ██║   ██╔══╝      ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗   ██║   ██║         ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝   ╚═╝   ╚═╝          ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
{C.RESET}{C.YELLOW}                    CTF Cryptography Toolkit - @leapwithluvi {C.RESET}
{C.DIM}                     Offline · No Internet · Always Ready{C.RESET}
""")

def ok(msg):    print(f"{C.GREEN}[+]{C.RESET} {msg}")
def err(msg):   print(f"{C.RED}[-]{C.RESET} {msg}")
def info(msg):  print(f"{C.CYAN}[*]{C.RESET} {msg}")
def warn(msg):  print(f"{C.YELLOW}[!]{C.RESET} {msg}")
def result(msg):print(f"\n{C.BOLD}{C.GREENs}══ RESULT ══{C.RESET}\n{C.WHITE}{msg}{C.RESET}\n")


# ═══════════════════════════════════════════════════════════
# 1. CAESAR CIPHER
# ═══════════════════════════════════════════════════════════
def caesar_encode(text, shift=3):
    result_str = ""
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result_str += chr((ord(ch) - base + shift) % 26 + base)
        else:
            result_str += ch
    return result_str

def caesar_decode(text, shift=3):
    return caesar_encode(text, -shift)

def caesar_bruteforce(text):
    print(f"{C.YELLOW}[Brute Force Caesar]{C.RESET}")
    for s in range(1, 26):
        decoded = caesar_decode(text, s)
        print(f"  Shift {s:2d}: {decoded}")


# ═══════════════════════════════════════════════════════════
# 2. ROT13
# ═══════════════════════════════════════════════════════════
def rot13_encode(text):
    return codecs.encode(text, 'rot_13')

def rot13_decode(text):
    return codecs.encode(text, 'rot_13')  # ROT13 adalah kebalikannya sendiri


# ═══════════════════════════════════════════════════════════
# 3. ROT47
# ═══════════════════════════════════════════════════════════
def rot47(text):
    result_str = ""
    for ch in text:
        code = ord(ch)
        if 33 <= code <= 126:
            result_str += chr(33 + (code - 33 + 47) % 94)
        else:
            result_str += ch
    return result_str


# ═══════════════════════════════════════════════════════════
# 4. ATBASH CIPHER
# ═══════════════════════════════════════════════════════════
def atbash(text):
    result_str = ""
    for ch in text:
        if ch.isalpha():
            if ch.isupper():
                result_str += chr(90 - (ord(ch) - 65))
            else:
                result_str += chr(122 - (ord(ch) - 97))
        else:
            result_str += ch
    return result_str


# ═══════════════════════════════════════════════════════════
# 5. BASE64
# ═══════════════════════════════════════════════════════════
def base64_encode(text):
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    # Tambah padding jika kurang
    missing = len(text) % 4
    if missing:
        text += '=' * (4 - missing)
    return base64.b64decode(text).decode(errors='replace')


# ═══════════════════════════════════════════════════════════
# 6. BASE32
# ═══════════════════════════════════════════════════════════
def base32_encode(text):
    return base64.b32encode(text.encode()).decode()

def base32_decode(text):
    missing = len(text) % 8
    if missing:
        text += '=' * (8 - missing)
    return base64.b32decode(text).decode(errors='replace')


# ═══════════════════════════════════════════════════════════
# 7. BASE16 / HEX
# ═══════════════════════════════════════════════════════════
def base16_encode(text):
    return base64.b16encode(text.encode()).decode()

def base16_decode(text):
    text = text.replace(' ', '').replace('0x', '').replace('\\x', '')
    return base64.b16decode(text.upper()).decode(errors='replace')

def hex_encode(text):
    return text.encode().hex()

def hex_decode(text):
    text = text.replace(' ', '').replace('0x', '').replace('\\x', '')
    return bytes.fromhex(text).decode(errors='replace')


# ═══════════════════════════════════════════════════════════
# 8. BINARY
# ═══════════════════════════════════════════════════════════
def binary_encode(text):
    return ' '.join(format(ord(c), '08b') for c in text)

def binary_decode(text):
    text = text.replace(' ', '')
    # Bagi per 8 bit
    chars = [text[i:i+8] for i in range(0, len(text), 8)]
    return ''.join(chr(int(b, 2)) for b in chars if b)


# ═══════════════════════════════════════════════════════════
# 9. OCTAL
# ═══════════════════════════════════════════════════════════
def octal_encode(text):
    return ' '.join(format(ord(c), 'o') for c in text)

def octal_decode(text):
    parts = text.split()
    return ''.join(chr(int(p, 8)) for p in parts)


# ═══════════════════════════════════════════════════════════
# 10. DECIMAL / ASCII
# ═══════════════════════════════════════════════════════════
def decimal_encode(text):
    return ' '.join(str(ord(c)) for c in text)

def decimal_decode(text):
    parts = text.split()
    return ''.join(chr(int(p)) for p in parts)


# ═══════════════════════════════════════════════════════════
# 11. MORSE CODE
# ═══════════════════════════════════════════════════════════
MORSE = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',
    'E': '.',    'F': '..-.', 'G': '--.',  'H': '....',
    'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',  'P': '.--.',
    'Q': '--.-', 'R': '.-.',  'S': '...',  'T': '-',
    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.',
    '!': '-.-.--', '/': '-..-.', '(': '-.--.',  ')': '-.--.-',
    '&': '.-...', ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-', '"': '.-..-.',
    '$': '...-..-', '@': '.--.-.', ' ': '/'
}
MORSE_REV = {v: k for k, v in MORSE.items()}

def morse_encode(text):
    result_chars = []
    for ch in text.upper():
        if ch in MORSE:
            result_chars.append(MORSE[ch])
        else:
            result_chars.append('?')
    return ' '.join(result_chars)

def morse_decode(text):
    parts = text.strip().split(' ')
    result_chars = []
    for p in parts:
        if p == '/':
            result_chars.append(' ')
        elif p in MORSE_REV:
            result_chars.append(MORSE_REV[p])
        elif p:
            result_chars.append(f'[{p}?]')
    return ''.join(result_chars)


# ═══════════════════════════════════════════════════════════
# 12. VIGENERE CIPHER
# ═══════════════════════════════════════════════════════════
def vigenere_encode(text, key):
    key = key.upper()
    result_str = []
    k_idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[k_idx % len(key)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            result_str.append(chr((ord(ch) - base + shift) % 26 + base))
            k_idx += 1
        else:
            result_str.append(ch)
    return ''.join(result_str)

def vigenere_decode(text, key):
    key = key.upper()
    result_str = []
    k_idx = 0
    for ch in text:
        if ch.isalpha():
            shift = ord(key[k_idx % len(key)]) - ord('A')
            base = ord('A') if ch.isupper() else ord('a')
            result_str.append(chr((ord(ch) - base - shift) % 26 + base))
            k_idx += 1
        else:
            result_str.append(ch)
    return ''.join(result_str)


# ═══════════════════════════════════════════════════════════
# 13. XOR CIPHER
# ═══════════════════════════════════════════════════════════
def xor_encode(text, key):
    if isinstance(key, str):
        # Key string → XOR berputar
        result_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
        return result_bytes.hex()
    elif isinstance(key, int):
        result_bytes = bytes([ord(c) ^ key for c in text])
        return result_bytes.hex()

def xor_decode(hex_text, key):
    try:
        data = bytes.fromhex(hex_text.replace(' ', ''))
    except:
        data = hex_text.encode()
    if isinstance(key, str):
        result_bytes = bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])
    else:
        result_bytes = bytes([b ^ key for b in data])
    return result_bytes.decode(errors='replace')

def xor_bruteforce(hex_text):
    """Brute force XOR single byte key"""
    try:
        data = bytes.fromhex(hex_text.replace(' ', ''))
    except:
        data = hex_text.encode()
    print(f"{C.YELLOW}[Brute Force XOR Single Byte]{C.RESET}")
    for k in range(256):
        dec = bytes([b ^ k for b in data])
        try:
            decoded = dec.decode('utf-8')
            # Cek apakah mostly printable
            printable = sum(1 for c in decoded if c.isprintable())
            if printable / len(decoded) > 0.8:
                print(f"  Key 0x{k:02x} ({k:3d}): {decoded}")
        except:
            pass


# ═══════════════════════════════════════════════════════════
# 14. URL ENCODING
# ═══════════════════════════════════════════════════════════
def url_encode(text):
    from urllib.parse import quote
    return quote(text, safe='')

def url_decode(text):
    from urllib.parse import unquote
    return unquote(text)


# ═══════════════════════════════════════════════════════════
# 15. HTML ENTITY ENCODING
# ═══════════════════════════════════════════════════════════
def html_encode(text):
    import html
    return html.escape(text)

def html_decode(text):
    import html
    return html.unescape(text)


# ═══════════════════════════════════════════════════════════
# 16. SUBSTITUTION / AFFINE
# ═══════════════════════════════════════════════════════════
def affine_encode(text, a=5, b=8):
    """Affine cipher: E(x) = (ax + b) mod 26"""
    result_str = []
    for ch in text:
        if ch.isalpha():
            x = ord(ch.upper()) - ord('A')
            enc = (a * x + b) % 26
            new_ch = chr(enc + ord('A'))
            result_str.append(new_ch if ch.isupper() else new_ch.lower())
        else:
            result_str.append(ch)
    return ''.join(result_str)

def affine_decode(text, a=5, b=8):
    """Affine cipher: D(x) = a^-1 * (x - b) mod 26"""
    # Cari modular inverse dari a
    a_inv = None
    for i in range(26):
        if (a * i) % 26 == 1:
            a_inv = i
            break
    if a_inv is None:
        raise ValueError(f"'a'={a} tidak memiliki inverse mod 26! a harus coprime dengan 26.")
    result_str = []
    for ch in text:
        if ch.isalpha():
            x = ord(ch.upper()) - ord('A')
            dec = (a_inv * (x - b)) % 26
            new_ch = chr(dec + ord('A'))
            result_str.append(new_ch if ch.isupper() else new_ch.lower())
        else:
            result_str.append(ch)
    return ''.join(result_str)


# ═══════════════════════════════════════════════════════════
# 17. RAILFENCE CIPHER
# ═══════════════════════════════════════════════════════════
def railfence_encode(text, rails=3):
    fence = [[] for _ in range(rails)]
    rail, direction = 0, 1
    for ch in text:
        fence[rail].append(ch)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    return ''.join(''.join(r) for r in fence)

def railfence_decode(text, rails=3):
    n = len(text)
    pattern = []
    rail, direction = 0, 1
    for i in range(n):
        pattern.append(rail)
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
        rail += direction
    indices = sorted(range(n), key=lambda i: pattern[i])
    result_arr = [''] * n
    for i, idx in enumerate(indices):
        result_arr[idx] = text[i]
    return ''.join(result_arr)


# ═══════════════════════════════════════════════════════════
# 18. COLUMNAR TRANSPOSITION
# ═══════════════════════════════════════════════════════════
def columnar_encode(text, key):
    key = key.upper()
    num_cols = len(key)
    # Isi grid
    grid = [text[i:i+num_cols] for i in range(0, len(text), num_cols)]
    # Padding
    last = grid[-1] if grid else ''
    grid[-1] = last.ljust(num_cols, 'X')
    # Urutan kolom berdasarkan key
    order = sorted(range(num_cols), key=lambda i: key[i])
    result_str = ''
    for col in order:
        for row in grid:
            if col < len(row):
                result_str += row[col]
    return result_str

def columnar_decode(text, key):
    key = key.upper()
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    order = sorted(range(num_cols), key=lambda i: key[i])
    # Hitung panjang tiap kolom
    extra = len(text) % num_cols
    col_lengths = []
    for i in range(num_cols):
        # Kolom ke-i dalam urutan asli (bukan sorted)
        col_lengths.append(num_rows)
    # Bagi ciphertext ke kolom-kolom
    cols = {}
    idx = 0
    for col in order:
        length = col_lengths[col]
        cols[col] = list(text[idx:idx+length])
        idx += length
    # Baca per baris
    result_str = ''
    for row in range(num_rows):
        for col in range(num_cols):
            if col in cols and row < len(cols[col]):
                result_str += cols[col][row]
    return result_str.rstrip('X')


# ═══════════════════════════════════════════════════════════
# 19. BACON CIPHER (A=AAAAA, B=AAAAB, ...)
# ═══════════════════════════════════════════════════════════
BACON_MAP = {
    'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB',
    'E': 'AABAA', 'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB',
    'I': 'ABAAA', 'J': 'ABAAB', 'K': 'ABABA', 'L': 'ABABB',
    'M': 'ABAAA', 'N': 'ABABA', 'O': 'ABBAA', 'P': 'ABBAB',  # I=J, U=V (versi lama)
    'Q': 'ABBBA', 'R': 'ABBBB', 'S': 'BAAAA', 'T': 'BAAAB',
    'U': 'ABAAA', 'V': 'BAABA', 'W': 'BAABB', 'X': 'BABAA',
    'Y': 'BABAB', 'Z': 'BABBA'
}
BACON_REV = {v: k for k, v in BACON_MAP.items()}

def bacon_encode(text):
    result_parts = []
    for ch in text.upper():
        if ch in BACON_MAP:
            result_parts.append(BACON_MAP[ch])
        elif ch == ' ':
            result_parts.append(' ')
    return ' '.join(result_parts)

def bacon_decode(text):
    # Bersihkan dan bagi per 5 karakter
    text = text.upper().replace(' ', '')
    result_str = ''
    for i in range(0, len(text), 5):
        code = text[i:i+5]
        if code in BACON_REV:
            result_str += BACON_REV[code]
    return result_str


# ═══════════════════════════════════════════════════════════
# 20. PLAYFAIR CIPHER
# ═══════════════════════════════════════════════════════════
def playfair_make_square(key):
    key = key.upper().replace('J', 'I')
    seen = set()
    square = []
    for ch in key + string.ascii_uppercase.replace('J', ''):
        if ch not in seen:
            seen.add(ch)
            square.append(ch)
    return square

def playfair_find(square, ch):
    idx = square.index(ch)
    return idx // 5, idx % 5

def playfair_encode(text, key):
    square = playfair_make_square(key)
    text = text.upper().replace('J', 'I').replace(' ', '')
    # Buat digram
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    result_str = ''
    for a, b in pairs:
        ra, ca = playfair_find(square, a)
        rb, cb = playfair_find(square, b)
        if ra == rb:
            result_str += square[ra*5 + (ca+1)%5]
            result_str += square[rb*5 + (cb+1)%5]
        elif ca == cb:
            result_str += square[((ra+1)%5)*5 + ca]
            result_str += square[((rb+1)%5)*5 + cb]
        else:
            result_str += square[ra*5 + cb]
            result_str += square[rb*5 + ca]
    return result_str

def playfair_decode(text, key):
    square = playfair_make_square(key)
    text = text.upper().replace('J', 'I').replace(' ', '')
    pairs = [(text[i], text[i+1]) for i in range(0, len(text)-1, 2)]
    result_str = ''
    for a, b in pairs:
        ra, ca = playfair_find(square, a)
        rb, cb = playfair_find(square, b)
        if ra == rb:
            result_str += square[ra*5 + (ca-1)%5]
            result_str += square[rb*5 + (cb-1)%5]
        elif ca == cb:
            result_str += square[((ra-1)%5)*5 + ca]
            result_str += square[((rb-1)%5)*5 + cb]
        else:
            result_str += square[ra*5 + cb]
            result_str += square[rb*5 + ca]
    return result_str


# ═══════════════════════════════════════════════════════════
# 21. RSA (CTF - dengan angka kecil)
# ═══════════════════════════════════════════════════════════
def rsa_encrypt(m, e, n):
    return pow(int(m), int(e), int(n))

def rsa_decrypt(c, d, n):
    return pow(int(c), int(d), int(n))

def rsa_find_d(e, p, q):
    phi = (p-1) * (q-1)
    # Extended Euclidean Algorithm
    def egcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x
    _, d, _ = egcd(int(e) % (phi), phi)
    return d % phi

def rsa_info():
    print(f"""
{C.CYAN}╔══════════════ RSA CTF CHEAT SHEET ══════════════╗{C.RESET}
{C.WHITE}Variabel:{C.RESET}
  p, q   = bilangan prima
  n      = p × q  (modulus)
  e      = public exponent (biasanya 65537)
  φ(n)   = (p-1)(q-1)  (Euler's totient)
  d      = modular inverse dari e mod φ(n)  (private key)

{C.WHITE}Enkripsi:{C.RESET}  c = m^e mod n
{C.WHITE}Dekripsi:{C.RESET}  m = c^d mod n
{C.WHITE}Cari d:{C.RESET}    gunakan opsi --rsa-find-d
{C.CYAN}╚═════════════════════════════════════════════════╝{C.RESET}""")


# ═══════════════════════════════════════════════════════════
# 22. HASH IDENTIFIER (bukan crack, tapi identify)
# ═══════════════════════════════════════════════════════════
def identify_hash(h):
    h = h.strip()
    length = len(h)
    hints = []
    # Cek apakah hex
    try:
        int(h, 16)
        is_hex = True
    except:
        is_hex = False

    if is_hex:
        if length == 32:   hints.append("MD5 (32 hex chars)")
        if length == 40:   hints.append("SHA-1 (40 hex chars)")
        if length == 56:   hints.append("SHA-224 (56 hex chars)")
        if length == 64:   hints.append("SHA-256 (64 hex chars)")
        if length == 96:   hints.append("SHA-384 (96 hex chars)")
        if length == 128:  hints.append("SHA-512 (128 hex chars)")
    # Base64 pattern
    if h.endswith('=') or (len(h) % 4 == 0 and all(c in string.ascii_letters + string.digits + '+/=' for c in h)):
        hints.append("Mungkin Base64")
    if all(c in '01 ' for c in h):
        hints.append("Mungkin Binary")
    if all(c in string.digits + ' ' for c in h):
        hints.append("Mungkin Decimal/ASCII codes")
    if all(c in '.-/ ' for c in h):
        hints.append("Mungkin Morse Code")
    if not hints:
        hints.append("Format tidak dikenali")
    return hints


# ═══════════════════════════════════════════════════════════
# 23. BASE85
# ═══════════════════════════════════════════════════════════
def base85_encode(text):
    return base64.b85encode(text.encode()).decode()

def base85_decode(text):
    return base64.b85decode(text.encode()).decode(errors='replace')


# ═══════════════════════════════════════════════════════════
# 24. BASE58
# ═══════════════════════════════════════════════════════════
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(text):
    data = text.encode()
    n = int.from_bytes(data, 'big')
    result_str = ''
    while n > 0:
        n, rem = divmod(n, 58)
        result_str = BASE58_ALPHABET[rem] + result_str
    # Leading zeros
    for byte in data:
        if byte == 0:
            result_str = '1' + result_str
        else:
            break
    return result_str

def base58_decode(text):
    n = 0
    for ch in text:
        if ch not in BASE58_ALPHABET:
            raise ValueError(f"Karakter tidak valid: {ch}")
        n = n * 58 + BASE58_ALPHABET.index(ch)
    # Hitung panjang
    result_bytes = n.to_bytes((n.bit_length() + 7) // 8, 'big') if n else b''
    # Leading 1s = leading zero bytes
    pad = 0
    for ch in text:
        if ch == '1':
            pad += 1
        else:
            break
    return (b'\x00' * pad + result_bytes).decode(errors='replace')


# ═══════════════════════════════════════════════════════════
# 25. AUTO DETECT & DECODE
# ═══════════════════════════════════════════════════════════
def auto_detect(text):
    print(f"{C.YELLOW}[Auto Detect Mode]{C.RESET}")
    results = []

    # Base64
    try:
        d = base64_decode(text)
        if d and all(c.isprintable() for c in d):
            results.append(("Base64", d))
    except: pass

    # Hex
    try:
        clean = text.replace(' ', '').replace('0x', '')
        if all(c in '0123456789abcdefABCDEF' for c in clean) and len(clean) % 2 == 0:
            d = bytes.fromhex(clean).decode(errors='replace')
            results.append(("Hex", d))
    except: pass

    # Binary
    clean_bin = text.replace(' ', '')
    if all(c in '01' for c in clean_bin) and len(clean_bin) % 8 == 0:
        try:
            d = binary_decode(clean_bin)
            results.append(("Binary", d))
        except: pass

    # Caesar brute force (tampilkan shift 1-3 saja)
    for shift in [1, 2, 3, 13]:
        d = caesar_decode(text, shift)
        if d != text:
            results.append((f"Caesar shift={shift}", d))

    # ROT13
    d = rot13_decode(text)
    if d != text:
        results.append(("ROT13", d))

    # ROT47
    d = rot47(text)
    if d != text:
        results.append(("ROT47", d))

    # Morse
    if all(c in '.- /' for c in text):
        try:
            d = morse_decode(text)
            results.append(("Morse", d))
        except: pass

    # URL decode
    from urllib.parse import unquote
    d = unquote(text)
    if d != text:
        results.append(("URL Decode", d))

    # HTML decode
    import html
    d = html.unescape(text)
    if d != text:
        results.append(("HTML Decode", d))

    if results:
        print(f"\n{C.GREEN}Kemungkinan hasil decode:{C.RESET}")
        for method, val in results:
            print(f"  {C.CYAN}[{method}]{C.RESET} {val}")
    else:
        print(f"  {C.RED}Tidak ada yang cocok. Coba manual.{C.RESET}")

    # Identifikasi hash
    hints = identify_hash(text)
    if hints:
        print(f"\n{C.YELLOW}Hash Identification:{C.RESET}")
        for h in hints:
            print(f"  → {h}")


# ═══════════════════════════════════════════════════════════
# MENU INTERAKTIF
# ═══════════════════════════════════════════════════════════
CIPHER_LIST = [
    ("caesar",      "Caesar Cipher (shift)"),
    ("rot13",       "ROT13"),
    ("rot47",       "ROT47"),
    ("atbash",      "Atbash Cipher"),
    ("base64",      "Base64"),
    ("base32",      "Base32"),
    ("base16",      "Base16 / Hex"),
    ("base58",      "Base58 (Bitcoin)"),
    ("base85",      "Base85"),
    ("hex",         "Hex (0123456789ABCDEF)"),
    ("binary",      "Binary (01010101)"),
    ("octal",       "Octal"),
    ("decimal",     "Decimal / ASCII"),
    ("morse",       "Morse Code"),
    ("vigenere",    "Vigenere Cipher (key)"),
    ("xor",         "XOR Cipher (key/single byte)"),
    ("url",         "URL Encoding"),
    ("html",        "HTML Entity"),
    ("affine",      "Affine Cipher (a, b)"),
    ("railfence",   "Rail Fence Cipher (rails)"),
    ("columnar",    "Columnar Transposition (key)"),
    ("bacon",       "Bacon's Cipher"),
    ("playfair",    "Playfair Cipher (key)"),
    ("rsa",         "RSA (e, d, n, p, q)"),
    ("auto",        "Auto Detect & Decode"),
    ("identify",    "Identify / Guess Hash/Encoding"),
]

def show_list():
    print(f"\n{C.BOLD}{C.CYAN}══ DAFTAR CIPHER/ENCODING ══{C.RESET}")
    for i, (code, name) in enumerate(CIPHER_LIST, 1):
        print(f"  {C.YELLOW}{i:2d}.{C.RESET} {C.GREEN}{code:<14}{C.RESET} {name}")
    print()

def interactive_menu():
    banner()
    while True:
        show_list()
        print(f"{C.DIM}Ketik 'q' untuk keluar, 'list' untuk tampilkan daftar{C.RESET}")
        choice = input(f"\n{C.BOLD}Pilih cipher [{C.CYAN}nama/nomor{C.RESET}{C.BOLD}]: {C.RESET}").strip().lower()

        if choice in ('q', 'quit', 'exit'):
            print(f"\n{C.CYAN}Semangat solvenya!{C.RESET}\n")
            break

        if choice == 'list':
            continue

        # Resolve nomor → nama
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(CIPHER_LIST):
                choice = CIPHER_LIST[idx][0]
            else:
                err("Nomor tidak valid!")
                continue

        if choice not in [c[0] for c in CIPHER_LIST]:
            err(f"Cipher '{choice}' tidak ditemukan. Ketik 'list' untuk melihat daftar.")
            continue

        # Pilih encode/decode
        if choice in ('auto', 'identify', 'rot13', 'rot47', 'atbash', 'morse'):
            mode = 'd'  # Langsung decode/process
        elif choice == 'rsa':
            mode = 'r'
        else:
            m = input(f"  {C.BOLD}[E]ncode / [D]ecode / [B]rute force: {C.RESET}").strip().lower()
            mode = m[0] if m else 'e'

        # Input teks
        if choice != 'rsa' and choice != 'identify':
            text = input(f"  {C.BOLD}Input teks: {C.RESET}")

        print()

        try:
            # ── CAESAR ──
            if choice == 'caesar':
                if mode == 'b':
                    caesar_bruteforce(text)
                else:
                    shift = int(input(f"  Shift (default=3): ") or "3")
                    if mode == 'e':
                        result(caesar_encode(text, shift))
                    else:
                        result(caesar_decode(text, shift))

            # ── ROT13 ──
            elif choice == 'rot13':
                result(rot13_encode(text))

            # ── ROT47 ──
            elif choice == 'rot47':
                result(rot47(text))

            # ── ATBASH ──
            elif choice == 'atbash':
                result(atbash(text))

            # ── BASE64 ──
            elif choice == 'base64':
                if mode == 'e': result(base64_encode(text))
                else: result(base64_decode(text))

            # ── BASE32 ──
            elif choice == 'base32':
                if mode == 'e': result(base32_encode(text))
                else: result(base32_decode(text))

            # ── BASE16 ──
            elif choice == 'base16':
                if mode == 'e': result(base16_encode(text))
                else: result(base16_decode(text))

            # ── BASE58 ──
            elif choice == 'base58':
                if mode == 'e': result(base58_encode(text))
                else: result(base58_decode(text))

            # ── BASE85 ──
            elif choice == 'base85':
                if mode == 'e': result(base85_encode(text))
                else: result(base85_decode(text))

            # ── HEX ──
            elif choice == 'hex':
                if mode == 'e': result(hex_encode(text))
                else: result(hex_decode(text))

            # ── BINARY ──
            elif choice == 'binary':
                if mode == 'e': result(binary_encode(text))
                else: result(binary_decode(text))

            # ── OCTAL ──
            elif choice == 'octal':
                if mode == 'e': result(octal_encode(text))
                else: result(octal_decode(text))

            # ── DECIMAL ──
            elif choice == 'decimal':
                if mode == 'e': result(decimal_encode(text))
                else: result(decimal_decode(text))

            # ── MORSE ──
            elif choice == 'morse':
                m2 = input(f"  [E]ncode / [D]ecode: ").strip().lower()
                if m2.startswith('e'): result(morse_encode(text))
                else: result(morse_decode(text))

            # ── VIGENERE ──
            elif choice == 'vigenere':
                key = input(f"  Key: ")
                if mode == 'e': result(vigenere_encode(text, key))
                else: result(vigenere_decode(text, key))

            # ── XOR ──
            elif choice == 'xor':
                if mode == 'b':
                    xor_bruteforce(text)
                else:
                    key_raw = input(f"  Key (string atau angka 0-255): ")
                    try:
                        key = int(key_raw)
                    except:
                        key = key_raw
                    if mode == 'e': result(xor_encode(text, key))
                    else: result(xor_decode(text, key))

            # ── URL ──
            elif choice == 'url':
                if mode == 'e': result(url_encode(text))
                else: result(url_decode(text))

            # ── HTML ──
            elif choice == 'html':
                if mode == 'e': result(html_encode(text))
                else: result(html_decode(text))

            # ── AFFINE ──
            elif choice == 'affine':
                a = int(input(f"  a (default=5): ") or "5")
                b = int(input(f"  b (default=8): ") or "8")
                if mode == 'e': result(affine_encode(text, a, b))
                else: result(affine_decode(text, a, b))

            # ── RAIL FENCE ──
            elif choice == 'railfence':
                rails = int(input(f"  Jumlah rel (default=3): ") or "3")
                if mode == 'e': result(railfence_encode(text, rails))
                else: result(railfence_decode(text, rails))

            # ── COLUMNAR ──
            elif choice == 'columnar':
                key = input(f"  Key (contoh: ZEBRA): ")
                if mode == 'e': result(columnar_encode(text, key))
                else: result(columnar_decode(text, key))

            # ── BACON ──
            elif choice == 'bacon':
                if mode == 'e': result(bacon_encode(text))
                else: result(bacon_decode(text))

            # ── PLAYFAIR ──
            elif choice == 'playfair':
                key = input(f"  Key: ")
                if mode == 'e': result(playfair_encode(text, key))
                else: result(playfair_decode(text, key))

            # ── RSA ──
            elif choice == 'rsa':
                rsa_info()
                sub = input(f"  [E]ncrypt / [D]ecrypt / [F]ind-d: ").strip().lower()
                if sub.startswith('e'):
                    m_val = input("  m (plaintext angka): ")
                    e_val = input("  e (public exponent): ")
                    n_val = input("  n (modulus): ")
                    result(str(rsa_encrypt(m_val, e_val, n_val)))
                elif sub.startswith('d'):
                    c_val = input("  c (ciphertext angka): ")
                    d_val = input("  d (private key): ")
                    n_val = input("  n (modulus): ")
                    res = rsa_decrypt(c_val, d_val, n_val)
                    print(f"\n{C.GREEN}══ RESULT ══{C.RESET}")
                    print(f"  Angka : {res}")
                    try:
                        print(f"  String: {res.to_bytes((res.bit_length()+7)//8, 'big').decode()}")
                    except:
                        pass
                    print()
                elif sub.startswith('f'):
                    e_val = int(input("  e: "))
                    p_val = int(input("  p: "))
                    q_val = int(input("  q: "))
                    d = rsa_find_d(e_val, p_val, q_val)
                    result(f"d = {d}")

            # ── AUTO ──
            elif choice == 'auto':
                auto_detect(text)

            # ── IDENTIFY ──
            elif choice == 'identify':
                h = input(f"  Input hash/string: ")
                hints = identify_hash(h)
                print(f"\n{C.CYAN}Kemungkinan:{C.RESET}")
                for hint in hints:
                    print(f"  → {hint}")
                print()

        except Exception as ex:
            err(f"Error: {ex}")

        input(f"\n{C.DIM}[Enter untuk lanjut...]{C.RESET}")
        print()


# ═══════════════════════════════════════════════════════════
# CLI (NON-INTERACTIVE) MODE
# ═══════════════════════════════════════════════════════════
def cli_mode():
    parser = argparse.ArgumentParser(
        description='CTF Cryptography Toolkit - @leapwithluvi',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Contoh:
  python3 crypto_ctf.py -c caesar -e "Hello World" --shift 13
  python3 crypto_ctf.py -c base64 -d "SGVsbG8="
  python3 crypto_ctf.py -c vigenere -e "Hello" --key SECRET
  python3 crypto_ctf.py -c xor -e "Hello" --key 42
  python3 crypto_ctf.py -c morse -e "SOS"
  python3 crypto_ctf.py -c auto -d "SGVsbG8="
  python3 crypto_ctf.py --list
        """
    )
    parser.add_argument('-c', '--cipher', help='Nama cipher (lihat --list)')
    parser.add_argument('-e', '--encode', metavar='TEXT', help='Encode teks')
    parser.add_argument('-d', '--decode', metavar='TEXT', help='Decode teks')
    parser.add_argument('-b', '--bruteforce', metavar='TEXT', help='Brute force')
    parser.add_argument('--shift', type=int, default=3, help='Caesar shift (default=3)')
    parser.add_argument('--key', default='', help='Key untuk Vigenere/XOR/Playfair/Columnar')
    parser.add_argument('--rails', type=int, default=3, help='Rail Fence rails (default=3)')
    parser.add_argument('--a', type=int, default=5, help='Affine a (default=5)')
    parser.add_argument('--b-val', type=int, default=8, help='Affine b (default=8)')
    parser.add_argument('--list', action='store_true', help='Tampilkan semua cipher')

    if len(sys.argv) == 1:
        return False  # Masuk interactive mode

    args = parser.parse_args()

    if args.list:
        banner()
        show_list()
        return True

    if not args.cipher:
        parser.print_help()
        return True

    c = args.cipher.lower()
    text = args.encode or args.decode or args.bruteforce or ''
    mode = 'e' if args.encode else ('b' if args.bruteforce else 'd')

    try:
        if c == 'caesar':
            if mode == 'b': caesar_bruteforce(text)
            elif mode == 'e': result(caesar_encode(text, args.shift))
            else: result(caesar_decode(text, args.shift))
        elif c == 'rot13': result(rot13_encode(text))
        elif c == 'rot47': result(rot47(text))
        elif c == 'atbash': result(atbash(text))
        elif c == 'base64':
            if mode == 'e': result(base64_encode(text))
            else: result(base64_decode(text))
        elif c == 'base32':
            if mode == 'e': result(base32_encode(text))
            else: result(base32_decode(text))
        elif c == 'base16':
            if mode == 'e': result(base16_encode(text))
            else: result(base16_decode(text))
        elif c == 'base58':
            if mode == 'e': result(base58_encode(text))
            else: result(base58_decode(text))
        elif c == 'base85':
            if mode == 'e': result(base85_encode(text))
            else: result(base85_decode(text))
        elif c == 'hex':
            if mode == 'e': result(hex_encode(text))
            else: result(hex_decode(text))
        elif c == 'binary':
            if mode == 'e': result(binary_encode(text))
            else: result(binary_decode(text))
        elif c == 'octal':
            if mode == 'e': result(octal_encode(text))
            else: result(octal_decode(text))
        elif c == 'decimal':
            if mode == 'e': result(decimal_encode(text))
            else: result(decimal_decode(text))
        elif c == 'morse':
            if mode == 'e': result(morse_encode(text))
            else: result(morse_decode(text))
        elif c == 'vigenere':
            if mode == 'e': result(vigenere_encode(text, args.key))
            else: result(vigenere_decode(text, args.key))
        elif c == 'xor':
            if mode == 'b': xor_bruteforce(text)
            else:
                try: key = int(args.key)
                except: key = args.key
                if mode == 'e': result(xor_encode(text, key))
                else: result(xor_decode(text, key))
        elif c == 'url':
            if mode == 'e': result(url_encode(text))
            else: result(url_decode(text))
        elif c == 'html':
            if mode == 'e': result(html_encode(text))
            else: result(html_decode(text))
        elif c == 'affine':
            if mode == 'e': result(affine_encode(text, args.a, args.b_val))
            else: result(affine_decode(text, args.a, args.b_val))
        elif c == 'railfence':
            if mode == 'e': result(railfence_encode(text, args.rails))
            else: result(railfence_decode(text, args.rails))
        elif c == 'columnar':
            if mode == 'e': result(columnar_encode(text, args.key))
            else: result(columnar_decode(text, args.key))
        elif c == 'bacon':
            if mode == 'e': result(bacon_encode(text))
            else: result(bacon_decode(text))
        elif c == 'playfair':
            if mode == 'e': result(playfair_encode(text, args.key))
            else: result(playfair_decode(text, args.key))
        elif c == 'auto':
            auto_detect(text)
        elif c == 'identify':
            hints = identify_hash(text)
            for h in hints:
                print(f"  → {h}")
        else:
            err(f"Cipher '{c}' tidak dikenali. Gunakan --list untuk daftar.")
    except Exception as ex:
        err(f"Error: {ex}")

    return True


# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    # Coba CLI mode dulu, kalau tidak ada argumen → interactive
    if not cli_mode():
        try:
            interactive_menu()
        except KeyboardInterrupt:
            print(f"\n\n{C.CYAN}Semangat solvenya!{C.RESET}\n")
