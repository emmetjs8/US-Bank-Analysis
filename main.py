from seriesIdParser import getSeriesIdsAndFilepaths
from fredClient import FredApiClient
from getApiKey import getApiKey

apiKey = getApiKey()
client = FredApiClient(apiKey)
H8_SeriesIds_Filepaths = getSeriesIdsAndFilepaths()

