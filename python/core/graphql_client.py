import requests


def fetch_product_data(shop, key, referer_url):
    url = "https://gql.tokopedia.com/graphql/PDPGetLayoutQuery"

    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "referer": referer_url,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "x-device": "desktop",
        "x-price-center": "true",
        "x-source": "tokopedia-lite",
        "x-tkpd-akamai": "pdpGetLayout",
        "x-tkpd-lite-service": "zeus",
        "x-version": "5116ab0",
        "bd-device-id": "7416638437661836818",
    }

    query_payload = {
        "operationName": "PDPGetLayoutQuery",
        "variables": {
            "shopDomain": shop,
            "productKey": key,
            "layoutID": "",
            "apiVersion": 1,
            "userLocation": None,
            "extParam": "src%3Dshop%26whid%3D18643634",
            "tokonow": None,
            "deviceID": "",
        },
        "query": """
        query PDPGetLayoutQuery($shopDomain: String, $productKey: String, $layoutID: String, $apiVersion: Float, $userLocation: pdpUserLocation, $extParam: String, $tokonow: pdpTokoNow, $deviceID: String) {
          pdpGetLayout(shopDomain: $shopDomain, productKey: $productKey, layoutID: $layoutID, apiVersion: $apiVersion, userLocation: $userLocation, extParam: $extParam, tokonow: $tokonow, deviceID: $deviceID) {
            components {
              name
              type
              position
              data {
                children {
                  productID
                  price
                  optionName
                  productURL
                }
              }
            }
          }
        }
        """,
    }

    try:
        response = requests.post(url, json=query_payload, headers=headers, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("API berhasil merespons!")
            return response.json()
        else:
            print(f"ERROR: {response.status_code}, {response.text}")
            raise Exception(f"Error fetching data: {response.status_code}")
    except requests.exceptions.Timeout:
        print("Request timeout! API tidak merespons dalam batas waktu.")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None
