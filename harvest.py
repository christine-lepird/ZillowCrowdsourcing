import zillow
import pandas as pd
from pprint import pprint

api = zillow.ValuationApi()
with open("zillow.key", 'r') as f:
    key = f.readline().replace("\n", "")

df_in = pd.read_csv("media.csv")

df_out = pd.DataFrame()

for _, row in df_in.iterrows():
	lst = row["City"].split(" ")
	postal_code = lst[-1]
	other = " ".join(lst[:-1])
	address = row["Address"] + " " + other

	print("Pulling data for: " + address + " " + postal_code)

	data = api.GetDeepSearchResults(key, address, postal_code)

	df = pd.DataFrame({**data.__dict__, 
		               **data.extended_data.__dict__, 
		               **data.zestimate.__dict__, 
		               **data.links.__dict__}, index = [0])

	df_out = df_out.append(df, ignore_index=True)

df_out.to_csv("data.csv", index=False)