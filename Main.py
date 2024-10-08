import requests

def get_data():
    # URL where to get the data from
    url = 'https://api.etherscan.io/api'

    api_key = "JR9PWKZBEUESZW11T6GZXW8YC44638RUFW"

    # Define the parameters for the request
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": api_key
    }

    # Send the GET request to the Etherscan API
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the API returned data successfully
        if data["status"] == "1":
            print("Gas Oracle Data:", data["result"])
        else:
            print(f"Error: {data['message']}")
    else:
        print(f"Request failed with status code {response.status_code}")



if __name__ == '__main__':
    get_data()

