import requests
import json
import pandas as pd


base_url = "https://data.gov.sg/api/action/datastore_search?resource_id="

def get_data(dataset_id):
  url = base_url + dataset_id
  response = requests.get(url)

  if response.status_code == 200:
    data = response.json()['result']['records']
    return pd.DataFrame(data)
  else:
    print(f"Failed to retrieve data {response.status_code}")
    return None

# Insurance DatasetID
INSURANCE_DATA_ID = "d_ad861cfc83aa1f4ce6be45d31290dba8"

# Fetch and clean data
df = get_data(INSURANCE_DATA_ID)
df.fillna(0, inplace=True) #Handling missing values
df_transposed = df.transpose().reset_index()
df_transposed.columns = df_transposed.iloc[-1]
for col in df_transposed.columns[1:]:  # Skip index column
    df_transposed[col] = pd.to_numeric(df_transposed[col], errors="coerce")
df_cleaned = df_transposed[:62]

# Convert DataFrame to JSON format for frontend use
df_cleaned.to_json("insurance_data.json", orient="records", indent=4)
