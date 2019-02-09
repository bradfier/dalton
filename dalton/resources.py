import re
from . import crs
from . import soap

from flask import jsonify
from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers', required=True)


def gen_auth_header(header):
    if header.startswith('Bearer'):
        token = re.sub(r'^Bearer\s+', '', header)
        return soap.auth_header(token)

    if header.startswith('bearer'):
        token = re.sub(r'^bearer\s+', '', header)
        return soap.auth_header(token)

    abort(400, message='Authorization header does not contain bearer token')


def parse_station(station):
    if station.upper() in crs.CODES:
        return station.upper()

    for code, name in crs.CODES.items():
        if name == station:
            return code

    abort(400, message='Bad CRS code or station name')


def parse_direction(direction):
    if (direction.lower() == 'from' or direction.lower() == 'to'):
        return direction.lower()
    else:
        abort(
            400,
            message='Bad filter direction specifier, must be \'from\' or \'to\''
        )


class CRS(Resource):
    def get(self):
        codes = [{
            'stationName': crs.CODES[k],
            'crsCode': k
        } for k in crs.CODES]

        return codes


class FilteredDepartures(Resource):
    def get(self, station, filter_direction, filter_station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetDepartureBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    filterCrs=parse_station(filter_station),
                    filterType=parse_direction(filter_direction),
                    _soapheaders=[header])))


class Departures(Resource):
    def get(self, station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetDepartureBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    _soapheaders=[header])))


class Arrivals(Resource):
    def get(self, station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetArrivalBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    _soapheaders=[header])))


class FilteredArrivals(Resource):
    def get(self, station, filter_direction, filter_station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetArrivalBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    filterCrs=parse_station(filter_station),
                    filterType=parse_direction(filter_direction),
                    _soapheaders=[header])))
