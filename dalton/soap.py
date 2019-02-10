import zeep
from zeep import Client
from zeep import xsd
from zeep.plugins import HistoryPlugin
from boltons.iterutils import remap

WSDL = 'http://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx?ver=2017-10-01'

history = HistoryPlugin()

client = Client(wsdl=WSDL, plugins=[history])

header = xsd.Element(
    '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}AccessToken',
    xsd.ComplexType([
        xsd.Element(
            '{http://thalesgroup.com/RTTI/2013-11-28/Token/types}TokenValue',
            xsd.String()),
    ]))


def auth_header(token):
    return header(TokenValue=token)


def to_dict(soap_obj, full=None, **kwargs):
    data = zeep.helpers.serialize_object(soap_obj, **kwargs)
    return remap(data, lambda p, k, v: v is not None) if not full else data
