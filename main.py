import hashlib
import time

# -------------------------------
# Block Class
# -------------------------------
class Block:
    def _init_(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data  # certificate details
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.previous_hash) + str(self.timestamp) + str(self.data)
        return hashlib.sha256(block_string.encode()).hexdigest()

# -------------------------------
# Blockchain Class
# -------------------------------
class Blockchain:
    def _init_(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block - Certificate Verification Started")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), previous_block.hash, time.time(), data)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# -------------------------------
# Certificate Registration
# -------------------------------
cert_chain = Blockchain()

num_certificates = int(input("Enter number of certificates to add: "))

for i in range(num_certificates):
    student_id = input(f"\nEnter Student ID for certificate {i+1}: ").strip()
    student_name = input("Enter Student Name: ").strip()
    course = input("Enter Course Name: ").strip()
    certificate_id = input("Enter Certificate ID: ").strip()
    issuer = input("Enter Issuer/Institute Name: ").strip()

    # Store certificate as block data
    cert_data = f"StudentID:{student_id}, Name:{student_name}, Course:{course}, CertificateID:{certificate_id}, Issuer:{issuer}, Status:Verified"
    cert_chain.add_block(cert_data)

print("\n--- Blockchain Certificates ---\n")
for block in cert_chain.chain:
    print(f"Index: {block.index}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}\n")

print("Is blockchain valid?", cert_chain.is_chain_valid())

# -------------------------------
# Verification Step
# -------------------------------
search_id = input("\nEnter Certificate ID to verify: ").strip()
found = False
for block in cert_chain.chain[1:]:
    if f"CertificateID:{search_id}" in block.data:
        print("\n✅ Certificate Verified!")
        print(f"Details: {block.data}")
        found = True
        break

if not found:
    print("❌ Certificate Not Found in Blockchain!")