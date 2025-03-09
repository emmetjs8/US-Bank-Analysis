"""
initDataFiles.py

This script initializes and downloads economic data series from the FRED API for the H8 and H41 reports, 
saving them to structured files. It retrieves series IDs and corresponding file paths, 
fetches the data using `FredApiClient`, processes it into a two-dimensional list, 
and writes it to files using a null character (`\0`) as a delimiter.

Dependencies:
    - `seriesIdParser.py`: Provides series ID and file path mappings.
    - `fredClient.py`: Handles API requests to the FRED database.
    - `pandasHelperFunctions.py`: Converts Pandas Series to 2D lists.
    - 'time': used to pause request to avoid rate limiter error

Data Storage Format:
    Each output file contains lines formatted as:
        Date<null character>Value\n
    Example:
        2000-06-28\0211.4984
        2000-07-05\0212.0107

Usage:
    Simply run the script to download and save the initial dataset.

Author: Emmet Szewczyk
Date: 3/9/25
"""

from getApiKey import *
from seriesIdParser import getSeriesIdsAndFilepaths
from fredClient import FredApiClient
from pandasHelperFunctions import seriesToTwoDimensionalList
import time

def writeParsedDataToFile(fileName: str, parsedData: list) -> bool:
    """
    Writes parsed time-series data to a file.

    Args:
        fileName (str): The file path where data should be stored.
        parsedData (list): A list of [date, value] pairs.

    Returns:
        bool: True if writing succeeds.
    """
    try:
        with open(fileName, "w") as file:
            for line in parsedData:
                # Write each line in "Date<null char>Value\n" format
                file.write(f"{line[0]}\0{line[1]}\n")
        return True
    except Exception as e:
        print(f"Error writing to {fileName}: {e}")
        return False

# Set up API key and client
apiKey = getApiKey
client = FredApiClient(apiKey)

# Get series IDs and file paths
H8_SeriesIds_Filepaths = getSeriesIdsAndFilepaths()

# Display metadata and begin downloading series data
for ufKey, datasets in H8_SeriesIds_Filepaths.items():
    print(f"Units & Frequency: {ufKey}")  # Print the units and frequency (e.g., Weekly-SA)
    
    # Iterate through each dataset in the current frequency and unit category
    for dataset, (seriesID, filePath) in datasets.items():
        print(f"  Dataset: {dataset}")  # Print the dataset name

        # Fetch the time-series data from the FRED API using the series ID
        data = client.getSeries(seriesID)
        
        # Convert the fetched data into a 2D list format (i.e., [[date, value], ...])
        parsedData = seriesToTwoDimensionalList(data)
        
        # Attempt to write the parsed data to the corresponding file path
        success = writeParsedDataToFile(filePath, parsedData)

        # Check if writing data was successful and print the appropriate message
        if success:
            print(f"    Data for {seriesID} successfully written to: {filePath}")
        else:
            print(f"    Failed to write data for {seriesID} to {filePath}")
        
        # Pause for 5 seconds to avoid hitting API rate limits
        time.sleep(5)

 