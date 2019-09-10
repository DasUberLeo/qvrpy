from datetime import datetime
from typing import Dict, List

from .camera import Camera
from .enums import QVRLogLevel, QVRLogType, QVRSortDirection
from .qvrapi import (
    authLogin as api_authLogin,
    authLogout as api_authLogout,
    cameraSearch as api_cameraSearch,
    cameraTest as api_cameraTest,
    cameraDetail as api_cameraDetail,
    cameraList as api_cameraList,
    streamList as api_streamList,
    cameraCapability as api_cameraCapability,
    eventCapability as api_eventCapability,
    cameraSupport as api_cameraSupport,
    cameraSnapshot as api_cameraSnapshot,
    logs as api_logs,
    channelList as api_channelList,
    )

class Instance:
    """Represents an instance of QVR Pro - effectively this is the core client"""

    def __init__(self, username: str, password: str, host: str, port: int, ssl: bool = False):
        """Initialise QVR Instance"""
        self.__username: str = username
        self.__password: str = password
        self.__cameras: Dict[str, Camera] = {}
        self.url = ('https://{0}:{1}' if ssl else 'http://{0}:{1}').format(host, str(port))
        self.sid = None

    def __loadCameras(self):
        """Load Camera Data from Instance"""
        self.__cameras = {}
        data = api_cameraList(self.url, self.sid)['datas']
        for camera_values in data:
            guid = camera_values['guid']
            stream_values = api_streamList(self.url, self.sid, guid)['streams']
            self.__cameras[guid] = Camera(self, camera_values, stream_values, self.__username, self.__password)
        data = api_cameraCapability(self.url, self.sid)
        data = api_eventCapability(self.url, self.sid)

    def connect(self) -> None:
        """Establish a connection to the instance and load camera data"""
        self.sid = api_authLogin(self.url, self.__username, self.__password)['authSid']
        self.__loadCameras()

    def disconnect(self) -> None:
        """Disconnect from the instance and remove camera data"""
        api_authLogout(self.url, self.sid)
        self.sid = None
        self.__cameras = None

    def doCameraSearch(self) -> List[Camera]:
        """Have the instance search the network for new cameras"""
        data = api_cameraSearch(self.url, self.sid)['data']
        cameras: List[Camera] = []
        for val in data:
            cameras.append(Camera(self, val))
        return cameras

    def getCameras(self) -> List[Camera]:
        """Get a list of Cameras connected to the instance"""
        if len(self.__cameras) == 0:
            self.__loadCameras()
        return self.__cameras.values()

    def getCamera(self, guid: str) -> Camera:
        """Get a single Camera by GUID"""
        return self.__cameras[guid]

    def getSupportedCameras(self) -> dict:
        """Get a dictionary of Brands and supported camera models for this instance"""
        brands = api_cameraSupport(self.url, self.sid)['brands']
        for brand in brands:
            brand['brand'] = brand['text']
            models = brand['models']
            del brand['models']
            del brand['text']
            del brand['value']
            for model in models:
                model['model'] = model['text']
                model['umsid'] = model['value']
                del model['text']
                del model['value']
            brand['models'] = models
        return brands

    def getLogs(self, log_type: QVRLogType, level: List[QVRLogLevel], user: str, source_ip: str, source_name: str, channel_id: List[int], global_channel_id: List[int], start_time: datetime, end_time: datetime, start_index: int, max_results: int, sort_field: str, sort_direction: QVRSortDirection) -> dict:
        """Return logs matching the specified criteria"""
        levels = []
        for l in level:
            levels.append(l.value)
        return api_logs(self.url, self.sid, log_type.value, str(levels), user, source_ip, source_name, str(channel_id), str(global_channel_id), start_time, end_time, start_index, max_results, sort_field, sort_direction)

    def getChannelList(self) -> dict:
        return api_channelList(self.url, self.sid)