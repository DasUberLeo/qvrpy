"""
Camera and Stream objects.

These represents a camera in QVR Pro, and video streams accessible for the Cameras
"""
import re
from typing import Sequence

from .enums import  QVRCamStatus, QVRStreamingProtocol
from .qvrapi import (
    liveStreamOpen as api_liveStreamOpen,
    liveStreamDelete as api_liveStreamDelete,
    )

_RESOLUTION_REGEX: re.Pattern = re.compile('(\d+)[xX*](\d+)')

def _checkValue(values: dict, key: str):
    if key in values:
        val = values[key]
        if val != None and (type(val) != str or len(val.strip()) > 0):
            return val
    return None

def _checkVideoResolution(values: dict, key: str) -> Sequence[int]:
    val: str = _checkValue(values, key)
    if val != None and type(val) == str:
       match = _RESOLUTION_REGEX.fullmatch(val.strip())
       if match != None:
           return (int(match.group(1)), int(match.group(2)))
       else:
           raise Exception("Bad Resolution Data: {0}".format(val))

def _checkVideoQuality(values: dict, key: str) -> str:
    val: str = _checkValue(values, key)
    if val != None:
        return val.replace(' ', '')

class Stream:
    """A representation of a Camera Stream in QVR Pro"""

    def __init__(self, camera, values: dict, username: str = None, password: str = None):
        self._camera = camera
        self.__username: str = username
        self.__password: str = password
#       Some cameras do not return with a stream, so a default is created based off the Camera
        if values != None:
            self.stream: int = values['stream']
            self.status: QVRCamStatus = _checkValue(values, 'status')
            self.video_codec: str = _checkValue(values, 'videoCodec')
            res = _checkVideoResolution(values, 'resolution')
            self.video_resolution_width: int = res[0]
            self.video_resolution_height: int = res[1]
            self.video_quality: str = _checkVideoQuality(values, 'quality')
            self.frame_rate: int = _checkValue(values, 'frameRate')
        self.__stream_url: str = None
        self.__token: str = None
        self.__protocol: QVRStreamingProtocol = None
            
    def openStream(self, protocol: QVRStreamingProtocol = QVRStreamingProtocol.RTSP) -> str:
        """Open a Stream using the selected protocol, the protocol defaults to RTSP"""
        #Store the returned stream URL and authorisation token, and return the URL
        response = api_liveStreamOpen(self._camera._instance.url, self._camera._instance.sid, self._camera.guid, self.stream, protocol.value)
        self.__protocol = protocol
        self.__stream_url = response['resourceUris']
        if self.__protocol == QVRStreamingProtocol.RTSP:
            self.__stream_url = self.__stream_url.replace('rtsp://', 'rtsp://{username}:{password}@'.format(username = self.__username, password = self.__password))
        if 'streamingToken' in response:
            self.__token = response['streamingToken']
        return self.__stream_url

    @property
    def streamURL(self) -> str:
        return self.__stream_url

    def closeStream(self) -> None:
        """Close the open stream"""
        if self.__protocol == QVRStreamingProtocol.RTSP:
            response = api_liveStreamDelete(self._camera._instance.url, self._camera._instance.sid, self._camera.guid, 'rtsp', None)
        else:
            response = api_liveStreamDelete(self._camera._instance.url, self._camera._instance.sid, self._camera.guid, self.stream, self.__token)
        self.__stream_url = None
        self.__token = None
        
    def __str__(self):
        tempdict = self.__dict__.copy()
        del tempdict['_camera']
        del tempdict['_Stream__username']
        del tempdict['_Stream__password']
        del tempdict['_Stream__stream_url']
        del tempdict['_Stream__token']
        return tempdict