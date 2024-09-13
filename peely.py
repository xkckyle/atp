import csv

# Remove columns with blank headers from "peelp.csv"
input_file = 'peelp.csv'
output_file = 'peelp_cleaned.csv'

# Open the CSV and remove columns with blank headers
with open(input_file, mode='r') as infile:
    reader = csv.reader(infile)
    headers = next(reader)
    
    # Find indices of non-blank headers
    valid_indices = [i for i, header in enumerate(headers) if header.strip()]
    
    # Filter out columns with blank headers
    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([headers[i] for i in valid_indices])
        
        # Write the rest of the rows
        for row in reader:
            writer.writerow([row[i] for i in valid_indices])


import pandas as pd
import numpy as np

# Load the cleaned CSV using pandas
df = pd.read_csv('peelp_cleaned.csv')

# Strip and replace spaces with underscores in column headers
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Convert Coll_Dt to datetime and filter the rows after "01-JAN-24"
df['Coll_Dt'] = pd.to_datetime(df['Coll_Dt'], format='%d-%a-%y', errors='coerce')
# df = df[df['Coll_Dt'] > ('2024-01-01')]

# Melt the 'Point' columns into one 'Point' column and 'Value' column
point_columns = ['Point_A', 'Point_B', 'Point_C', 'Point_D', 'Point_E', 'Point_F', 'Point_Left', 'Point_Center', 'Point_Right']
df_melted = pd.melt(df, id_vars=['Coll_Dt', 'Matrix_Type', 'Location', 'Proj_Num', 'Sealer'], 
                    value_vars=point_columns, var_name='Point', value_name='Value')

# Set 'Value' to numeric, force errors to NaN and filter out non-numeric rows
df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')
df_melted = df_melted.dropna(subset=['Value'])

# Remove rows where 'Proj_Num' is blank
df_melted = df_melted[df_melted['Proj_Num'].notna() & df_melted['Proj_Num'].str.strip() != '']

# View the final dataframe
print(df_melted.head)


import plotly.express as px
import pandas as pd

# Sample data - replace this with the actual 'df_melted' from the previous step
df = df_melted  # Assuming df_melted is already filtered

# Filter the columns needed for the plot
# df['Coll_Dt'] = pd.to_datetime(df['Coll_Dt'], format='%d-%a-%y', errors='coerce')
# df = df[df['Matrix_Type']=='Polyester Barrier Pouch']
# 'Polyester Barrier Pouch'
# print(df.head)
# Define a function to update the chart based on selected Matrix_Type
def update_chart(selected_matrix_type):
    # Filter the data by selected Matrix_Type
    filtered_df = df[df['Matrix_Type'] == selected_matrix_type]

    # Create a scatter plot using Plotly Express
    fig = px.scatter(filtered_df, 
                     x='Coll_Dt', 
                     y='Value', 
                     color='Sealer', 
                     title=f'Scatter Plot of Values over Time for {selected_matrix_type}',
                     labels={'Coll_Dt': 'Collection Date', 'Value': 'Value'},
                     template="plotly_white")

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="Collection Date",
        yaxis_title="Value",
        legend_title="Sealer",
        transition_duration=500,
    )
    
    return fig

# Generate the initial plot for the first Matrix_Type in the list
initial_matrix_type = 'Polyester Barrier Pouch'#df['Matrix_Type'].unique()[7]
fig = update_chart(initial_matrix_type)

# Add dropdown to filter by Matrix_Type
matrix_types = df['Matrix_Type'].unique()

dropdown_buttons = [
    {
        'label': matrix_type,
        'method': 'update',
        'args': [{'visible': [matrix_type == mt for mt in matrix_types]}]  # Show/Hide traces
    }
    for matrix_type in matrix_types
]

fig.update_layout(
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'down',
        'showactive': True,
    }]
)

# Show the plot
fig.show()