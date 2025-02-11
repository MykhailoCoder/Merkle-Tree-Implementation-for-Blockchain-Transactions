import hashlib

class MerkleTree:
    def __init__(self, transactions):
        self.transactions = transactions
        self.tree = []
        self.root = self.build_merkle_tree()

    def hash_transaction(self, data):
        """Hashes a transaction using SHA-256"""
        return hashlib.sha256(data.encode()).hexdigest()

    def build_merkle_tree(self):
        """Builds a Merkle tree and returns the Merkle root"""
        leaves = [self.hash_transaction(tx) for tx in self.transactions]
        self.tree.append(leaves)

        while len(leaves) > 1:
            new_level = []
            for i in range(0, len(leaves), 2):
                if i + 1 < len(leaves):
                    combined = leaves[i] + leaves[i + 1]
                else:
                    combined = leaves[i]  # If odd, duplicate last hash
                new_level.append(self.hash_transaction(combined))
            leaves = new_level
            self.tree.append(leaves)

        return leaves[0] if leaves else None

    def print_tree(self):
        """Prints the Merkle tree levels"""
        for i, level in enumerate(self.tree):
            print(f"Level {i}: {level}")

    def verify_transaction(self, transaction):
        """Verifies if a transaction is part of the Merkle tree"""
        hashed_tx = self.hash_transaction(transaction)
        for level in self.tree:
            if hashed_tx in level:
                return True
        return False


# Example usage
if __name__ == "__main__":
    transactions = [
        "Alice pays Bob 10 BTC",
        "Bob pays Charlie 5 BTC",
        "Charlie pays Dave 2 BTC",
        "Dave pays Eve 1 BTC"
    ]

    merkle_tree = MerkleTree(transactions)
    
    print("\nMerkle Tree:")
    merkle_tree.print_tree()
    
    print("\nMerkle Root:", merkle_tree.root)

    # Verifying a transaction
    tx_to_verify = "Alice pays Bob 10 BTC"
    print(f"\nIs '{tx_to_verify}' in the Merkle Tree? {merkle_tree.verify_transaction(tx_to_verify)}")
