<p align="center">
  <img src="assets/banner.png" alt="CryptiHub Banner" width="80%"/>
</p>

<h1 align="center">🔐 CryptiHub | Secure Encrypted Chat System</h1>

<p align="center">
  A real-time room-based chat system with end-to-end encryption designed to secure communication using modern cryptographic standards.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Encryption-AES--256%20(Fernet)-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Key%20Derivation-PBKDF2-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Socket-Real--Time-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge" />
</p>

---

## 📌 Overview

**CryptiHub** is a lightweight encrypted chat system built for secure communication over networks.

It supports:
- Room-based secure messaging
- Real-time multi-client communication
- Strong symmetric encryption pipeline

---

## ✨ Features

- 🔒 End-to-End Encryption (Fernet / AES-256)
- 🧵 Multi-client real-time chat via sockets
- 🛡️ Room-based authentication system
- 🔑 PBKDF2 key derivation (1.2M iterations)
- ⚡ Thread-safe server architecture

---

## ⚙️ Installation

### 📥 Clone Repository
```bash
git clone https://github.com/pevinkumar10/CryptiHub.git
cd CryptiHub
````

---

### 📦 Install Dependencies

#### Windows:

```bash
pip install -r requirements.txt
```

#### Linux:

```bash
sudo apt-get install python3-tk
```

---

## ⚙️ Configuration

### 🖥️ Server Config

Edit:

```
server/modules/core.py
```

```python
HOST = ""
PORT = 1234
```

---

### 💻 Client Config

Edit:

```
client/client.py
```

```python
HOST = ""
PORT = 1234
```

---

## 🚀 Usage

### ▶️ Start Server

```bash
python3 server/server.py
```

### 💬 Start Client

```bash
python3 client/client.py
```

---

## 🔐 Security Architecture

### 1. Key Derivation

* PBKDF2-HMAC-SHA256
* 1,200,000 iterations
* Per-message random salt (16 bytes)
* 32-byte derived encryption key

### 2. Encryption Layer

* Fernet (AES-256)
* Message-level encryption
* Replay attack resistance via salts

### 3. Authentication Model

* Room-based access control
* Username collision prevention
* Shared session key per room

---

## ⚠️ Limitations

This implementation uses **shared symmetric keys**, meaning:

* Server can potentially decrypt messages
* Not fully true E2EE

### Recommended Improvements:

* Diffie-Hellman key exchange
* Ephemeral session keys
* Client-side key storage only

---

## 📜 License

MIT License © 2025 PevinKumar A
