import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Centralized configuration management."""
    
    # Network
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
    RPC_URL = f"https://devnet.helius-rpc.com/?api-key={HELIUS_API_KEY}" if HELIUS_API_KEY else "https://api.devnet.solana.com"
    
    # Agent Settings
    AGENT_NAME = "Talos v1.2 (Nightly)"
    DEFAULT_TX_FEE = 0.001  # SOL
    SIMULATION_MODE = os.getenv("SIMULATION_MODE", "True").lower() == "true"
    
    # Retry Logic
    MAX_RETRIES = 3
    TIMEOUT = 10  # seconds

config = Config()
