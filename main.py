from fredClient import FredApiClient
from getApiKey import getApiKey
from setUp import *

apiKey = getApiKey()
client = FredApiClient(apiKey)
H41_Filepaths, H8_Filepaths = getFilePaths()
print(H41_Filepaths)

updateData = checkLastDataDownload(H8_Filepaths[0])


