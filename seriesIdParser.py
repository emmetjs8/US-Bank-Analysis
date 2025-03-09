"""
seriesIdParser.py

This script reads a text file containing economic data series metadata on the Federal Reserve's
H8 and H41 reports and organizes the series IDs into categorized dictionaries based on their 
frequency and seasonal adjustment type. It also generates standardized file paths for storing data.

File Format Assumption (H8_Series_Ids.txt and H41_Series_Ids.txt):
    - Dataset Name-Frequency (Weekly or Monthly)-Units (SA or NSA)-Series IDs

Example Input:
    Consumer Loans, Credit Cards and Revolving Plans-Weekly-SA-CCLACBW027SBOG
    Deposits-Weekly-SA-DPSACBW027SBOG

Example Output (Returned Dictionary):
    {
        "SAW": { # Weekly Seasonally Adjusted
            "Consumer Loans": ["CCLACBW027SBOG", "data/SAW/CCLACBW027SBOG.txt"],
            "Deposits": ["DPSACBW027SBOG", "data/SAW/DPSACBW027SBOG.txt"]
        },
        "SAM": {  # Monthly Seasonally Adjusted
            "Loans": ["LNSACBM027SBOG", "data/SAM/LNSACBM027SBOG.txt"]
        },
        "NSAW": {  # Weekly Non-Seasonally Adjusted
            "Deposits": ["DPSNSBW027SBOG", "data/NSAW/DPSNSBW027SBOG.txt"]
        },
        "NSAM": {}  # Monthly Non-Seasonally Adjusted (empty in this example)
    }

Functions:
    - createFilePath(frequency, units, seriesId): Generates a standardized file path.
    - initDicts(parsedLine, weeklySA, weeklyNSA, monthlySA, monthlyNSA): 
      Parses metadata and stores (series ID, file path) in the appropriate dictionary.
    - getSeriesIdsAndFilepaths(): Reads the input file and returns a structured dictionary.

Author: Emmet Szewczyk
Date: 3/9/25
"""

def createFilePath(frequency: str, units: str, seriesId: str) -> str:
    """
    Generates a standardized file path for storing series data.

    Args:
        frequency (str): Frequency of data ("Weekly" or "Monthly").
        units (str): Seasonal adjustment type ("SA" or "NSA").
        seriesId (str): Unique identifier for the series.

    Returns:
        str: The formatted file path for storing the series data.
    """
    return f"data/{units.upper()}{frequency[0].upper()}/{seriesId}.txt"


def initDicts(parsedLine: list, weeklySA: dict, weeklyNSA: dict, monthlySA: dict, monthlyNSA: dict) -> None:
    """
    Parses a metadata line and categorizes the series ID into the appropriate dictionary.

    Args:
        parsed_line (list): List of metadata components (Dataset, Frequency, Units, Series ID).
        weeklySA (dict): Dictionary to store weekly seasonally adjusted series.
        weeklyNSA (dict): Dictionary to store weekly non-seasonally adjusted series.
        monthlySA (dict): Dictionary to store monthly seasonally adjusted series.
        monthlyNSA (dict): Dictionary to store monthly non-seasonally adjusted series.

    Returns:
        None: Updates the respective dictionary in place.
    """
    if len(parsedLine) < 4:
        print(f"Warning: Malformed line detected - {parsedLine}")
        return

    # Extract metadata elements
    datasetName = parsedLine[0].strip()
    frequency = parsedLine[-3].strip()
    units = parsedLine[-2].strip()
    seriesId = parsedLine[-1].strip()

    # Generate file path
    filePath = createFilePath(frequency, units, seriesId)

    # Select the appropriate dictionary
    targetDict = None
    if frequency == "Weekly" and units == "SA":
        targetDict = weeklySA
    elif frequency == "Weekly" and units == "NSA":
        targetDict = weeklyNSA
    elif frequency == "Monthly" and units == "SA":
        targetDict = monthlySA
    elif frequency == "Monthly" and units == "NSA":
        targetDict = monthlyNSA

    # Store series ID in the dictionary
    if targetDict is not None:
        if datasetName not in targetDict:
            targetDict[datasetName] = []  # Initialize an empty list
        targetDict[datasetName].append(seriesId)
        targetDict[datasetName].append(filePath)


def getSeriesIdsAndFilepaths() -> dict:
    """
    Reads the H8_Series_Ids.txt file, parses its contents, and categorizes the series IDs 
    into four dictionaries based on frequency and seasonal adjustment type.

    Returns:
        dict: A dictionary containing four categorized series ID mappings:
              - "SAW": Weekly Seasonally Adjusted
              - "SAM": Monthly Seasonally Adjusted
              - "NSAW": Weekly Non-Seasonally Adjusted
              - "NSAM": Monthly Non-Seasonally Adjusted
    """
    seriesIdFile = "H8_Series_Ids.txt"

    # Dictionaries for categorized series IDs
    weeklySA, monthlySA, weeklyNSA, monthlyNSA = {}, {}, {}, {}

    # Open the file and process its contents
    with open(seriesIdFile, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing spaces and newline characters
            if not line:
                continue  # Skip empty lines
            
            parsedLine = [part.strip() for part in line.split("-")]  # Split on '-'

            # Update dictionaries
            initDicts(parsedLine, weeklySA, weeklyNSA, monthlySA, monthlyNSA)

    # Return categorized dictionaries
    return {"SAW": weeklySA, "SAM": monthlySA, "NSAW": weeklyNSA, "NSAM": monthlyNSA}