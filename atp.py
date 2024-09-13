import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the CSV file
df = pd.read_csv('atp.csv')

# Convert 'Start_Time' to datetime
df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='%m/%d/%Y %H:%M:%S %p')

# Convert 'TargetVol_(mL)' and 'Volume' to numeric
df['TargetVol_(mL)'] = pd.to_numeric(df['TargetVol_(mL)'], errors='coerce')
df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

# Remove rows where 'TargetVol_(mL)' < 3100
df = df[df['TargetVol_(mL)'] >= 3100]

# Remove rows where 'Chemical' contains "BUFFER"
df = df[~df['Chemical'].str.contains("BUFFER", na=False)]

# Limit 'Bath' values to A to D
df = df[df['Bath'].isin(['A', 'B', 'C', 'D'])]

# Create the summary table
df_limits = df.groupby('Chemical')['TargetVol_(mL)'].max().reset_index()
df_limits['UCL'] = df_limits['TargetVol_(mL)'] + 300
df_limits['LCL'] = df_limits['TargetVol_(mL)'] - 300

# Create the subplots
fig = make_subplots(rows=4, cols=4, subplot_titles=[f"{chemical} - Bath {bath}" for chemical in df['Chemical'].unique() for bath in df['Bath'].unique()])

# Create the line charts
chemicals = df['Chemical'].unique()
baths = df['Bath'].unique()

for i, chemical in enumerate(chemicals):
    for j, bath in enumerate(baths):
        row = i + 1
        col = j + 1
        
        # Filter data
        df_plot = df[(df['Chemical'] == chemical) & (df['Bath'] == bath)]
        
        # Find limits for the current chemical
        limits = df_limits[df_limits['Chemical'] == chemical].iloc[0]
        target_vol = limits['TargetVol_(mL)']
        ucl = limits['UCL']
        lcl = limits['LCL']
        
        # Add trace for Volume
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=df_plot['Volume'], mode='lines+markers', marker=dict(size=4, color='blue'), name='Volume'),
                      row=row, col=col)
        
        # Add trace for TargetVol_(mL)
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=[target_vol] * len(df_plot), mode='lines', line=dict(color='black', width=2), name='TargetVol_(mL)', showlegend=False),
                      row=row, col=col)
        
        # Add trace for UCL
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=[ucl] * len(df_plot), mode='lines', line=dict(color='red', width=2, dash='dash'), name='UCL', showlegend=False),
                      row=row, col=col)
        
        # Add trace for LCL
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=[lcl] * len(df_plot), mode='lines', line=dict(color='red', width=2, dash='dash'), name='LCL', showlegend=False),
                      row=row, col=col)
        
        # Add yellow lines at 1 standard deviation
        std_dev = df_plot['Volume'].std()
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=[target_vol + std_dev] * len(df_plot), mode='lines', line=dict(color='yellow', width=2, dash='dot'), name='+1 Std Dev', showlegend=False),
                      row=row, col=col)
        fig.add_trace(go.Scatter(x=df_plot['Start_Time'], y=[target_vol - std_dev] * len(df_plot), mode='lines', line=dict(color='yellow', width=2, dash='dot'), name='-1 Std Dev', showlegend=False),
                      row=row, col=col)

# Update layout
fig.update_layout(
    title='ATP Dispense - Run Charts',
    height=1200,  # Increase height
    showlegend=False
)

# Save as pickle file
import pickle
with open('atp-new.pkl', 'wb') as f:
    pickle.dump(fig, f)

# Show the figure
fig.show()
