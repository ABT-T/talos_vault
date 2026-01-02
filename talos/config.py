import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

class Config:
    """
    Centralized configuration management for the Talos Agent.
    Implements security guardrails and network parameters.
    """
    
    # --- OPERATION MODES ---
    # Defaults to SIMULATION to prevent accidental capital loss during development/demos.
    MODE = os.getenv("TALOS_MODE", "SIMULATION").upper()
    
    # --- RISK MANAGEMENT (GUARDRAILS) ---
    # Hard limits to prevent runaway loops or excessive spending.
    MAX_TX_PER_SESSION = 5       # Execution cap per runtime session
    MAX_DAILY_LOSS = 0.1         # Maximum authorized drawdown in SOL
    
    # --- NETWORK INFRASTRUCTURE ---
    HELIUS_API_KEY = os.getenv("HELIUS_API_KEY")
    # Fallback to public RPC if Helius key is missing, though latency may increase.
    RPC_URL = f"https://devnet.helius-rpc.com/?api-key={HELIUS_API_KEY}" if HELIUS_API_KEY else "https://api.devnet.solana.com"
    
    # --- AGENT METADATA ---
    AGENT_NAME = "Talos v1.2 (Sentinel Build)"
    DEFAULT_TX_FEE = 0.001

config = Config()
