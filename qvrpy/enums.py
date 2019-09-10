###################################################################################################
# This file is part of a higher-level implementation of the QVR Pro API found at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/
#
# Version: 0.1
# Author: Grant Patterson
# Email: patterson.grant@gmail.com
#
###################################################################################################

from enum import Enum

class QVRPTZAction(Enum):
    """Enumerated values of Directions for PTZ commands"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UP_LEFT = "up_left"
    UP_RIGHT = "up_right"
    DOWN_LEFT = "down_left"
    DOWN_RIGHT = "down_right"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    FOCUS_FAR = "focus_far"
    FOCUS_NEAR = "focus_near"

class QVRLogType(Enum):
    """Enumerated values of Log Types for QVR Pro Logs"""
    SYSTEM_EVENTS = 1
    SYSTEM_CONNECTIONS = 2
    SURVEILLANCE_EVENTS = 3
    SURVEILLANCE_CONNECTIONS = 4
    SURVEILLANCE_SETTINGS = 5

class QVRLogLevel(Enum):
    """Enumerated values of Log Levels for QVR Pro Logs"""
    INFORMATION = 0
    WARNING = 1
    ERROR = 2

class QVRSortDirection(Enum):
    """Enumerated values for sorting of QVR Pro Logs"""
    ASCENDING = "ASC"
    DESCENDING = "DESC"

class QVRCamStatus(Enum):
    """Enumerated values for camera status"""
    NVR_CAM_CONNECTED = 'NVR_CAM_CONNECTED'
    NVR_CAM_CONNECT_IDLE = 'NVR_CAM_CONNECT_IDLE'
    NVR_CAM_CONNECTING = 'NVR_CAM_CONNECTING'
    NVR_CAM_UNDEFINED = 'NVR_CAM_UNDEFINED'

class QVRRecordingStatus(Enum):
    """Enumerated values for recording status for Cameras and Streams"""
    NOT_RECORDING = 'NOT_RECORDING'
    RECORDING = 'RECORDING'

class QVRStreamingProtocol(Enum):
    """Enumerated values for streaming protocols"""
    HLS = 'hls'
    RTMP = 'rtmp'
    RTSP = 'rtsp'