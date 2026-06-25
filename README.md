# CipherKit CTF — Python Cryptography Toolkit for CTF

> **Offline CLI tool** untuk encode & decode 26+ cipher/encoding — dibuat khusus untuk persiapan lomba CTF, tanpa butuh internet atau website online.

```
 ██████╗████████╗███████╗     ██████╗██████╗ ██╗   ██╗██████╗ ████████╗ ██████╗ 
██╔════╝╚══██╔══╝██╔════╝    ██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝██╔═══██╗
██║        ██║   █████╗      ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   ██║   ██║
██║        ██║   ██╔══╝      ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   ██║   ██║
╚██████╗   ██║   ██║         ╚██████╗██║  ██║   ██║   ██║        ██║   ╚██████╔╝
 ╚═════╝   ╚═╝   ╚═╝          ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝    ╚═════╝ 
```

---

## Fitur

- **26+ cipher & encoding** dalam satu file Python
- **Mode interaktif** — navigasi dengan menu bernomor
- **Mode CLI** — langsung dari terminal, cocok untuk skripting cepat
- **Auto Detect** — tidak tahu formatnya? biarkan tool yang tebak
- **Brute Force** — Caesar & XOR single-byte otomatis
- **RSA helper** — encrypt, decrypt, dan cari private key `d`
- **Zero dependency** — hanya Python 3 standard library
- **100% offline** — tidak butuh internet sama sekali

---

## Cara Pakai

### Mode Interaktif (Rekomendasi)

```bash
python3 crypto_ctf.py
```

Pilih cipher dari menu bernomor, lalu ikuti instruksi di layar.

### Mode CLI

```bash
# Lihat semua cipher yang tersedia
python3 crypto_ctf.py --list

# Encode / Decode
python3 crypto_ctf.py -c base64 -e "Hello World"
python3 crypto_ctf.py -c base64 -d "SGVsbG8gV29ybGQ="

# Caesar dengan shift tertentu
python3 crypto_ctf.py -c caesar -e "Hello" --shift 13
python3 crypto_ctf.py -c caesar -d "Uryyb" --shift 13

# Caesar brute force (coba semua 25 shift)
python3 crypto_ctf.py -c caesar -b "Khoor"

# Vigenere dengan key
python3 crypto_ctf.py -c vigenere -e "Hello" --key SECRET
python3 crypto_ctf.py -c vigenere -d "Zincs" --key SECRET

# XOR dengan key angka
python3 crypto_ctf.py -c xor -e "Hello" --key 42

# XOR brute force single byte
python3 crypto_ctf.py -c xor -b "624f464645"

# RSA helper
python3 crypto_ctf.py -c rsa   # interaktif

# Auto detect encoding (tidak tahu formatnya)
python3 crypto_ctf.py -c auto -d "SGVsbG8="
```

---

## 📋 Daftar Cipher & Encoding

| # | Cipher | Flag CLI | Keterangan |
|---|--------|----------|------------|
| 1 | Caesar | `caesar` | Shift A-Z, support brute force |
| 2 | ROT13 | `rot13` | Caesar shift 13, symmetric |
| 3 | ROT47 | `rot47` | Semua karakter ASCII printable |
| 4 | Atbash | `atbash` | A↔Z, B↔Y (mirror alphabet) |
| 5 | Base64 | `base64` | Encoding paling umum di CTF |
| 6 | Base32 | `base32` | Mirip Base64, uppercase + angka |
| 7 | Base16 | `base16` | Alias hex uppercase |
| 8 | Base58 | `base58` | Dipakai Bitcoin, tanpa 0/O/I/l |
| 9 | Base85 | `base85` | Lebih padat dari Base64 |
| 10 | Hex | `hex` | Hexadecimal 0-9 A-F |
| 11 | Binary | `binary` | 01010101 per karakter 8-bit |
| 12 | Octal | `octal` | Basis 8 |
| 13 | Decimal | `decimal` | ASCII code per karakter |
| 14 | Morse | `morse` | `. - / ` |
| 15 | Vigenere | `vigenere` | Polyalphabetic + key |
| 16 | XOR | `xor` | XOR dengan key string/byte, + brute force |
| 17 | URL Encode | `url` | %XX percent encoding |
| 18 | HTML Entity | `html` | `&amp;` `&lt;` dst. |
| 19 | Affine | `affine` | E(x) = (ax + b) mod 26 |
| 20 | Rail Fence | `railfence` | Zigzag transposition |
| 21 | Columnar | `columnar` | Transposisi berdasarkan key |
| 22 | Bacon | `bacon` | A=AAAAA, B=AAAAB, ... |
| 23 | Playfair | `playfair` | Digraph substitution 5×5 |
| 24 | RSA | `rsa` | Encrypt / Decrypt / Cari `d` |
| 25 | Auto Detect | `auto` | Coba semua metode sekaligus |
| 26 | Hash Identify | `identify` | Tebak jenis hash/encoding |

---

## 💡 Tips CTF

**Tidak tahu enkripsi apa?** Gunakan `auto`:
```bash
python3 crypto_ctf.py -c auto -d "teks_misterius_di_sini"
```

**Ciri-ciri cepat mengenali encoding:**

| Ciri | Kemungkinan |
|------|-------------|
| Hanya `A-Z`, `2-7`, diakhiri `=` | Base32 |
| `A-Z`, `a-z`, `0-9`, `+/=` | Base64 |
| Hanya `0-9` dan `A-F` | Hex |
| Hanya `0` dan `1` | Binary |
| Ada `.-` dan `/` | Morse |
| Panjang 32 hex | MD5 |
| Panjang 40 hex | SHA-1 |
| Panjang 64 hex | SHA-256 |
| Semua huruf bergeser seragam | Caesar/ROT13 |
| Teks bergeser tapi tidak seragam | Vigenere |

---

## ⚙️ Requirement

- Python 3.6+
- Tidak ada library eksternal (pure standard library)

```bash
# Clone dan langsung pakai
git clone https://github.com/leapwithluvi/cipherkit.git
cd cipherkit
python3 crypto_ctf.py
```

---

## Struktur

```
cipherkit/
└── crypto_ctf.py    # Semua cipher dalam satu file
└── README.md
```

---

## Dibuat Untuk

- Track Cybersecurity / CTF
- Kompetisi CTF lainnya yang membatasi akses internet
- Belajar kriptografi klasik secara mandiri

---

## License

MIT License — bebas dipakai, dimodifikasi, dan dibagikan.
