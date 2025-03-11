"""
seriesIdParser.py

This script is associated with `initDataFiles.py` and is used exclusively for initializing 
files and data that do not exist yet. It processes metadata from the Federal Reserve's 
H8 and H41 reports, organizes series IDs into structured dictionaries, and generates 
standardized file paths for storing data.

Once the program is fully running, another script will be developed to read similar 
information but with precomputed file paths in each line, allowing these functions 
to be bypassed for efficiency.

File Format Assumption (H8_Series_Ids.txt and H41_Series_Ids.txt):
    - Dataset Name-Frequency (Weekly or Monthly)-Units (SA or NSA)-Series ID
    - Table Number-Balance Sheet Section(s)-Series ID

Functions:
    - createH8FilePath(frequency, units, seriesId): Generates a standardized file path.
    - createH41FilePath(tableNumber, seriesId): Generates a file path for a given table and series ID.
    - initDicts(parsedLine, weeklySA, weeklyNSA, monthlySA, monthlyNSA): 
      Parses metadata and stores (series ID, file path) in the appropriate dictionary.
    - getSeriesIdsAndFilepaths(): Reads the input file and returns a structured dictionary.
    - initH41Dict(parsedLine, currentTable, reserveBalanceSheet): 
      Initializes and updates the hierarchical dictionary with series data.
    - parseH41Series(): Parses the H41 series file and builds a nested dictionary.

Author: Emmet Szewczyk
Date: 3/11/25
"""

def createH8FilePath(frequency: str, units: str, seriesId: str) -> str:
    """
    Generates a standardized file path for storing H8 series data.

    Args:
        frequency (str): Frequency of data ("Weekly" or "Monthly").
        units (str): Seasonal adjustment type ("SA" or "NSA").
        seriesId (str): Unique identifier for the series.

    Returns:
        str: The formatted file path for storing the series data.
    """
    return f"data/H8/{units.upper()}{frequency[0].upper()}/{seriesId}.txt"

def createH41FilePath(tableNumber: str, seriesId: str) -> str:
    """
    Generates a structured file path for storing H41 series data.

    Args:
        tableNumber (str): The table number associated with the series.
        seriesId (str): The unique identifier for the series.

    Returns:
        str: A formatted file path for the specified table and series ID.
    """
    return f"data/H41/{tableNumber}/{seriesId}.txt"


def initH8Dicts(parsedLine: list, weeklySA: dict, weeklyNSA: dict, monthlySA: dict, monthlyNSA: dict) -> None:
    """
    Parses a metadata line of H8 information and categorizes the series ID into the appropriate dictionary.

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
    filePath = createH8FilePath(frequency, units, seriesId)

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

def initH41Dict(parsedLine: list, currentTable: str, reserveBalanceSheet: dict) -> None:
    """
    Populates the hierarchical reserve balance sheet dictionary with series data from H41.

    This function navigates the nested dictionary structure and inserts series IDs
    with their corresponding file paths.

    Args:
        parsedLine (list): A list representing hierarchical levels of the series.
        currentTable (str): The table number associated with the series.
        reserveBalanceSheet (dict): The main dictionary storing the H41 series data.

    Returns:
        None
    """
    currentLevel = reserveBalanceSheet  # Start from the root of the dictionary

    # Iterate through all levels except the last one (which is the series ID)
    for level in parsedLine[:-1]:
        if level not in currentLevel:
            currentLevel[level] = {}  # Create a new nested dictionary if it doesn't exist
        currentLevel = currentLevel[level]  # Move deeper into the structure

    # Assign the last element (series ID) along with the generated file path
    seriesId = parsedLine[-1]
    currentLevel["seriesId"] = seriesId
    currentLevel["filePath"] = createH41FilePath(currentTable, seriesId)

def parseH8Series() -> dict:
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
    seriesIdFile = "data/H8_Series_Ids.txt"

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
            initH8Dicts(parsedLine, weeklySA, weeklyNSA, monthlySA, monthlyNSA)

    # Return categorized dictionaries
    return {"SAW": weeklySA, "SAM": monthlySA, "NSAW": weeklyNSA, "NSAM": monthlyNSA}

def parseH41Series() -> dict:
    """
    Parses the H41 series data file and builds a nested dictionary.

    Reads the "H41_Series_Ids.txt" file, processes each line into hierarchical
    components, and structures them in a dictionary with series IDs and file paths.

    Returns:
        dict: A nested dictionary representing the parsed H41 series data.
    """
    reserveBalanceSheet = {}  # Initialize the main dictionary

    seriesIdFile = "data/H41_Series_Ids.txt"  # File containing series ID mappings

    with open(seriesIdFile, "r") as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing spaces and newline characters
            if not line:
                continue  # Skip empty lines

            parsedLine = [part.strip() for part in line.split("-")]  # Split hierarchy by '-'

            # Populate the dictionary with parsed data
            initH41Dict(parsedLine, parsedLine[0], reserveBalanceSheet)

    return reserveBalanceSheet