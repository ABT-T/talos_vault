"""
Talos LangChain Integration
Provides a TalosPaymentTool for AI agents to execute secure payments via MultiChainEngine.
"""
from langchain_core.tools import BaseTool
from typing import Type, Optional

from langchain_core.pydantic_v1 import BaseModel, Field, PrivateAttr
# -----------------------------------------------------------------------

from talos.payments.engine import MultiChainEngine

class PaymentInput(BaseModel):
    to_address: str = Field(description="The wallet address of the recipient.")
    amount: float = Field(description="The amount of crypto to send.")
    chain: str = Field(default="SOLANA", description="Preferred blockchain network (SOLANA, BASE, ETH). Defaults to SOLANA.")

class TalosPaymentTool(BaseTool):
    name: str = "talos_payment_protocol"
    description: str = (
        "Use this tool whenever the user wants to send money, crypto, or make a payment. "
        "You must extract the target address, the amount, and optionally the preferred chain."
    )
    args_schema: Type[BaseModel] = PaymentInput
    
    _engine: MultiChainEngine = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._engine = MultiChainEngine()

    def _run(self, to_address: str, amount: float, chain: str = "SOLANA"):
        try:
            print(f"\n  AI Agent is requesting payment on [{chain}]...")
            
            if self._engine is None:
                self._engine = MultiChainEngine()

            tx_hash = self._engine.send_request(to_address, amount, preferred_chain=chain)
            
            if tx_hash:
                return f" Payment Successful! Transaction Hash: {tx_hash}"
            else:
                return " Payment Failed or Cancelled by Security Protocol."
                
        except Exception as e:
            return f" Error executing payment: {str(e)}"

    def _arun(self, to_address: str, amount: float, chain: str = "SOLANA"):
        raise NotImplementedError("Async not implemented yet")