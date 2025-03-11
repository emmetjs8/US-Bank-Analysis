"""
getApiKey.py

This script contains functions to retrieve API keys.
It includes:
    - A function to fetch a personal API key from a local file (apiKeys.txt).
    - A function to prompt the user to enter their own API key and confirm it.
    - A wrapper function that either retrieves the personal API key or prompts the user for one.

Functions:
    - getPersonalKey: Returns the personal API key from a local file (apiKeys.txt).
    - getUserApiKey: Prompts the user to input their API key and returns it.
    - getApiKey: Returns the API key, either by fetching the personal one or prompting the user for it.

Author: [Your Name]
Date: [Today's Date]
"""

def getPersonalKey(fileName="apiKeys.txt") -> str:
    """
    Retrieves the personal API key from the specified file.

    Args:
        fileName (str): The file path where the personal API key is stored (default is "apiKeys.txt").

    Returns:
        str: The personal API key.
    """
    try:
        # Open the apiKeys.txt file and read the key
        with open(fileName, 'r') as file:
            # Read the first line and strip any extra whitespace/newline characters
            personalKey = file.readline().strip()
        return personalKey
    except FileNotFoundError:
        print(f"Error: The file {fileName} was not found.")
        return ""
    except Exception as e:
        print(f"An error occurred while reading the API key: {e}")
        return ""


def getUserApiKey() -> str:
    """
    Prompts the user to enter their API key and confirms if it's correct.

    Returns:
        str: The user-input API key.
    """
    userApiKey = input("Please enter your API key: ")

    # Print entered key and ask for confirmation
    print(f"You entered: {userApiKey}")
    valid = input("Enter 'Y' to confirm or 'N' to try again: ").lower()

    if valid == 'Y':
        return userApiKey
    else:
        # Recursively call the function if the user chooses to try again
        return getUserApiKey()


def getApiKey() -> str:
    """
    Retrieves the API key by first attempting to fetch the personal key from the file, 
    and if not found, prompts the user for their API key.

    Returns:
        str: The API key, either fetched from the file or entered by the user.
    """
    # Set up API key and client
    personalApiKey = getPersonalKey()

    # If a personal API key is found, use it; otherwise, prompt the user for one
    if personalApiKey != "":
        return personalApiKey
    else:
        return getUserApiKey()
