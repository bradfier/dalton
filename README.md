# Dalton

## Darwin (UK National Rail) Live Departure Board JSON Proxy

Dalton is a Python reimplementation of the JSON proxy API defined in
[Huxley](https://huxley.unop.uk), allowing access to the National Rail
Departure Boards Web-Service, without the pain and suffering generally
associated with consuming SOAP.

The most useful parts of Huxley's API are reimplemented, the notable
exceptions being the staff endpoints and the delay calculations.

## Access Tokens

You will need to obtain an [OpenLDBWS Access Token](http://realtime.nationalrail.co.uk/OpenLDBWSRegistration/)
before you can use the API.

## The Authorization Header

This is the one notable difference between the Huxley and Dalton API,
while Huxley expects the credentials to be passed as a query parameter,
Dalton uses a more standard method by reading the HTTP Authorization header.

When calling the API, set the `Authorization` header to `Bearer <access-token>`, e.g:

```python
>>> import requests

>>> url = 'https://daltonapi.herokuapp.com/departures/EUS/5'
>>> headers = {'Authorization': 'Bearer abcert17-abcd-1234-5678-ccbcce0b0b0b'}

>>> data = requests.get(url, headers=headers)
```

