import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from decimal import Decimal, ROUND_HALF_UP

# read the CSV file into a pandas DataFrame
df = pd.read_csv(
    r"C:\Users\Jason\Desktop\Data Analytics Portfolio Projects\Python Web Scraping\Expedia Webscraper\flight_information_dated.csv")

#####################################################################################################################################

# Average Price by Airline'
# remove the $ symbol from the 'Price' column
df['Price'] = df['Price'].str.replace('$', '', regex=False).astype(float)
# group the DataFrame by airline and calculate the mean price
avg_price_by_airline = df.groupby('Airline')['Price'].mean().reset_index()
# round the average price to 2 decimal places, using "banker's rounding"
avg_price_by_airline['Price'] = avg_price_by_airline['Price'].apply(
    lambda x: round(x, 2))
# round the average price to 2 decimal places, rounding up or down based on the 3rd decimal place
avg_price_by_airline['Price'] = avg_price_by_airline['Price'].apply(
    lambda x: float(Decimal(str(x)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)))
# create a Plotly table with the average price for each airline
fig = go.Figure(data=[go.Table(
    header=dict(values=['Airline', 'Average Price (USD)'],
                fill_color='black',
                align='left'),
    cells=dict(values=[avg_price_by_airline['Airline'], avg_price_by_airline['Price']],
               fill_color='rgba(0,0,0,0)',
               align='left'))
])
# set the title
fig.update_layout(title='', font=dict(
    color='white', family='Montserrat Regular'), plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)', autosize=False, width=410, height=91, margin={'l': 1, 'r': 1, 't': 1, 'b': 1},
                  )
# show the plot
# fig.show()
pio.write_image(fig, 'avgpricebyairline.png')
pio.write_json(fig, 'avgpricebyairline.json')

#####################################################################################################################################

# Average Price by Airline per Day
# group the DataFrame by airline, date, and the index of the date within each set of 5 rows
df['Date_Index'] = df.groupby(['Airline', 'Date']).cumcount() // 5
df_grouped = df.groupby(['Airline', 'Date', 'Date_Index'])[
    'Price'].mean().reset_index()
# create a line chart with the average price per day for each airline
fig = go.Figure()
colors = {'Alaska': ' #A304A2', 'Delta': '#faa53e', 'United': '#2d3290'}
for airline in df_grouped['Airline'].unique():
    airline_df = df_grouped[df_grouped['Airline'] == airline]
    fig.add_trace(go.Scatter(x=airline_df['Date'], y=airline_df['Price'],
                             mode='lines+markers', name=airline,
                             line=dict(color=colors[airline]),
                             marker=dict(color=colors[airline], size=5)))
# set the title and axis labels
fig.update_layout(title='', margin={'l': 1, 'r': 1, 't': 1, 'b': 1},
                  xaxis_title='Date', yaxis_title='Average Price (USD)',
                  legend=dict(orientation="h", yanchor="bottom", y=1.02,
                              xanchor="right", x=1, bgcolor='rgba(0,0,0,0)'),
                  plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                  font=dict(color='white', family='Montserrat Regular'),
                  xaxis=dict(showgrid=False, ticks='inside',
                             tickwidth=1, ticklen=5, tickcolor='white', linecolor='white'),
                  yaxis=dict(showgrid=False, ticks='inside', tickwidth=1, ticklen=5, tickcolor='white', linecolor='white'))
# show the plot
# fig.show()
pio.write_json(fig, 'avgpricebyairlinebyday.json')
pio.write_image(fig, 'avgpricebyairlinebyday.png')


######################################################################################################################################

# Flight Prices by Departure Time and Airline
# convert the 'Time' column to datetime format
df['Time'] = pd.to_datetime(df['Time'], format='%I:%M%p')

# create a dictionary to map airlines to numerical values
airline_dict = {'Alaska': ' #A304A2', 'Delta': '#faa53e', 'United': '#2d3290'}
# map the 'Airline' column to the corresponding color using the dictionary
df['Color'] = df['Airline'].map(airline_dict)
# create a Plotly scatter plot with the price and departure time of each flight
fig = go.Figure()
for airline, color in airline_dict.items():
    airline_df = df[df['Airline'] == airline]
    fig.add_trace(
        go.Scatter(
            x=airline_df['Time'],
            y=airline_df['Price'],
            mode='markers',
            marker=dict(
                size=8,
                color=color,
            ),
            name=airline,  # add name for legend
            # add airline and time info to the hover text
            text=airline_df['Airline'] + ', ' + \
            airline_df['Time'].dt.strftime('%I:%M%p')
        )
    )
# set the axis labels and title
fig.update_layout(
    margin={'l': 1, 'r': 1, 't': 1, 'b': 1},
    xaxis_title='Departure Time',
    yaxis_title='Price (USD)',
    title='',
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Montserrat Regular'),
    xaxis=dict(
        tickformat='%-I:%M%p',
        showgrid=False,
        ticks='inside',
        tickwidth=1,
        ticklen=5,
        tickcolor='white',
        linecolor='white'
    ),
    yaxis=dict(showgrid=False, ticks='inside',
               tickwidth=1, ticklen=5, tickcolor='white', linecolor='white'),
    # add legend
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    )
)
# show the plot
# fig.show()
pio.write_image(fig, 'avgpricebyairlinebytime.png')
pio.write_json(fig, 'avgpricebyairlinebytime.json')
