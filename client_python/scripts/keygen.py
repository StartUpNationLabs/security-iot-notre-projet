import rsa

# Generate a 512-bit RSA key pair
(pubkey, privkey) = rsa.newkeys(512)

# Save keys to files
with open("server.pub", "wb") as f:
    f.write(rsa.PublicKey.save_pkcs1(pubkey))
with open("server.pem", "wb") as f:
    f.write(rsa.PrivateKey.save_pkcs1(privkey))

# Format public key components as byte arrays
e_bytes = pubkey.e.to_bytes((pubkey.e.bit_length() + 7) // 8, "big")
n_bytes = pubkey.n.to_bytes((pubkey.n.bit_length() + 7) // 8, "big")

# Print formatted for Java
print("// Server's public key (e)")
print("private static final byte[] SERVER_KEY_E = {")
print(",".join(f"(byte) 0x{b:02X}" for b in e_bytes))
print("};")
print("\n// Server's public key (n)")
print("private static final byte[] SERVER_KEY_N = {")
print(",".join(f"(byte) 0x{b:02X}" for b in n_bytes))
print("};")
