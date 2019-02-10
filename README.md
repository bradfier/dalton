# Dalton

## Darwin (UK National Rail) Live Departure Board JSON Proxy

Dalton is a Python reimplementation of the JSON proxy API defined in
[Huxley](https://huxley.unop.uk), allowing access to the National Rail
Departure Boards Web-Service, without the pain and suffering generally
associated with consuming SOAP.

The most useful parts of Huxley's API are reimplemented, the notable
exceptions being the staff endpoints and the delay calculations.

## Deployment

Configuration files are included for deployment on a Heroku Dyno, and an
instance is available for testing at `https://daltonapi.herokuapp.com`

To run Dalton locally, or on your own server, install the dependencies
with `pip` and start the proxy with Gunicorn:

```sh
$ pip install -r requirements.txt
...
$ gunicorn dalton.api:app
```

If you run your own proxy, it is recommended that you enable SSL for all
requests, otherwise your LDBWS Access Token will be sent in the clear.

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
$ curl -H "..." https://daltonapi.herokuapp.com/crs/Euston
[{"stationName": "London Euston", "crsCode": "EUS"}]
```

You can supply the exact station name in place of the CRS code in other API
queries, and the CRS will be inserted for you.

### Service Information

More details about a service listed in a departure or arrival board can be
obtained from the `/service/{serviceID}` endpoint.


## Example Usage

Unfiltered departures:

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

---

Filtered arrivals:

```sh
$ curl -H "..." https://daltonapi.herokuapp.com/arrivals/EUS/from/MKC/2 | python -m json.tool
```
```json
{
  "crs": "EUS",
  "filterLocationName": "Milton Keynes Central",
  "filterType": "from",
  "filtercrs": "MKC",
  "generatedAt": "Sun, 10 Feb 2019 09:48:51 GMT",
  "locationName": "London Euston",
  "platformAvailable": true,
  "trainServices": {
    "service": [
      {
        "destination": {
          "location": [
            {
              "crs": "EUS",
              "locationName": "London Euston",
            }
          ]
        },
        "eta": "On time",
        "operator": "West Midlands Trains",
        "operatorCode": "LM",
        "origin": {
          "location": [
            {
              "crs": "NMP",
              "locationName": "Northampton",
            }
          ]
        },
        "platform": "8",
        "rsid": "LM500800",
        "serviceID": "TBrpFO9M/Nko3c0sdHXzdA==",
        "serviceType": "train",
        "sta": "10:11",
      },
      {
        "destination": {
          "location": [
            {
              "crs": "EUS",
              "locationName": "London Euston",
            }
          ]
        },
        "eta": "On time",
        "operator": "Virgin Trains",
        "operatorCode": "VT",
        "origin": {
          "location": [
            {
              "crs": "WVH",
              "locationName": "Wolverhampton",
            }
          ]
        },
        "platform": "6",
        "rsid": "VT550100",
        "serviceID": "ipsbHiuHrKc1Osxh2bL5Pg==",
        "serviceType": "train",
        "sta": "10:25",
      }
    ]
  }
}
```

---

Service details:

```sh
$ curl -H "..." https://daltonapi.herokuapp.com/service/ipsbHiuHrKc1Osxh2bL5Pg== | python -m json.tool
```
```json
{
  "crs":"EUS",
  "generatedAt":"Sun, 10 Feb 2019 09:54:55 GMT",
  "locationName":"London Euston",
  "previousCallingPoints":{
    "callingPointList":[
      {
        "assocIsCancelled":"false",
        "callingPoint":[
          {
            "at":"On time",
            "crs":"WVH",
            "locationName":"Wolverhampton",
            "st":"08:05"
          },
          {
            "at":"08:17",
            "crs":"SAD",
            "locationName":"Sandwell & Dudley",
            "st":"08:15"
          },
          {
            "at":"On time",
            "crs":"BHM",
            "locationName":"Birmingham New Street",
            "st":"08:30"
          },
          {
            "at":"On time",
            "crs":"BHI",
            "locationName":"Birmingham International",
            "st":"08:40"
          },
          {
            "at":"On time",
            "crs":"COV",
            "locationName":"Coventry",
            "st":"08:51"
          },
          {
            "at":"On time",
            "crs":"RUG",
            "locationName":"Rugby",
            "st":"09:04"
          },
          {
            "at":"On time",
            "crs":"MKC",
            "locationName":"Milton Keynes Central",
            "st":"09:39"
          }
        ],
        "serviceChangeRequired":"false",
        "serviceType":"train"
      }
    ]
  }
}
```

### Returning Full Results

By default, Dalton suppresses any fields in the Darwin response with `null` values,
the National Rail service tends to send a lot of these, and it's a bit of a waste
of bandwidth.

If you prefer, you can append `?full=true` to any query URL to receive the full
result set instead.

```sh
$ curl -H "..." https://daltonapi.herokuapp.com/departures/KGX/5?full=true | python -m json.tool
```
```json
{
  "areServicesAvailable":null,
  "busServices":null,
  "crs":"KGX",
  "ferryServices":null,
  "filterLocationName":null,
  "filterType":null,
  "filtercrs":null,
  "generatedAt":"Sun, 10 Feb 2019 10:18:54 GMT",
  "locationName":"London Kings Cross",
  "nrccMessages":{
    "message":[
      {
        "_value_1":"Additional trains to Great Northern destinations also operate from London St Pancras International (STP) which is a short walk from London Kings Cross."
      }
    ]
  },
  "platformAvailable":true,
  "trainServices":{
    "service":[
      {
        "adhocAlerts":null,
        "cancelReason":null,
        "currentDestinations":null,
        "currentOrigins":null,
        "delayReason":null,
        "destination":{
          "location":[
            {
              "assocIsCancelled":null,
              "crs":"EDB",
              "futureChangeTo":null,
              "locationName":"Edinburgh",
              "via":null
            }
          ]
        },
        "detachFront":null,
        "eta":null,
        "etd":"On time",
        "filterLocationCancelled":null,
        "formation":null,
        "isCancelled":null,
        "isCircularRoute":null,
        "isReverseFormation":null,
        "length":null,
        "operator":"London North Eastern Railway",
        "operatorCode":"GR",
        "origin":{
          "location":[
            {
              "assocIsCancelled":null,
              "crs":"KGX",
              "futureChangeTo":null,
              "locationName":"London Kings Cross",
              "via":null
            }
          ]
        },
        "platform":"6",
        "rsid":"GR622100",
        "serviceID":"3InPTIgVZbt2gtMLSHJ2mg==",
        "serviceType":"train",
        "sta":null,
        "std":"10:30"
      }
    ]
  }
}
```

## License

Dalton is licensed under the GNU Affero General Public License, Version 3, see
LICENSE for more information.

Included public sector information is licensed under the Open Government
License v3.0.

Dalton is powered by the [National Rail Darwin Data Feeds](http://www.nationalrail.co.uk/100296.aspx).
