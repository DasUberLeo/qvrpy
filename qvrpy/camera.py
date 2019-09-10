from datetime import datetime
import re
from typing import List, Sequence

from .enums import QVRPTZAction
from .qvrapi import (
    cameraSnapshot as api_cameraSnapshot,
    cameraRecordingStart as api_cameraRecordingStart,
    cameraRecordingStop as api_cameraRecordingStop,
    cameraAlarmStart as api_cameraAlarmStart,
    cameraAlarmStop as api_cameraAlarmStop,
    cameraRecordingFile as api_cameraRecordingFile,
    cameraPTZStartMove as api_cameraPTZStartMove,
    cameraPTZStopMove as api_cameraPTZStopMove,
    cameraPTZ as api_cameraPTZ,
    streamList as api_streamList,
    )
from .stream import Stream

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

class Camera:
    """A representation of a Camera for QVR Pro"""

    def __init__(self, instance, camera_values: dict, stream_values: List[dict], username: str = None, password: str = None):
        self._instance = instance
        self.channel_index: int = _checkValue(camera_values, 'channel_index')
        self.name: str = _checkValue(camera_values, 'name')
        self.umsid: str = _checkValue(camera_values, 'umsid')
        self.guid: str = _checkValue(camera_values, 'guid')
        self.brand: str = _checkValue(camera_values, 'brand')
        self.model: str = _checkValue(camera_values, 'model')
        self.mac: str = _checkValue(camera_values, 'mac')
        self.ver: str = _checkValue(camera_values, 'ver')
        self.ip: str = _checkValue(camera_values, 'ip')
        self.port: int = _checkValue(camera_values, 'port')
        self.__username: str = username or _checkValue(camera_values, 'username')
        self.__password: str = password or _checkValue(camera_values, 'password')
        self.rtsp_port: int = _checkValue(camera_values, 'rtsp_port')
        self.http_video_url: str = _checkValue(camera_values, 'http_video_url')
        self.video_codec: str = _checkValue(camera_values, 'video_codec_setting')
        res = _checkVideoResolution(camera_values, 'video_resolution_setting')
        self.video_resolution_width: int = res[0]
        self.video_resolution_height: int = res[1]
        self.frame_rate_setting: str = _checkValue(camera_values, 'frame_rate_setting')
        self.video_quality: str = _checkVideoQuality(camera_values, 'video_quality_setting')
        self.status: QVRCamStatus = _checkValue(camera_values, 'status')
        self.rec_state: QVRRecordingStatus = _checkValue(camera_values, 'rec_state')
        self.rec_state_err_code: int = _checkValue(camera_values, 'rec_state_err_code')
        self.frame_rate: str = _checkValue(camera_values, 'frame_rate')
        self.bit_rate: int = _checkValue(camera_values, 'bit_rate')
        self.streams: List[Stream] = []
        for val in stream_values:
            self.streams.append(Stream(self, val, self.__username, self.__password))

    def getSnapShot(self, image_timestamp: datetime):
        """Return an image for this camera at the given timestamp"""
        return api_cameraSnapshot(self._instance.url, self._instance.sid, self.guid, image_timestamp)

    def startRecording(self) -> None:
        """Start recording for this Camera"""
        api_cameraRecordingStart(self._instance.url, self._instance.sid, self.guid)

    def stopRecording(self) -> None:
        """Stop recording for this Camera"""
        api_cameraRecordingStop(self._instance.url, self._instance.sid, self.guid)

    def startAlarm(self) -> None:
        """Start the Alarm for this Camera"""
        api_cameraAlarmStart(self._instance.url, self._instance.sid, self.guid)

    def stopAlarm(self) -> None:
        """Stop the Alarm for this Camera"""
        api_cameraAlarmStop(self._instance.url, self._instance.sid, self.guid)
        
    def startPTZMove(self, direction: QVRPTZAction) -> None:
        """Start a PTZ move for this Camera"""
        api_cameraPTZStartMove(self._instance.url, self._instance.sid, self.guid, direction.value)
        
    def stopPTZMove(self, direction: QVRPTZAction) -> None:
        """Stop a PTZ move for this Camera"""
        api_cameraPTZStopMove(self._instance.url, self._instance.sid, self.guid, direction.value)

    def doPTZAction(self, action: QVRPTZAction) -> None:
        """Perform a PTZ action for this Camera"""
        api_cameraPTZ(self._instance.url, self._instance.sid, self.guid, action.value)

    def getStream(self, stream_id: int = 0) -> Stream:
        """Get a stream matching the provided ID, where no ID is provided this will be Stream #0"""
        return self.streams[stream_id]

    def getStreamList(self) -> List[Stream]:
        """Get all streams for this Camera"""
        return self.streams

    def __str__(self):
        tempdict = self.__dict__.copy()
        del tempdict['_instance']
        del tempdict['_Camera__username']
        del tempdict['_Camera__password']
        templist = []
        for s in tempdict['streams']:
            templist.append(s.__str__())
        tempdict['streams'] = templist
        return tempdict.__str__()