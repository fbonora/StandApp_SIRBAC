#!/usr/bin/env python

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("www.dati.lombardia.it", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.dati.lombardia.it,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("4mr7-hfsh", limit=200)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

print(results_df)
