import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('cleaned_peelp.csv')

# Strip the header and replace spaces with underscores
df.columns = df.columns.str.strip().str.replace(' ', '_')


