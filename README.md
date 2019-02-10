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

## Usage

The URL scheme follows that [established by Huxley](https://github.com/jpsingleton/Huxley#url-format),
absent the `/staff*/`, `/delays/` and `/all/` endpoints. The first is missing
as I have no use for a staff only API, and the latter two because they are
easily computed by the client application, instead of adding complicated logic
to the proxy.

### General Format

Unfiltered departures or arrivals boards:

`{board}/{crs}/{numRows}`

Filtered departures or arrivals boards:

`{board}/{crs}/{filterType}/{filterCRS}/{numRows}`

Allowable values:

```ebnf
board      = "departures" | "arrivals";   (* type of board to query *)
crs        = stationCRS | Station Name;   (* station to get board for *)
filterType = "from" | "to";               (* (optional) filter direction *)
filterCRS  = crs;                         (* (optional) filter origin/destination *)
numRows    = integer;                     (* maximum number of services to return *)
```

### CRS Codes

Station CRS codes can be looked up via the CRS query API:

`crs/{query}`

For example:

```
# curl -H "..." https://daltonapi.herokuapp.com/crs/Euston
[{"stationName": "London Euston", "crsCode": "EUS"}]
```

You can supply the exact station name in place of the CRS code in other API
queries, and the CRS will be inserted for you.


### Example Usage
```sh
$ curl -H "..." https://daltonapi.herokuapp.com/departures/London\ Cannon\ Street/1 | python -m json.tool
```
```json
{
  "generatedAt": "Sun, 10 Feb 2019 09:12:13 GMT",
  "locationName": "London Cannon Street",
  "platformAvailable": true,
  "trainServices": {
    "service": [
      {
        "destination": {
          "location": [
            {
              "crs": "DFD",
              "locationName": "Dartford",
              "via": "via Lewisham & Sidcup"
            }
          ]
        },
        "etd": "On time",
        "operator": "Southeastern",
        "operatorCode": "SE",
        "origin": {
          "location": [
            {
              "crs": "CST",
              "locationName": "London Cannon Street",
            }
          ]
        },
        "platform": "2",
        "rsid": "SE259200",
        "serviceID": "HZYtxCpU1/9RKILKJh/XRg==",
        "serviceType": "train",
        "std": "09:24"
      }
    ]
  }
}
```
