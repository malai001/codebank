import requests
parameters = {"lat": 37.78, "lon": -122.41}
resp = requests.get('http://api.open-notify.org/iss-pass.json',params=parameters)
if resp.status_code == 200:
	print(resp.json())
else:
	raise ApiError('GET /tasks/ {}'.format(resp.status_code))