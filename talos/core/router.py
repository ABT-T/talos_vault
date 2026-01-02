import logging

logger = logging.getLogger("TalosRouter")

class NetworkRouter:
    
    def __init__(self):
        self.networks = {
            "SOLANA": {"status": "ONLINE", "fee": 0.000005, "speed": "FAST"},
            "BASE":   {"status": "ONLINE", "fee": 0.0001,   "speed": "MEDIUM"},
            "POLYGON":{"status": "CONGESTED", "fee": 0.01,  "speed": "SLOW"},
        }
    
    def get_best_route(self, preferred_chain=None):
        if preferred_chain and self.networks.get(preferred_chain, {}).get("status") == "ONLINE":
            return preferred_chain

        logger.info(" Analyzing blockchain networks for best route...")
        best_chain = "SOLANA"
        min_fee = 999.0
        
        for chain, stats in self.networks.items():
            if stats["status"] == "ONLINE" and stats["fee"] < min_fee:
                best_chain = chain
                min_fee = stats["fee"]
        
        logger.info(f" Optimal Route Found: {best_chain} (Fee: ${min_fee})")
        return best_chain