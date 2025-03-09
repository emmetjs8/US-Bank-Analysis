import time
from fredapi import Fred
from datetime import datetime, timedelta

class FredApiClient:
    """
    A client for interacting with the FRED API.
    
    This class manages sending requests to the FRED API, while ensuring that the rate limit
    of 120 requests per minute is respected. If the rate limit is exceeded, it will retry up to 6 times
    with a 20-second delay between each attempt.
    """
    
    def __init__(self, apiKey):
        """
        Initialize the FredApiClient class with the given API key.
        
        :param apiKey: The API key to access FRED data.
        """
        self.apiKey = apiKey
        self.fred = Fred(api_key=self.apiKey)  # Create an instance of the Fred class with the provided API key
        self.retryLimit = 6
        self.retryDelay = 20
        self.requestTimes = []  # List to track request times for rate limit control
    
    def trackRequests(self):
        """
        Tracks the time of each request to ensure that no more than 120 requests are made per minute.
        
        This function adds the current time of each request to the `requestTimes` list and removes
        any times that are older than 1 minute to ensure the list only contains times within the last minute.
        If more than 120 requests are made within the last minute, it will wait for the next available time window.
        """
        currentTime = datetime.now()

        # Remove request times that are older than 1 minute
        self.requestTimes = [t for t in self.requestTimes if currentTime - t < timedelta(minutes=1)]

        if len(self.requestTimes) >= 120:
            # If more than 120 requests have been made in the last minute, wait until the next minute
            waitTime = 60 - (currentTime - self.requestTimes[0]).seconds
            print(f"Request limit reached. Waiting for {waitTime} seconds.")
            time.sleep(waitTime)
        
        # Add the current time to the requestTimes list
        self.requestTimes.append(currentTime)
    
    def getSeries(self, seriesId, startDate=None, endDate=None, maxAttempts=6):
        """
        Retrieves a time series from the FRED API while respecting the rate limit.

        :param series_id: The FRED series ID to fetch data for.
        :param start_date: The start date for the data (YYYY-MM-DD, optional).
        :param end_date: The end date for the data (YYYY-MM-DD, optional).
        :param max_attempts: Maximum retry attempts if rate limit is exceeded.
        :return: A pandas Series containing the requested FRED data.
        """
        attempt = 0

        while attempt < maxAttempts:
            try:
                self.trackRequests()  # Ensure we are within the request limit

                # If user a date range was not inputted, get all the data for the series
                if (startDate is None and endDate is None):
                    data = self.fred.get_series(seriesId)
                # Otherwise, get the data in the time period
                else:
                    data = self.fred.get_series(seriesId, startDate, endDate)
                return data  # Return the retrieved series

            except Exception as e:
                errorMsg = str(e)
                
                if "429" in errorMsg:
                    # Rate limit exceeded, apply retry mechanism
                    attempt += 1
                    print(f"Rate limit exceeded. Retrying in {self.retryDelay} seconds (Attempt {attempt}/{maxAttempts})...")
                    time.sleep(self.retryDelay)
                else:
                    # Other errors (e.g., network, invalid API key, etc.)
                    print(f"Error fetching series {seriesId}: {errorMsg}")
                    return None

        print("Max retry attempts reached. Could not fetch data.")
        return None