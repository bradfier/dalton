from flask import Flask
from flask_restful import Resource, Api

from .resources import CRS, Departures, FilteredDepartures, NextDeparture, Arrivals, FilteredArrivals, Fastest, ServiceDetails

app = Flask(__name__)
api = Api(app)

api.add_resource(CRS, '/crs', '/crs/<string:query>')

api.add_resource(Departures, '/departures/<string:station>/<int:num_rows>',
                 '/departures/<string:station>')
api.add_resource(
    FilteredDepartures,
    '/departures/<string:station>/<string:filter_direction>/<string:filter_station>/<int:num_rows>',
    '/departures/<string:station>/<string:filter_direction>/<string:filter_station>'
)

api.add_resource(Arrivals, '/arrivals/<string:station>/<int:num_rows>',
                 '/arrivals/<string:station>')
api.add_resource(
    FilteredArrivals,
    '/arrivals/<string:station>/<string:filter_direction>/<string:filter_station>/<int:num_rows>',
    '/arrivals/<string:station>/<string:filter_direction>/<string:filter_station>'
)

api.add_resource(NextDeparture,
                 '/next/<string:station>/to/<string:station_list>')

api.add_resource(Fastest, '/fastest/<string:station>/to/<string:station_list>')

api.add_resource(ServiceDetails, '/service/<string:service_id>')

if __name__ == '__main__':
    app.run(debug=False)
