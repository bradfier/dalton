import re
from . import crs
from . import soap

from flask import jsonify
from flask_restful import reqparse, abort, Resource
from functools import wraps

parser = reqparse.RequestParser()
parser.add_argument('Authorization', location='headers', required=True)


def handle_fault(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        from zeep.exceptions import Fault
        last_fault = None
        try:
            return f(*args, **kwargs)
        except Fault as fault:
            last_fault = fault

        # Bad API keys result in weird non-soap error XML
        if last_fault.detail is not None:
            try:
                if '401' in bytes.decode(last_fault.detail):
                    abort(401, message='Invalid authentication token')
            except TypeError:
                pass
        abort(502, message=last_fault.message)

    return wrapper


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


def parse_station_list(stations):
    return [parse_station(s) for s in stations.split(',')]


def parse_direction(direction):
    if (direction.lower() == 'from' or direction.lower() == 'to'):
        return direction.lower()
    else:
        abort(
            400,
            message='Bad filter direction specifier, must be \'from\' or \'to\''
        )


class SoapResource(Resource):
    method_decorators = [handle_fault]


class CRS(Resource):
    def get(self):
        codes = [{
            'stationName': crs.CODES[k],
            'crsCode': k
        } for k in crs.CODES]

        return codes


class Departures(SoapResource):
    def get(self, station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetDepartureBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    _soapheaders=[header])))


class FilteredDepartures(SoapResource):
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


class NextDeparture(SoapResource):
    def get(self, station, station_list):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetNextDepartures(
                    crs=parse_station(station),
                    filterList=parse_station_list(station_list),
                    _soapheaders=[header])))


class Arrivals(SoapResource):
    def get(self, station, num_rows=10):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetArrivalBoard(
                    numRows=num_rows,
                    crs=parse_station(station),
                    _soapheaders=[header])))


class FilteredArrivals(SoapResource):
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


class Fastest(SoapResource):
    def get(self, station, station_list):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetFastestDepartures(
                    crs=parse_station(station),
                    filterList=parse_station_list(station_list),
                    _soapheaders=[header])))


class ServiceDetails(SoapResource):
    def get(self, service_id):
        args = parser.parse_args()
        header = gen_auth_header(args['Authorization'])
        return jsonify(
            soap.to_dict(
                soap.client.service.GetServiceDetails(
                    serviceID=service_id, _soapheaders=[header])))
