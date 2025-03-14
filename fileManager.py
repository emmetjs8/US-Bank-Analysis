def readFromFile(fileName: str, deliniator: str = None) -> list:
    """
    Reads data from a file and returns a list of its contents. 

    :param fileName: Path to the file to be read.
    :param deliniator: Optional delimiter to split each line. Defaults to None.
    :return: A list containing the file's contents. If a delimiter is provided, 
             each line is split into a list based on the delimiter.
    """

    fileData = []  # Initialize an empty list to store file contents

    try:
        with open(fileName, "r") as file:
            if deliniator is not None:
                fileData = [line.strip().split(deliniator) for line in file]  # Read and split each line
            else:
                fileData = [line.strip() for line in file]  # Read and strip each line

    except FileNotFoundError:
        print(f"Warning: {fileName} not found. Returning an empty list.")
        return []
    
    if not fileData:
        print(f"Warning: {fileName} is empty. Returning an empty list.")
        return []

    return fileData
