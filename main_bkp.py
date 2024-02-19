import requests


def call_api(endpoint):
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()  # Assuming the response is JSON
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


def main():
    endpoint = "https://server.duinocoin.com/users/nanomachine"  # Replace this with your actual endpoint
    data = call_api(endpoint)
    if data:
        # Display balance without decimal
        balance = data['result']['balance']['balance']
        print("B:", int(balance))

        # Sum all miners' hashrate
        miners_hashrate_sum = int(sum(miner['hashrate'] for miner in data['result']['miners']) / 1000)
        print("H:", miners_hashrate_sum, "kH/s")


if __name__ == "__main__":
    main()
