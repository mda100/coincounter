import requests
import time

def fetch_address_info(address: str) -> dict:
    """
    Fetch address information from blockchain API.
    Returns address data and first 50 transactions (demo limitation).
    note: for production, fetch all transactions through batch requests.
    """
    url = f"https://blockchain.info/rawaddr/{address}?limit=50"
    
    retries = 3
    base_delay = 5
    
    while retries > 0:
        try:
            time.sleep(base_delay)
            
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            
            return {
                "n_tx": data.get("n_tx", 0),
                "n_unredeemed": data.get("n_unredeemed", 0),
                "total_received": data.get("total_received", 0),
                "total_sent": data.get("total_sent", 0),
                "final_balance": data.get("final_balance", 0),
                "transactions": data.get("txs", [])  # First 50 transactions only
            }
            
        except requests.exceptions.RequestException as e:
            retries -= 1                
            if retries: 
                if hasattr(e, 'response') and e.response.status_code == 429: # rate limited
                    wait_time = 60 * (2 ** (3 - retries))
                    print(f"Rate limited, waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    wait_time = 10 * (3 - retries)
                    print(f"Request failed, retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            else:
                raise Exception(f"Request to {url} failed after 3 retries: {str(e)}")