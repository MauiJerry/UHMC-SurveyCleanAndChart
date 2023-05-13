import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt

df = pd.read_csv('20230423_survey_0.csv')

print(df.columns)

# rename columns
print("now try renaming columns")
df = df.rename(columns={'What is the date and time of collection?':'DateTimeOfCollection'})
df = df.rename(columns={'Where are you recording the point?':'WhereRecording'})
df = df.rename(columns={'Are there no crops (fallow or pasture), one crop, or multiple crops growing in the field?':'FieldType'})
df = df.rename(columns={'Which crop(s) are present in the field?':'CropsInField'})
df = df.rename(columns={'Other - Which crop(s) are present in the field?':'OtherCropsInField'})
df = df.rename(columns={'[OPTIONAL] If you selected multiple crops in the previous question, is there a dominant crop?':'DominantCrop'})
df = df.rename(columns={'Other - [OPTIONAL] If you selected multiple crops in the previous question, is there a dominant crop?':'OtherDominantCrop'})
df = df.rename(columns={'[OPTIONAL] Additional notes':'Notes'})
df = df.rename(columns={'x': 'Longitude', 'y': 'Latitude'})

print("now export with new columns")
df.to_csv('20230423_survey_NewCol.csv', index=False)

# crop names have embedded backticks, which mess up python string processing
# so nix the characters out
df['CropsInField'] = df['CropsInField'].str.replace('`', '')  # Replace backtick character
# Split multi-value cells on comma separator
df['Crops'] = df['CropsInField'].str.split(',')

# Count unique crop names
exploded_crops = df.explode('Crops')
print(exploded_crops['Crops'].unique())
crop_counts = df.explode('Crops')['Crops'].value_counts()

# Display result
print(crop_counts)
crop_counts.to_csv("crop_counts.csv", index=False)
###################
# lots of Other, and Other are not counted in this.
# would be good to add them but then again, i got other things to do
# and this is good enough for the class Final for now

crop_counts = df.explode('Crops')['Crops'].loc[df['Crops'] != 'other'].value_counts()

print("Graph crop counts")

# create the bar plot
ax = crop_counts.plot.bar(x='Crop', y='Count', rot=90)

# set the x-axis label
ax.set_xlabel('Crop')

# set the y-axis label
ax.set_ylabel('Count')

# set the plot title
ax.set_title('Crop Counts')

# display the plot
plt.show()

print("Now calculate FarmIDs")

# assign FarmID to rows within 100m of each other
# Define function to calculate Haversine distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    distance = R * c
    return distance

# Define function to cluster points within 100 meters of each other

def label_farms(df, distance_threshold=0.5):
    farm_id = 0
    df['FarmID'] = -1
    # Sort DataFrame by CreationDate in ascending order
    df = df.sort_values('CreationDate')
    for i, row in df.iterrows():
        if df.loc[i, 'FarmID'] == -1:
            df.loc[i, 'FarmID'] = farm_id
            for j in range(i + 1, len(df)):
                # Check if the datetime difference is within 5 minutes and if the distance is within 500 meters
                if ((pd.Timestamp(df.loc[j, 'CreationDate']) - pd.Timestamp(
                        df.loc[i, 'CreationDate'])).seconds <= 300) and (
                        haversine(df.loc[i, 'Latitude'], df.loc[i, 'Longitude'], df.loc[j, 'Latitude'],
                                     df.loc[j, 'Longitude']) <= distance_threshold):
                    df.loc[j, 'FarmID'] = farm_id
            farm_id += 1
    return df

df = label_farms(df, distance_threshold=0.5)
print ("Save the df to FarmClustered.csv")

df.to_csv('20230423_survey_FarmClustered.csv', index=False)


