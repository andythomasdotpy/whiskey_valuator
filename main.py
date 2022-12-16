import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
import mplcursors


# Filter bottle exact search criteria.
NAME_OF_BOTTLE = "Weller Full Proof"


def name_filter_auto(bottle_input_auto):
    if bottle_input_auto == NAME_OF_BOTTLE:
        return True
    else:
        return False


x_rate = 1.16

# Request whiskey data
url = "https://whiskyauctioneer.com/auction-search?text=weller+full+proof&sort=field_reference_field_end_date+DESC&items_per_page=500"
r = requests.get(url, auth=('user', 'pass'))
print(r)

# Soupify data
soup = BeautifulSoup(r.text, 'html.parser')
print(soup)

# Extract each bottle from site to a list
gen_list = soup.select("div .views-row")
num_bottles_returned = len(gen_list)
print(f"{num_bottles_returned} bottle prices included")

# Create header names
header = ["bottle_name", "sales_status", "price_usd", "sales_date"]

# Open a csv file for writting/create if it doesn't exist
with open('bottle_info.csv', 'w') as file:
    writer = csv.writer(file)

    # Write the initial header row
    writer.writerow(header)

    # Iterate through list of bottles
    for item in gen_list:
        #Create temp list for each row
        row = []

        # Parse bottle name and sales status
        bottle_name = item.find(class_="protitle").contents[0]
        sales_status = item.find_all(class_="label")[1].contents[0]

        # Optional Bottle Filter (auto)
        bool_filter = name_filter_auto(bottle_name)

        # Only add bottles that pass the filter (if filter activiated)
        if bool_filter == True:

            # Only include bottles if auction has closed "Winning Bid:" status means auction has closed
            if sales_status == "Winning Bid:":
                # Create a list called "price_list" will pull the price and sale date and insert into a list
                price_list = item.find_all(class_="uc-price")

                # Extract price from list and assign to varible "raw_price"
                raw_price = price_list[0].contents[0][1:]

                # Remove comma's from price
                price_usd = raw_price.replace(",", "")

                # Convert price from string to int and convert from pounds to dollars
                price_int = int(int(price_usd) * x_rate)

                # Extract date from list and assign to variable "sales_date"
                sales_date = price_list[1].contents[0]

                # Convert date from string to datetime object
                date_time_obj = datetime.strptime(sales_date, '%d.%m.%y')

                # Add all the variables to a temp list called "row"
                row.append(bottle_name)
                row.append(sales_status)
                row.append(price_int)
                row.append(date_time_obj)

                title_needed = True
                if title_needed:
                    chart_title = bottle_name
                    title_needed = False

                # Add row to csv file
                writer.writerow(row)


# Plot prices
df = pd.read_csv('bottle_info.csv')

# Remove time from datetime object
df['sales_date'] = pd.to_datetime(df['sales_date']).dt.date

# Create chart and print to screen
sns.set(rc = {'figure.figsize':(15,8)})
# sns.lineplot(data=df, x="sales_date", y="price_usd").set(title=bottle_name)
sns.lineplot(data=df, x="sales_date", y="price_usd").set()
sns.scatterplot(data=df, x="sales_date", y="price_usd")
plt.xlabel('Date of Sale')
plt.ylabel('Price (converted to USD)')
plt.xticks(rotation=295)
mplcursors.cursor(hover=True)
plt.show()