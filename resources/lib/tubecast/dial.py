# -*- coding: utf-8 -*-
from bottle import Bottle, request, response

from resources.lib.kodi import kodilogging
from resources.lib.tubecast.kodicast import Kodicast
from resources.lib.tubecast.utils import build_template
from resources.lib.tubecast.youtube.app import YoutubeCastV1

logger = kodilogging.get_logger()

__device__ = '''<?xml version="1.0" encoding="utf-8"?>
    <root xmlns="urn:schemas-upnp-org:device-1-0">
        <specVersion>
            <major>1</major>
            <minor>1</minor>
        </specVersion>
        <device>
            <deviceType>urn:schemas-upnp-org:device:dial:1</deviceType>
            <friendlyName>{{ friendlyName }}</friendlyName>
            <manufacturer>Bobpril LLC.</manufacturer>
            <modelName>Bobpril TV Device</modelName>
            <UDN>uuid:{{ uuid }}</UDN>
            <serviceList>
                <service>
                    <serviceType>urn:schemas-upnp-org:service:dial:1</serviceType>
                    <serviceId>urn:upnp-org:serviceId:dial</serviceId>
                    <controlURL>/ssdp/notfound</controlURL>
                    <eventSubURL>/ssdp/notfound</eventSubURL>
                    <SCPDURL>/ssdp/notfound</SCPDURL>
                </service>
            </serviceList>
        </device>
    </root>'''


class DIALApp(Bottle):
    def __init__(self):
        super(DIALApp, self).__init__()
        # Register the Youtube application in the DIAL server.
        self.youtube_app = YoutubeCastV1(self)


app = DIALApp()


@app.route('/ssdp/device-desc.xml')
def service_desc():
    ''' route for DIAL service discovery '''
    response.set_header('Access-Control-Allow-Method',
                        'GET, POST, DELETE, OPTIONS')
    response.set_header('Access-Control-Expose-Headers', 'Location')
    response.set_header('Application-URL',
                        'http://{}/apps'.format(request.get_header('host')))
    logger.debug('http://{}/apps'.format(request.get_header('host')))
    logger.debug(Kodicast.uuid)
    response.set_header('Content-Type', 'application/xml')
    return build_template(__device__).render(
        friendlyName=Kodicast.friendlyName,
        uuid=Kodicast.uuid,
        path="http://%s" % request.get_header('host')
    )


@app.error(404)
def error404(error):
    ''' Default error message to override the one provided by bottle '''
    return 'Only Youtube is supported'
