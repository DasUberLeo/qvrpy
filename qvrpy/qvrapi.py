###################################################################################################
# This file is a python implementation of the QVR Pro API found at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/
#
# Version: 0.1
# Author: Grant Patterson
# Email: patterson.grant@gmail.com
#
# TODO:
#  - Test almost everything
#  - Implement unimplemented methods
#
# Implemented Methods:
#  - GET /cgi-bin/authLogin.cgi
#  - GET cgi-bin/authLogout.cgi
#  - GET /qvrpro/camera/search
#  - GET /qvrpro/camera/test
#  - GET /qvrpro/camera/list
#  - GET /qvrpro/camera/capability
#  - GET /qvrpro/camera/support
#  - GET /qvrpro/camera/snapshot/{guid}
#  - PUT /qvrpro/camera/mrec/{guid}/{action}
#  - ​PUT /qvrpro​/camera​/alarm​/{guid}​/{action}
#  - GET /qvrpro/camera/recordingfile/{guid}/{stream}
#  - PUT /qvrpro/ptz/v1/channel_list/{guid}/ptz/action_list/{action_id}/invoke
#  - GET /qvrpro/logs/logs
#  - GET /qvrpro/qshare/StreamingOutput/channels
#  - GET /qvrpro/qshare/StreamingOutput/channel/{guid}/streams
#  - POST /qvrpro/qshare/StreamingOutput/channel/{guid}/stream/{stream}/liveStream
#  - DELETE /qvrpro/qshare/StreamingOutput/channel/{guid}/stream/{stream}/liveStream
#
# Unimplemented Methods:
#  - GET /qvrpro/streaming/getstream.cgi
#  - GET /qvrpro/apis/qplay.cgi
#  - GET /qvrpro/qvrip/Vault/checkVaultName
#  - POST /qvrpro/qvrip/Vault/addVault
#  - POST /qvrpro/qvrip/Vault/removeVault
#  - PUT /qvrpro/qvrip/Vault/modifyVault
#  - GET /qvrpro/qvrip/Vault/getVaultList
#  - GET /qvrpro/qvrip/Vault/getVaultInfo/{vault_id}
#  - POST /qvrpro/qvrip/Filter/modifyFilter
#  - POST /qvrpro/qvrip/Filter/testFilter
#  - POST /qvrpro/qvrip/Filter/recvTestData
#  - DELETE /qvrpro/qvrip/Filter/stopRecvData
#  - POST /qvrpro/qvrip/Event/recvNotify/Generic/{vault_id}
#  - POST /qvrpro/qvrip/Metadata/Query
#
###################################################################################################

import base64
import json
import requests
from datetime import datetime
from xml.etree import ElementTree
from typing import List, Dict

__API_VERSION: str = '1.1.0'
__ERROR_CODES: dict = {
    '0xB1000000' : 'API version not support',
    '0xB1000001' : 'Authorization fail',
    '0xB1000002' : 'Insufficient permission',
    '0xB1000003' : 'Invalid Request: Illegal parameter or missing of parameter',
    '0xB1000004' : 'Invalid request',
    '0xB1000007' : 'API camera test fail',
    '0xB1000008' : 'generic error',
    '0xB1000009' : 'connection fail',
    '0xB100000A' : 'authentication fail',
    '0xB100000B' : 'set media config fail',
    '0xB100000C' : 'http reply fail',
    '0xB100000D' : 'model mismatch',
    '0xB100000E' : 'admin password incorrect',
    '0xB100000F' : 'guest password incorrect',
    '0xB1000010' : 'RTSP request fail',
    '0xB1000011' : 'RTP data not received',
    '0xB1000012' : 'JPEG success, MPEG4 RTSP fail',
    '0xB1000013' : 'JPEG success, MPEG4 RTP fail',
    '0xB1000014' : 'MPEG4 test locked',
    '0xB1000015' : 'user already login',
    '0xB1000016' : 'JPEG success, H264 RTSP fail',
    '0xB1000017' : 'JPEG success, H264 RTP fail',
    '0xB1000018' : 'H264 test locked',
    '0xB1000019' : 'RTSP DESCRIBE fail',
    '0xB100001A' : 'RTSP SETUP fail',
    '0xB100001B' : 'RTSP PLAY fail',
    '0xB100001C' : 'RTSP OPTION fail',
    '0xB100001D' : 'RTSP TEARDOWN fail',
    '0xB100001E' : 'Get camera info fail',
    '0xB100001F' : 'Get UMSID list fail',
    '0xB1000021' : 'Failed getting camera license info',
    '0xB1000022' : 'Failed getting license domain info',
    '0xC4000002' : 'missing request body',
    '0xC4000003' : 'missing parameter',
    '0xC4000004' : 'invalid argument',
    '0xC4000005' : 'authorization failed',
    '0xC400000A' : 'insufficient permissions',
    '0xC400000E' : 'invalid channel or channel license required',
    '0xC4000200' : 'failed to connect to database',
    '0xC4000502' : 'socket connection failed',
    '0xC4010001' : 'vault does not exist',
    '0xC4010006' : 'unknown vault type',
    '0xC4010007' : 'unknown connection type'
}

__URL_AUTH_LOGIN: str = '{url}/cgi-bin/authLogin.cgi'
__URL_AUTH_LOGOUT: str = '{url}/cgi-bin/authLogout.cgi'
__URL_CAMERA_SEARCH: str = '{url}/qvrpro/camera/search'
__URL_CAMERA_TEST: str = '{url}/qvrpro/camera/test'
__URL_CAMERA_LIST: str = '{url}/qvrpro/camera/list'
__URL_CAMERA_CAPABILITY: str = '{url}/qvrpro/camera/capability'
__URL_CAMERA_SUPPORT: str = '{url}/qvrpro/camera/support'
__URL_CAMERA_SNAPSHOT: str = '{url}/qvrpro/camera/snapshot/{guid}'
__URL_CAMERA_RECORDING: str = '{url}/qvrpro/camera/mrec/{guid}/{action}'
__URL_CAMERA_ALARM: str = '{url}/qvrpro/camera/alarm/{giod}/{action}'
__URL_CAMERA_RECORDINGFILE: str = '{url}/qvrpro/camera/recordingfile/{guid}/{stream}'
__URL_CAMERA_PTZ: str = '{url}​/qvrpro​/ptz​/v1​/channel_list​/{guid}​/ptz​/action_list​/{action_id}​/invoke'
__URL_LOGS: str = '{url}/qvrpro/logs/logs'
__URL_CHANNEL_LIST: str = '{url}/qvrpro/qshare/StreamingOutput/channels'
__URL_STREAM_LIST: str = '{url}/qvrpro/qshare/StreamingOutput/channel/{guid}/streams'
__URL_LIVESTREAM: str = '{url}/qvrpro/qshare/StreamingOutput/channel/{guid}/stream/{stream}/liveStream'

def __clean_json_response(value: str) -> str:
    """Removes erroneous characters/bad form from JSON responses"""
    return json.loads(value.replace('\n','').replace('\t','').replace('[}]','[]'))


# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Authorization/get_cgi_bin_authLogin_cgi
def authLogin(url: str, user: str, password: str) -> dict:
    """Get SID and log in"""
    params = {
        'user' : user,
        'serviceKey' : 1,
        'pwd' : base64.standard_b64encode(bytes(password, 'utf-8'))
        }
    response = requests.get(__URL_AUTH_LOGIN.format(url = url), params)
    if response.status_code == 200:
        tree = ElementTree.fromstring(response.text)
        data = {data.tag: tree.find(data.tag).text for data in tree}
        return data
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Authorization/get_cgi_bin_authLogout_cgi
def authLogout(url: str, sid: str) -> None:
    """Use SID to log out"""
    params = {
        'sid' : sid,
        'logout' : 1
        }
    response = requests.get(__URL_AUTH_LOGOUT.format(url = url), params)
    if response.status_code != 200:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Settings/get_qvrpro_camera_search
def cameraSearch(url: str, sid: str) -> dict:
    """Search for new cameras on the LAN via upnp and udp."""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION
        }
    response = requests.get(__URL_CAMERA_SEARCH.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Settings/get_qvrpro_camera_test
def cameraTest(url: str, sid: str, ipcam_umsid: str, ipcam_address: str, ipcam_port: int, ipcam_username: str, ipcam_password: str, ipcam_rtsp_port: int, ipcam_http_video_url: str, nvr_channel_id: int):
    """Test the connection of a single camera"""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION,
        'ipcam_umsid' : ipcam_umsid,
        'ipcam_address' : ipcam_address,
        'ipcam_port' : ipcam_port,
        'ipcam_username' : ipcam_username,
        'ipcam_password' : ipcam_password,
        'ipcam_rtsp_port' : ipcam_rtsp_port,
        'ipcam_http_video_url' : ipcam_http_video_url,
        'nvr_channel_id' : nvr_channel_id
        }
    response = requests.get(__URL_CAMERA_TEST.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Settings/get_qvrpro_camera_list
def __cameraList(url: str, sid: str, guid: str) -> dict:
    """Get the connection status and recording status of one or all cameras"""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION,
        'guid' : guid
        }
    response = requests.get(__URL_CAMERA_LIST.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
def cameraDetail(url: str, sid: str, guid: str) -> dict:
    """Get the connection status and recording status of one camera"""
    return __cameraList(url, sid, guid)
def cameraList(url: str, sid: str) -> dict:
    """Get the connection status and recording status of all cameras"""
    return __cameraList(url, sid, None)
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Settings/get_qvrpro_camera_capability
def __cameraCapability(url: str, sid: str, act: str) -> dict:
    """Get connection capability and recording status of one or all cameras"""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION,
        'act' : act
        }
    response = requests.get(__URL_CAMERA_CAPABILITY.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
def cameraCapability(url: str, sid: str) -> dict:
    """Get connection capability and recording status of one or all cameras"""
    return __cameraCapability(url, sid, 'get_camera_capability')
def eventCapability(url: str, sid: str) -> dict:
    """Get connection capability and recording status of one or all cameras"""
    return __cameraCapability(url, sid, 'get_event_capability')

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Settings/get_qvrpro_camera_support
def cameraSupport(url: str, sid: str):
    """Get all the supported cameras sorted by their brand and model"""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION
        }
    response = requests.get(__URL_CAMERA_SUPPORT.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Control/get_qvrpro_camera_snapshot__guid_
def cameraSnapshot(url: str, sid: str, guid: str, image_timestamp: datetime):
    """Get a snapshot image from the camera."""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION,
        'image_ts' : image_timestamp.isoformat
        }
    response = requests.get(__URL_CAMERA_SNAPSHOT.format(url = url, guid = guid), params)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Control/put_qvrpro_camera_mrec__guid___action_
def __cameraRecording(url: str, sid: str, guid: str, action: str) -> None:
    """Start/stop recording the particular camera."""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION
        }
    response = requests.get(__URL_CAMERA_RECORDING.format(url = url, guid = guid, action = action), params)
    if response.status_code == 200:
        return
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
def cameraRecordingStart(url: str, sid: str, guid: str) -> None:
    """Start recording the particular camera."""
    __cameraRecording(url, sid, guid, 'start')
def cameraRecordingStop(url: str, sid: str, guid: str) -> None:
    """Stop recording the particular camera."""
    __cameraRecording(url, sid, guid, 'stop')
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Control/put_qvrpro_camera_alarm__guid___action_
def __cameraAlarm(url: str, sid: str, guid: str, action: str) -> None:
    """Start/stop alarm output to a particular camera."""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION
        }
    response = requests.get(__URL_CAMERA_ALARM.format(url = url, guid = guid, action = action), params)
    if response.status_code == 200:
        return
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
def cameraAlarmStart(url: str, sid: str, guid: str):
    """Start alarm output to a particular camera."""
    __cameraAlarm(url, sid, guid, 'start')
def cameraAlarmStop(url: str ,sid: str, guid: str):
    """Stop alarm output to a particular camera."""
    __cameraAlarm(url, sid, guid, 'stop')
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20Control/get_qvrpro_camera_recordingfile__guid___stream_
def cameraRecordingFile(url: str, sid: str, guid : str, stream: int, time: datetime, pre_period: int, post_period: int):
    """Get a recording file from a specific time range."""
    params = {
        'sid' : sid,
        'ver' : __API_VERSION
        }
    response = requests.get(__URL_CAMERA_RECORDINGFILE.format(url = url, guid = guid, stream = stream), params)
    if response.status_code == 200:
        return response.content
    elif response.status_code == 403:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Camera%20PTZ/put_qvrpro_ptz_v1_channel_list__guid__ptz_action_list__action_id__invoke
def __cameraPTZ(url: str, sid: str, guid: str, action: str, direction: str) -> dict:
    """Move camera in different angles"""
    params = {
        'sid' : sid
        }
    if direction != None:
        params['direction'] = direction
    response = requests.put(__URL_CAMERA_PTZ.format(url = url, guid = guid, action_id = action), params = params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
def cameraPTZStartMove(url:str, sid: str, guid: str, direction: str) -> dict:
    """Start moving camera in different angles"""
    return __cameraPTZ(url, sid, guid, 'start_move', direction)
def cameraPTZStopMove(url: str, sid: str, guid: str, direction: str) -> dict:
    """Stop moving camera in different angles"""
    return __cameraPTZ(url, sid, guid, 'stop_move', direction)
def cameraPTZ(url: str, sid: str, guid: str, action: str) -> dict:
    """Start moving camera in different angles"""
    return __cameraPTZ(url, sid, guid, action, None)

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/SDK%20Logs/get_qvrpro_logs_logs
def logs(url: str, sid: str, log_type: int, level: str, user: str, source_ip: str, source_name: str, channel_id: str, global_channel_id: str, start_time: datetime, end_time: datetime, start_index: int, max_results: int, sort_field: str, sort_direction: str) -> dict:
    """Get logs in QVR Pro"""
    params = {
        'sid' : sid,
        'log_type' : log_type,
        'level' : level,
        'user' : user,
        'source_ip' : source_ip,
        'source_name' : source_name,
        'channel_id' : channel_id,
        'global_channel_id' : global_channel_id,
        'start_time' : start_time,
        'end_time' : end_time,
        'start' : start_index,
        'max_results' : max_results,
        'sort_field' : sort_field,
        'dir' : sort_direction
        }
    response = requests.get(__URL_LOGS.format(url = url), params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/Streaming%20Output:%20Channel%20list/get_qvrpro_qshare_StreamingOutput_channels
def channelList(url: str, sid: str) -> dict:
    """Return a list of channel infomation in QVR Pro."""
    params = {
        'sid' : sid
        }
    response = requests.get(__URL_CHANNEL_LIST.format(url = url), params = params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code in [401, 403]:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/Streaming%20Output:%20Streams/get_qvrpro_qshare_StreamingOutput_channel__guid__streams
def streamList(url: str, sid: str, guid: str) -> dict:
    """Return a list of stream information from a specific channel."""
    params = {
        'sid' : sid,
        }
    response = requests.get(__URL_STREAM_LIST.format(url = url, guid = guid), params = params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    elif response.status_code in [401, 403]:
        error_code = __clean_json_response(response.text)['error_code']
        raise Exception('{0}: {1}'.format(error_code, __ERROR_CODES[error_code]))
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))

# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/Streaming%20Output:%20Live%20stream/post_qvrpro_qshare_StreamingOutput_channel__guid__stream__stream__liveStream
def liveStreamOpen(url: str, sid: str, guid: str, stream: int, protocol: str) -> dict:
    """Open a livestream resource, a stream of a channel in QVR Pro, is available for users to access through RTMP, HLS, or RTSP."""
    params = {
        'sid' : sid,
        }
    data = {
        'protocol' : protocol
        }
    response = requests.post(__URL_LIVESTREAM.format(url = url, guid = guid, stream = stream), json = data, params = params)
    if response.status_code == 200:
        return __clean_json_response(response.text)
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))
        print(str(response))
    
# Documentation for this method is at
# http://petstore.swagger.io/?url=https://download.qnap.com/apidoc/qvrpro/qvr_pro_api_1.1.0.yaml#/Streaming%20Output:%20Live%20stream/delete_qvrpro_qshare_StreamingOutput_channel__guid__stream__stream__liveStream
def liveStreamDelete(url: str, sid: str, guid: str, stream: str, token: str) -> None:
    """Close a livestream resource, a stream of a channel in QVR Pro, is available for users to access through RTMP, HLS, or RTSP."""
    params = {
        'sid' : sid,
        }
    data = {
        'token' : token
        }
    response = requests.delete(__URL_LIVESTREAM.format(url = url, guid = guid, stream = stream), json = data, params = params)
    if response.status_code == 204:
        return
    else:
        raise Exception('HTTP Status Code {0}'.format(response.status_code))