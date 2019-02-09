from flask import Flask
from flask_restful import Resource, Api

from .resources import CRS, Departures, FilteredDepartures, Arrivals, FilteredArrivals

app = Flask(__name__)
api = Api(app)

api.add_resource(CRS, '/crs')

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

if __name__ == '__main__':
    app.run(debug=False)
