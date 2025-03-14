from datetime import datetime, timedelta
from fileManager import readFromFile

def getFilePaths() -> tuple[list, list]:
    """
    Retrieves lists of file paths from the H41 and H8 dataset filenames text files.

    :return: A tuple containing two lists:
             - First list contains file paths from the H41 dataset.
             - Second list contains file paths from the H8 dataset.
    """
    H41_File_Database = "data/H41/filenames.txt"
    H8_File_Database = "data/H8/filenames.txt"

    # Read file paths from each dataset file
    H41_Filepaths = readFromFile(H41_File_Database)
    H8_Filepaths = readFromFile(H8_File_Database)

    return H41_Filepaths, H8_Filepaths


def checkLastDataDownload(filePath: str) -> bool:
    """
    Checks if the last data download recorded in the file was within the last 7 days.

    :param filePath: Path to the file containing download dates.
    :return: True if the last recorded download was within the last 7 days, False otherwise.
    """

    # Open the file and download content:
    fileData = readFromFile(filePath, "\0")

    lastDownloadDate = fileData[-1][0]  # Extract last recorded date
    print(f"Last Download Date: {lastDownloadDate}")

    try:
        lastDownloadDate = datetime.strptime(lastDownloadDate, "%Y-%m-%d")  # Convert to datetime
    except ValueError:
        print(f"Error: Invalid date format in {filePath}. Returning False.")
        return False

    # Check if the last download was within the last 7 days
    sevenDaysAgo = datetime.today() - timedelta(days=7)
    
    return lastDownloadDate >= sevenDaysAgo

