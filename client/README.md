# sanic.access

Use aiohttp to access sanic web server based on the token authentication mechanism (sanic-jwt).

## Preparation

- Python 3.5.3+
- Install aiohttp

## Access to the process

- Access token value

		As follows:
			HTTP request mode: POST
			Request path: http://IP:PORT/auth
			Request parameters: {"username": "XXX", "password": "XXX"}
			
	Return the correct results as follows：
	
	```
{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE1MjQ3MzY3NTF9.Z1_0OG6SRgxZ6tAUhiTyCnGNxwIrSwWlyPA9Fg-37Qg"}
	```
	*Note：*The value of the above return "access_token" is JWT.

- Access to encrypted resources

		As follows:
			HTTP request mode: GET
			Request path: http://IP:PORT/v2/events
			Request header: {'Authorization': 'Bearer $JWT'}
			
	Return the correct results as follows：
	
	```
[
    {
        "version": "1.1.0",
        "id": 201,
        "type": "alarm",
        "system": 1,
        "segment": 2,
        "offset": 0.5,
        "timestamp": "2018-01-01 08:30:45",
        "remark": "reserve"
    },
    {
        "version": "1.1.0",
        "id": 208,
        "type": "alarm",
        "system": 3,
        "segment": 9,
        "offset": 0.8,
        "timestamp": "2018-01-01 09:39:01",
        "remark": "reserve"
    }
]
	```			

## Achievement goal

* The effect of the client implementation. as follows:
	* If the user and password are incorrect, respond immediately.
	* Client programs cannot be terminated for reasons other than human.
	* The web server is restarted after it is disconnected, and the correct data can be obtained immediately.
	* When the token value is expired, the token value should be automatically regained and the data is retrieved.