import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# # Step 1: Create the dataset with 30 rows
# np.random.seed(42)  # For reproducible results
# dates = pd.date_range(start="2024-09-01", periods=30)
# chemicals = ['Chem1', 'Chem2', 'Chem3', 'Chem4']
# Baths = ['B1', 'B2', 'B3']
# Stations = ['S1', 'S2', 'S3', 'S4']
# Volumes = np.random.uniform(10, 30, size=30)  # Random Volumes between 10 and 30
# targets = np.random.randint(0, 2, size=30)   # Random 0s and 1s

# # Create the DataFrame
# df = pd.DataFrame({
#     'Start_Time': np.random.choice(dates, size=30),
#     'chemical': np.random.choice(chemicals, size=30),
#     'Bath': np.random.choice(Baths, size=30),
#     'Station': np.random.choice(Stations, size=30),
#     'Volume': Volumes,
#     'target': targets
# })
 
# 
df = pd.read_csv('atp.csv'); df['Start_Time'] = pd.to_datetime(df['Start_Time'],format='%m/%d/%Y %H:%M:%S %p'); 
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'])

# pre-filter for now...
df = df[df['TargetVol_(mL)'] > 3000]


#
Baths = df['Bath'].unique(); print(Baths)
Chemicals = df['Chemical'].unique(); print(Chemicals)
Stations = df['Station'].unique(); print(Stations)
#,Start_Time,Batch_ID,Phase,TargetVol_(mL),Volume,Station,Chemical,Bath


# Step 2: Create a Plotly figure with subplots (2 columns and 4 rows)
fig = make_subplots(rows=4, cols=2, subplot_titles=("Scatter 1", "Box 1", "Scatter 2", "Box 2",
                                                    "Scatter 3", "Box 3", "Scatter 4", "Box 4"))

# Step 3: Add scatter plots with trend lines and red 1-sigma lines (1st column)
for i in range(4):
    scatter_data = df[df['Chemical'] == Chemicals[i % len(Chemicals)]]  # Filter data for each Bath
    
    # Scatter plot with marker size set to 1
    scatter_fig = px.scatter(scatter_data, x='Start_Time', y='Volume', color='Bath', trendline='ols')
    
    # Calculate 1-sigma (standard deviation)
    sigma = scatter_data['Volume'].std()

    # Add scatter plot traces with marker size 1
    for trace in scatter_fig['data']:
        trace.marker.update(size=1)
        fig.add_trace(trace, row=i+1, col=1)

    # Add red lines at +1 and -1 sigma
    fig.add_trace(
        go.Scatter(x=scatter_data['Start_Time'], 
                   y=[scatter_data['Volume'].mean() + sigma] * len(scatter_data), 
                   mode='lines', line=dict(color='red', dash='dash'), 
                   name=f'+1 Sigma'),
        row=i+1, col=1
    )
    fig.add_trace(
        go.Scatter(x=scatter_data['Start_Time'], 
                   y=[scatter_data['Volume'].mean() - sigma] * len(scatter_data), 
                   mode='lines', line=dict(color='red', dash='dash'), 
                   name=f'-1 Sigma'),
        row=i+1, col=1
    )

# Step 4: Add box plots in the 2nd column (color by Station, x as Bath)
for i in range(4):
    box_data = df[df['Station'] == Stations[i % len(Stations)]]  # Filter data for each Station
    box_fig = px.box(box_data, x='Bath', y='Volume')

    # Add box plot traces
    for trace in box_fig['data']:
        fig.add_trace(trace, row=i+1, col=2)

# Step 5: Update layout for better visualization
fig.update_layout(height=1000, width=1200, title_text="Scatter with Trendlines and 1 Sigma (Column 1) and Box Plots (Column 2)")

# Step 6: Show the figure
fig.show()
