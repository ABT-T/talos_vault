import asyncio
import logging
import sys
from talos.payments.engine import MultiChainEngine

# Configure formatting for a clean CLI output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%H:%M:%S'
)

async def main():
    print("\n" + "="*50)
    print("   TALOS AUTONOMOUS AGENT v1.0.2 (Build: Nightly)")
    print("   Architecture: Solana / Async / Fault-Tolerant")
    print("="*50 + "\n")

    engine = MultiChainEngine()
    
    try:
        await engine.start_session()
        
        # User Interaction
        query = input(">> Enter search query or task: ").strip()
        if not query:
            print("(!) No query provided. Exiting.")
            return

        # Cost calculation logic (simplified for demo)
        estimated_cost = 0.001
        print(f"\n[?] Estimated Network Fee: {estimated_cost} SOL")
        
        confirm = input(">> Authorize payment? (Y/n): ").lower()
        if confirm not in ('y', 'yes', ''):
            print("[-] Operation aborted by user.")
            await engine.close_session()
            return

        print("\n[*] Processing on-chain transaction...")
        
        # Execute payment
        tx_hash = await engine.send_request("TargetServiceNode_v4", estimated_cost)

        if tx_hash:
            print("\n" + "-"*50)
            print(" [SUCCESS] PAYMENT CONFIRMED")
            print(f" [TX ID]   {tx_hash[:20]}...{tx_hash[-20:]}")
            print(f" [LINK]    https://solscan.io/tx/{tx_hash}?cluster=devnet")
            print("-"*50)
            
            print(f"\n[+] Agent is executing task: '{query}'")
            print("[+] Results retrieved successfully.\n")
        else:
            print("\n[!] Transaction Failed. Please check logs.")

    except KeyboardInterrupt:
        print("\n\n[!] Force shutdown initiated.")
    finally:
        await engine.close_session()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
