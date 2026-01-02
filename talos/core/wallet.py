import os
import base58
from abc import ABC, abstractmethod
from typing import Optional
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Load environment variables for local development context
load_dotenv()

class Signer(ABC):
    """
    Abstract base class defining the interface for transaction signing strategies.
    
    Design Pattern: Strategy Pattern
    This abstraction allows the engine to decouple business logic from the specific 
    signing implementation (e.g., Local Key, Hardware Wallet, MPC, or Cloud KMS).
    """
    
    @abstractmethod
    def public_key(self) -> Pubkey:
        """Returns the public key associated with the signer entity."""
        pass

    @abstractmethod
    def sign_message(self, message: bytes) -> bytes:
        """
        Cryptographically signs an arbitrary message or transaction payload.
        
        Args:
            message (bytes): The serialized message to sign.
            
        Returns:
            bytes: The resulting signature.
        """
        pass

class LocalKeySigner(Signer):
    """
    Implementation for Devnet/PoC environments using ephemeral local environment variables.
    
    Security Note: 
    This implementation utilizes hot-wallet keys injected via the process environment.
    It is STRICTLY intended for development, testing, and non-production demonstrations.
    """
    def __init__(self):
        secret = os.getenv("SOLANA_PRIVATE_KEY")
        if not secret:
            # Graceful fallback: Generate ephemeral key for CI/CD or unconfigured environments
            self._keypair = Keypair()
        else:
            try:
                decoded = base58.b58decode(secret)
                self._keypair = Keypair.from_bytes(decoded)
            except Exception:
                # Prevent initialization crash on malformed keys; revert to ephemeral
                self._keypair = Keypair()

    def public_key(self) -> Pubkey:
        return self._keypair.pubkey()

    def sign_message(self, message: bytes) -> bytes:
        # Wrapper around the underlying ed25519 signing logic
        return bytes(self._keypair.sign_message(message))

class HardwareSigner(Signer):
    """
    Placeholder implementation for Hardware Security Module (HSM) or Ledger integration.
    Reserved for Phase 2 (Production Hardening) to enforce physical transaction authorization.
    """
    def public_key(self) -> Pubkey:
        raise NotImplementedError("Hardware signing interface is not active in the current build.")

    def sign_message(self, message: bytes) -> bytes:
        raise NotImplementedError("Hardware signing interface is not active in the current build.")
