import requests

# Change this to localhost while developing
PORTFOLIO_API = "http://localhost:3000/api/profile"

# After deployment use:
# PORTFOLIO_API = "https://portfolio-ofanushka.vercel.app/api/profile"


def get_portfolio_data():
    try:
        response = requests.get(PORTFOLIO_API, timeout=10)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    data = get_portfolio_data()
    print(data)