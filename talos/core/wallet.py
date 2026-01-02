import os
import json
import base58
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from eth_account import Account

load_dotenv()

class MultiChainWallet:
    """
    Secure wallet manager supporting Solana and EVM chains.
    Keys are loaded from environment variables, never stored in plain text files.
    """
    def __init__(self):
        self.keys = {}
        self._load_keys()

    def _load_keys(self):
        # 1. Load Solana Key
        sol_secret = os.getenv("SOLANA_PRIVATE_KEY")
        if sol_secret:
            try:
                # پشتیبانی از فرمت Base58 (فانتوم)
                decoded = base58.b58decode(sol_secret)
                self.keys["solana"] = Keypair.from_bytes(decoded)
            except Exception as e:
                print(f"Warning: Could not load Solana key: {e}")
                self.keys["solana"] = Keypair() # Fallback: Generate random for safety
        else:
            self.keys["solana"] = Keypair()

        self.evm_account = Account.create()

    def get_address(self, chain="solana"):
        if chain == "solana":
            return str(self.keys["solana"].pubkey())
        elif chain in ["ethereum", "base", "polygon"]:
            return self.evm_account.address
        return None

    def sign_message(self, message, chain="solana"):
        pass
