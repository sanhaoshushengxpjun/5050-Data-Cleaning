import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

file_path = '/mnt/data/FloodArchive-1.xlsx'
data = pd.read_excel(file_path)


# Replace missing values and zeros in the 'GlideNumber' column with 'N/A'
data['GlideNumber'] = data['GlideNumber'].replace(0, 'N/A').fillna('N/A')


# Define a mapping dictionary for standardizing country names
country_corrections = {
    'BANGALDESH': 'BANGLADESH',
    'BANGLEDESH': 'BANGLADESH',
    'BURMA': 'MYANMAR',
    'BURMA/MYANMAR': 'MYANMAR',
    'COLOMBIA': 'COLOMBIA',
    'COLUMBIA': 'COLOMBIA',
    # Assuming 'CONGO' refers to 'REPUBLIC OF CONGO' for consistency
    'CONGO': 'REPUBLIC OF CONGO',
    'CONGO REPUBLIC': 'REPUBLIC OF CONGO',
    "COTE D'IAVOIR": "CÔTE D'IVOIRE",
    "COTE D'IVOIRE": "CÔTE D'IVOIRE",
    'CZECH REPUBLIC': 'CZECH REPUBLIC',
    'CZECHOSLOVAKIA': 'CZECH REPUBLIC',  # Using current country name
    'DEMOCRATIC  REPUBLIC OF THE CONGO': 'DEMOCRATIC REPUBLIC OF THE CONGO',
    'DEMOCRATIC REPUBLIC CONGO': 'DEMOCRATIC REPUBLIC OF THE CONGO',
    'DEMOCRATIC REPUBLIC OF CONGO': 'DEMOCRATIC REPUBLIC OF THE CONGO',
    'EL SALVADOR': 'EL SALVADOR',
    'EL SAVADOR': 'EL SALVADOR',
    'KAZAHKSTAN': 'KAZAKHSTAN',
    'KAZAKHSTAN': 'KAZAKHSTAN',
    'MADAGASCAR': 'MADAGASCAR',
    'MADASCAR': 'MADAGASCAR',
    'MOLDAVA': 'MOLDOVA',
    'MOLDOVA': 'MOLDOVA',
    'MYANAMAR': 'MYANMAR',
    'MYANMAR': 'MYANMAR',
    'NIGER': 'NIGER',
    'NIGERIA': 'NIGERIA',
    'PAPUA NEW GUINEA': 'PAPUA NEW GUINEA',
    'PAPUA NEW GUNEA': 'PAPUA NEW GUINEA',
    'PHILIPINES': 'PHILIPPINES',
    'PHILIPPINE': 'PHILIPPINES',
    'PHILIPPINES': 'PHILIPPINES',
    'PHILLIPPINES': 'PHILIPPINES'
}

def clean_country_names(country):
    # Remove extra spaces, convert to uppercase, and apply corrections
    country = country.strip().upper()
    if country in country_corrections:
        return country_corrections[country]
    return country

# Apply corrections to the Country column
data['Country'] = data['Country'].apply(
    lambda x: country_corrections.get(x, x))

# Clean the Country column
data['Country'] = data['Country'].apply(clean_country_names)
# Split entries that contain multiple countries and explode into separate rows
data_exploded = data.assign(
    Country=data['Country'].str.split(' AND ')).explode('Country')

# Apply corrections again if there are leftovers from splitting
data_exploded['Country'] = data_exploded['Country'].apply(
    lambda x: country_corrections.get(x.strip(), x.strip()))

# Show the unique country names after cleanup and the head of the exploded data
data_exploded.head(), data_exploded['Country'].unique()



# Fill missing values in 'OtherCountry' with 'N/A'
data['OtherCountry'] = data['OtherCountry'].fillna('N/A')
# Apply the same standardization function used for 'Country' to 'OtherCountry' again after review
data_exploded['OtherCountry'] = data_exploded['OtherCountry'].apply(
    clean_country_names)

# Display the cleaned and standardized unique values in 'OtherCountry' to verify corrections
data_exploded['OtherCountry'].unique()

# Display the corrected unique country names
corrected_unique_countries = sorted(data_exploded['Country'].unique())
corrected_unique_other_countries = sorted(
    data_exploded['OtherCountry'].unique())

corrected_unique_countries, corrected_unique_other_countries

# Further refine the country name corrections to match international standards
international_corrections = {
    'CZECH REPUBLIC': 'CZECHIA',  # Reflecting modern usage
    'MACEDONIA': 'NORTH MACEDONIA',  # Reflecting modern usage
    'BURMA': 'MYANMAR',
    'SWAZILAND': 'ESWATINI',  # Reflecting modern usage
    'ZAIRE': 'DEMOCRATIC REPUBLIC OF THE CONGO',
    'ALASKA': 'USA',  # Alaska is part of the USA
    'TAIWAN': 'TAIWAN',  # Officially recognized as Taiwan for international dealings
    # Specify which Virgin Islands if not already done
    'VIRGIN ISLANDS': 'U.S. VIRGIN ISLANDS',
    'SIBERIA': 'RUSSIA',  # Siberia is a region in Russia
    'HONG KONG': 'HONG KONG',  # Special administrative region of China
    'MACAU': 'MACAU'  # Special administrative region of China
}

# Apply international corrections to both 'Country' and 'OtherCountry'
data_exploded['Country'] = data_exploded['Country'].apply(
    lambda x: international_corrections.get(x, x))
data_exploded['OtherCountry'] = data_exploded['OtherCountry'].apply(
    lambda x: international_corrections.get(x, x))

# Verify the adjustments
final_countries = sorted(data_exploded['Country'].unique())
final_other_countries = sorted(data_exploded['OtherCountry'].unique())

# Check if they are identical now
identical_countries = set(final_countries) == set(final_other_countries)
final_countries, final_other_countries, identical_countries

# Handling special cases and unifying columns
# Update the function to include special cases like 'Alaska' and 'Taiwan'
special_cases = {
    'ALASKA': 'USA',  # Alaska is part of the USA
    'TAIWAN': 'TAIWAN'  # Taiwan is treated as a separate entity
}

data['Country'] = data['Country'].apply(lambda x: special_cases.get(x, x))
data['OtherCountry'] = data['OtherCountry'].apply(
    lambda x: special_cases.get(x, x))



unique_validation_values = data['Validation'].unique()
print("Unique values before cleaning:", unique_validation_values)

# Standardize text format to title case for consistency
data['Validation'] = data['Validation'].str.title()

# Dictionary to merge similar or duplicative values
validation_corrections = {
    "Flood LIst": "FloodList",
    "Floodlist": "FloodList",
    "Flood LIst": "FloodList",
    "Floodlist And Glide": "FloodList and GLIDE",
    "Floodlist And News": "FloodList and News",
    "Floodlist And Other Media": "FloodList and Other Media",
    "News Reports": "News",
    "News Media": "News",
    "News": "News",
    "Dfo": "DFO",
    "Nasa-Earth-Observatory": "NASA Earth Observatory",
    "Nasa Flood Alerts": "NASA Flood Alerts",
    "Usgs Gauging": "USGS Gauging",
    "Tropical Storm Track": "Tropical Storm Track",
    "River Gauging": "River Gauging",
    "International Charter": "International Charter",
    "Gfms Prediction": "GFMS Prediction",
    "0": "N/A"  # Assuming '0' represents missing or non-applicable data
}

# Apply corrections to merge similar or duplicative values
data['Validation'] = data['Validation'].apply(
    lambda x: validation_corrections.get(x, x))

# Display unique values after corrections to verify changes
unique_validation_values_corrected = data['Validation'].unique()
print("Unique values after cleaning:", unique_validation_values_corrected)



# Assuming 'data' is your DataFrame containing the flood event information

# Calculate duration, flood magnitude, and categorize the magnitudes
data['Duration'] = (data['Ended'] - data['Began']).dt.days + 1
data['Flood Magnitude'] = np.log(
    data['Duration'] * data['Severity'] * data['Area'])
data['Magnitude Level'] = pd.cut(data['Flood Magnitude'], bins=5, labels=[
                                 "Very Low", "Low", "Moderate", "High", "Very High"])

# Group the data by Country and Magnitude Level, then count the occurrences
country_flood_counts = data.groupby(
    ['Country', 'Magnitude Level']).size().unstack(fill_value=0)

# Select the top five countries based on the total number of floods
top_countries = country_flood_counts.sum(axis=1).nlargest(5)
top_countries_detail = country_flood_counts.loc[top_countries.index]

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(12, 8))
top_countries_detail.plot(kind='bar', ax=ax, stacked=True, colormap='viridis')

# Adding labels and title to the plot
ax.set_title('Distribution of Flood Magnitudes in Top Five Countries')
ax.set_xlabel('Country')
ax.set_ylabel('Number of Flood Events')
ax.legend(title='Magnitude Level')

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Ensure everything fits well visually
plt.tight_layout()

# Display the plot
plt.show()
