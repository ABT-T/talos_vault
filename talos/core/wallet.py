import os
import base58
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey

load_dotenv()

class Signer(ABC):
    """Abstract base class for transaction signing strategies."""
    
    @abstractmethod
    def public_key(self) -> Pubkey:
        pass

    @abstractmethod
    def sign_transaction(self, tx_bytes: bytes) -> bytes:
        pass

class LocalKeySigner(Signer):
    """
    Implementation for PoC/Devnet using local environment variables.
    WARNING: Not suitable for Mainnet production.
    """
    def __init__(self):
        secret = os.getenv("SOLANA_PRIVATE_KEY")
        if not secret:
            # Fallback for CI/CD or no-key environments
            self._keypair = Keypair()
        else:
            try:
                decoded = base58.b58decode(secret)
                self._keypair = Keypair.from_bytes(decoded)
            except Exception:
                self._keypair = Keypair()

    def public_key(self) -> Pubkey:
        return self._keypair.pubkey()

    def sign_transaction(self, tx_bytes: bytes) -> bytes:
        # In a real implementation, this would sign the transaction object
        # For this abstraction demo, we return the keypair signature logic
        return b"mock_signature_bytes" 

class HardwareSigner(Signer):
    """
    Placeholder for Ledger/HSM implementation.
    TODO: Implement PKCS#11 interface for Mainnet.
    """
    def public_key(self) -> Pubkey:
        raise NotImplementedError("Hardware signing not available in PoC.")

    def sign_transaction(self, tx_bytes: bytes) -> bytes:
        raise NotImplementedError("Hardware signing not available in PoC.")
