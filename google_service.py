import time
import random

def perform_premium_search(query):
    
    print(f"\n  Service Provider: Searching Google for '{query}'...")
    
    time.sleep(1.5)
    
    results = [
        f"Result 1: Wikipedia article about {query}",
        f"Result 2: Latest news concerning {query}",
        f"Result 3: Top YouTube videos for {query}",
        "Result 4: Official documentation"
    ]
    
    print(" Service Provider: Data retrieved successfully.")
    return results