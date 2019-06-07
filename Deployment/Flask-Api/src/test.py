import requests 
  
# api-endpoint 
URL = "http://localhost:5000/api"
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {'Authorization': 'Bearer you-will-never-guess'} 
  
# sending get request and saving the response as response object 
r = requests.get(url = URL, headers = PARAMS) 
  
# extracting data in json format 
data = r.json() 

print(data)