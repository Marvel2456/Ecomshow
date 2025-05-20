import requests

def get_bitcoin_conversion_rate():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
        return data['bitcoin']['usd']
    except Exception as e:
        print(f"Error fetching Bitcoin conversion rate: {e}")
        return None
    
def get_ethereum_conversion_rate():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
        return data['ethereum']['usd']
    except Exception as e:
        print(f"Error fetching Ethereum conversion rate: {e}")
        return None