"""
initDataFiles.py

This script initializes and downloads economic data series from the FRED API for the H8 and H41 reports, 
saving them to structured files. It ensures that necessary files exist before the main program runs. 

Once the system is fully operational, another script will be developed to read in series metadata 
with precomputed file paths, eliminating the need for these initialization functions.

Dependencies:
    - `seriesIdParser.py`: Provides series ID and file path mappings.
    - `fredClient.py`: Handles API requests to the FRED database.
    - `pandasHelperFunctions.py`: Converts Pandas Series to 2D lists.
    - `time`: Used to pause requests to avoid rate limiter errors.

Data Storage Format:
    Each output file contains lines formatted as:
        Date<null character>Value\n
    Example:
        2000-06-28\0211.4984
        2000-07-05\0212.0107

Usage:
    Run the script to download and save the initial datasets.

Author: Emmet Szewczyk
Date: 3/11/25
"""

from getApiKey import *
from seriesIdParser import parseH8Series, parseH41Series
from fredClient import FredApiClient
from pandasHelperFunctions import seriesToTwoDimensionalList
import time

def saveH8FileNames(fileName: str) -> None:
    """
    This function writes the filename of a downloaded H8 data file to a file database
    in data/H8/filenames.txt for easy access to data during application run time.

    Args:
        filename (str): The file path to save in the H8 file database
    
    Returns:
        None (Just writes filename to file)
    """
    saveFileNameTo = "data/H8/filenames.txt"

    with open(saveFileNameTo, "a") as file:
        file.write(fileName + "\n")

def saveH41FileNames(fileName: str) -> None:
    """
    This function writes the filename of a downloaded H41 data file to a file database
    in data/H41/filenames.txt for easy access to data during application run time.

    Args:
        filename (str): The file path to save in the H41 file database
    
    Returns:
        None (Just writes filename to file)
    """
    saveFileNameTo = "data/H41/filenames.txt"

    with open(saveFileNameTo, "a") as file:
        file.write(fileName + "\n")

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

def downloadH8Data(H8_SeriesIds_Filepaths: dict, client: FredApiClient) -> None: 
    """
    downloadH8Data

    Downloads and saves time-series data for the H8 report using series IDs and file paths.

    This function iterates through the structured dictionary of H8 series metadata, 
    retrieves the corresponding data from the FRED API, and saves it to designated file paths. 
    Upon succesful download, parsing, and file writing of time-series data, the function saves file names 
    in a filename databse for the H8 data set.

    To prevent exceeding API rate limits, it includes a delay between requests.

    Parameters:
        - H8_SeriesIds_Filepaths (dict): 
            A nested dictionary where keys represent units & frequency categories 
            (e.g., "Weekly-SA") and values map dataset names to tuples of (seriesID, filePath).
        - client (FredApiClient): 
            An instance of `FredApiClient` used to fetch time-series data from the FRED database.

    Returns:
        - None (writes data to files and prints status messages).
    """
    # Display metadata and begin downloading H8 series data
    for ufKey, datasets in H8_SeriesIds_Filepaths.items():
        print(f"Units & Frequency: {ufKey}")  # Print the units and frequency (e.g., Weekly-SA)
        
        # Iterate through each dataset in the current frequency and unit category
        for dataset, (seriesID, filePath) in datasets.items():
            print(f"  Dataset: {dataset}")  # Print the dataset name

            # Fetch the time-series data from the FRED API using the series ID
            data = client.getSeries(str(seriesID))

            # Convert the fetched data into a 2D list format (i.e., [[date, value], ...])
            parsedData = seriesToTwoDimensionalList(data)

            # Attempt to write the parsed data to the corresponding file path
            success = writeParsedDataToFile(filePath, parsedData)

            # Check if writing data was successful and print the appropriate message
            if success:
                print(f"    Data for {seriesID} successfully written to: {filePath}")
                saveH8FileNames(filePath) # Save the data file in file database for H8
            else:
                print(f"    Failed to write data for {seriesID} to {filePath}")
            
            # Pause for 5 seconds to avoid hitting API rate limits
            time.sleep(5)

def unwrapH41Dict(H41Data: dict, recursionDepth: int, client: FredApiClient):
    """
    unwrapH41Dict

    This function uses recursion to unwrap and retrieve seriesIds for data sets, and then
    downloads, parses, and saves time-series data for the H41 report using series IDs and file paths.

    This function iterates through the structured dictionary of H41 series metadata, 
    retrieves the corresponding data from the FRED API, and saves it to designated file paths in H41Data. 
    Upon succesful download, parsing, and file writing of time-series data, the function saves file names 
    in a filename databse for the H41 data set.
    
    To prevent exceeding API rate limits, it includes a delay between requests.

    Parameters:
        - H41Data (dict): A nested dictionary containing balance sheet lines, series IDs, and file paths.
        - recursionDepth (int): Tracks the depth of recursion for structured printing.
        - client (FredApiClient): API client instance used to fetch the series data.

    Returns:
        - None (Downloads and writes data to files).
    """
    for key in H41Data:  # Iterate over keys
        value = H41Data[key]  # Get the corresponding value
        print(f"{'  ' * recursionDepth}{recursionDepth}) Balance Sheet Line: {key}")

        if isinstance(value, dict):
            # If the dictionary contains a seriesId and filePath, download the data
            if 'seriesId' in value and 'filePath' in value:
                seriesId = value['seriesId']
                filePath = value['filePath']

                print(f"{'  ' * recursionDepth}    {recursionDepth}) Downloading Series ID: {seriesId}")

                # Fetch the time-series data from the FRED API
                try:
                    data = client.getSeries(seriesId, None, None, 6)

                    # Convert data to a 2D list (e.g., [[date, value], ...])
                    parsedData = seriesToTwoDimensionalList(data)

                    # Write the parsed data to the corresponding file path
                    success = writeParsedDataToFile(filePath, parsedData)

                    # Print confirmation
                    if success:
                        print(f"{'  ' * recursionDepth}    {recursionDepth}) Data successfully written to: {filePath}")
                        saveH41FileNames(filePath) # Save the data file in file database for H41
                    else:
                        print(f"{'  ' * recursionDepth}    {recursionDepth}) Failed to write data to: {filePath}")

                    # Pause for 5 seconds to avoid hitting API rate limits
                    time.sleep(5)

                except Exception as e:
                    print(f"Error fetching series {seriesId}: {e}")

            # Continue recursive traversal for nested elements
            unwrapH41Dict(value, recursionDepth + 1, client)

# Set up API key and client
apiKey = getApiKey()
client = FredApiClient(apiKey)

# Get series IDs and file paths for H8 Dataset
H8_SeriesIds_Filepaths = parseH8Series()

# Download and Save the H8 Data
downloadH8Data(H8_SeriesIds_Filepaths, client)

# Get series IDs and file paths for H41 Dataset
H41_SeriesIds_Filepaths = parseH41Series()

# Download and Save the H41 Data
for tableNumber in H41_SeriesIds_Filepaths.keys():
    print(f"Downloading {tableNumber}")
    unwrapH41Dict(H41_SeriesIds_Filepaths[tableNumber], 0, client)