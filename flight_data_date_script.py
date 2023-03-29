import pandas as pd
from datetime import datetime, timedelta

# Read the csv file into a pandas DataFrame
df = pd.read_csv(r"C:\Users\Jason\Desktop\Data Analytics Portfolio Projects\Python Web Scraping\Expedia Webscraper\Expedia_BZN_PHX_Flight_Information.csv",
                 header=0, names=['Airline', 'Time', 'Price'])

# Initialize the date counter and the date column
date_counter = 0
date_list = []

# Iterate over the rows of the DataFrame
for i, row in df.iterrows():

    # Assign the date for the current row based on the date counter
    if i % 5 == 0:
        date = datetime(2023, 2, 17) + timedelta(days=date_counter)
        date_counter += 1
    date_list.append(date)

# Add the date column to the DataFrame
df['Date'] = date_list

# Save the updated DataFrame to a new CSV file
df.to_csv('flight_information_dated.csv', index=False)
