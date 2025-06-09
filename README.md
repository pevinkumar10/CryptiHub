# CryptiHub - Secure End-to-End Encrypted Chat System

A secure chat application featuring room-based end-to-end encryption, designed to protect your communications from eavesdropping.

## Key Features

- 🔒 **End-to-End Encryption** using Fernet (AES-256)
- 🛡️ **Room-Based Authentication** with unique keys
- 🌐 **Real-Time Broadcasting** to multiple clients
- 🧵 **Thread-Safe** socket handling
- 🔑 **PBKDF2 Key Derivation** (1.2M iterations)

## Installation

```bash
git clone https://github.com/pevinkumar10/CryptiHub.git
cd CryptiHub
```
### Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server
```bash
python server/server.py
```

### Connecting Clients
```bash

python3 clients/client.py

```

## Security Architecture

1. **Key Derivation**  
   Uses PBKDF2-HMAC-SHA256 with:
   - 1,200,000 iterations
   - 16-byte random salt per message
   - 32-byte derived keys

2. **Encryption**  
   - AES-256 in GCM mode via Fernet
   - Message-level salts prevent replay attacks

3. **Authentication**  
   - Clients must prove room ID to enter the chat
   - Username collision prevention

## Limitations

⚠️ **Note**: This implementation uses symmetric encryption with a shared room key. For true E2EE where the server cannot decrypt messages, consider:

1. Implementing Diffie-Hellman key exchange
2. Adding ephemeral session keys
3. Client-side key storage

## License

[MIT](./LICENSE) © 2025 PevinKumar A