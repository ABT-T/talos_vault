import logging
import time
import json
import os

logger = logging.getLogger("TalosLocalAuth")

PENDING_FILE = os.path.join(os.path.expanduser("~"), "talos_request.json")
# ---------------------------------------------

class HumanApproval:
    def __init__(self, risk_threshold=1.0):
        self.risk_threshold = risk_threshold
    
    def requires_approval(self, amount):
        if amount >= self.risk_threshold:
            return True
        return False

    def request_approval(self, amount, to_address):
        print("\n" + "!"*50)
        print(f" SECURITY ALERT: Transaction paused.")
        print(f"Waiting for approval in Admin Dashboard...")
        print("!"*50 + "\n")

        request_data = {
            "id": int(time.time()),
            "amount": amount,
            "to": to_address,
            "status": "PENDING",
            "timestamp": time.ctime()
        }
        
        # نوشتن درخواست
        with open(PENDING_FILE, "w") as f:
            json.dump(request_data, f)

        # حلقه انتظار
        while True:
            try:
                if not os.path.exists(PENDING_FILE):
                    time.sleep(1)
                    continue

                with open(PENDING_FILE, "r") as f:
                    data = json.load(f)

                if data.get("status") == "APPROVED":
                    print(" Transaction APPROVED from Dashboard.")
                    self._cleanup()
                    return True
                
                elif data.get("status") == "REJECTED":
                    print(" Transaction REJECTED from Dashboard.")
                    self._cleanup()
                    return False
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error checking status: {e}")
                time.sleep(1)

    def _cleanup(self):
        if os.path.exists(PENDING_FILE):
            try:
                os.remove(PENDING_FILE)
            except:
                pass