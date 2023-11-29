import json
import os
import boto3
import requests
from google.cloud import storage
import base64
# encoded_private_key="ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiY3N5ZTYyMjUtZGV2LTQwNTcyMCIsCiAgInByaXZhdGVfa2V5X2lkIjogIjlhYmM0ZGY1OGIwZDY3YzdlZDhiMjZlODJiYzI3MWMwZjExY2Y0ZTgiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRRHUxd3lISmNIb2txOThcbjNSbStnQjNiQjdKMXRYV0FtZk84ZzFDTnVUNFNCV0JDa1JSUzhtUWVnOWtBR3ZqU2szLzZmTmZnYnNqREZLYWJcbklzdFY4eGtwR284Y0ZFbXNUT1AveUpIQ3d6a1Zja3FSNzJBRkVZMys4ODNPN0o4R2o2MWJVRzZaby9HVEJzY3BcbmZpaWNlYlFZMVJwMWRvOXFPZ3pyNHdSTFE1ekJQclRobjl0MW5KVWlLN3UrREdaN0RRWUFBWGxreWFsandPSHlcblpveXhzQVVseFA3eWRxUGFKVVRzTTFwWWw0dld2TXZmU3V0RUNqUlkxU2dXaWJISHN3RlFZYnJGdkJIVnZkWTZcbkZtMzBTU1IyWi8vcTJ1MHRacXI0OTd4V21VK1lwbVlnU1ZLTjYwNWhMc3RaU1k1Q1AzTEd1RmFtUGVQZ28zVGhcbmc3b0hsZEcxQWdNQkFBRUNnZ0VBSTVrWjNPcmJ3L1paQVp0U3d2b0ZlU2ZraVhiS1ZLaWRrM05mQmtDZDU4RzFcblh6YVFlT3gzejdTSEcyVHB3VGtLMGlMWmFqSVk2anFodW0ydE1OcFMzYlYvcndlM0UxOUNmRlZBcEc3RWkxWEZcbmw0cStIUU5JenI4MzVhZU83RU50NnpaSnhjeVJyUUJObnZtV3cvdS94Qk8vSmRMTi9WODVuYzd3VE9kKzdhNUpcbk9uL0ZLLzVDbVRja0Q4M1Frem9QU0xrMXNuVmE4SkRhZmtDdDltMithaktFRGNpQkRFRTRueG9HV016YmZPT1VcbmVYNDhSRHZVdWhMT1BSV1piWEI4d2Q5MXNXc1Y2RlhwMmdtT0lWY1BwaDhvbWNOUWFOUlo4aThkbkJScE5jVmlcbnZKQm5vbTlicmVDQSt5MTFzZE10WUZFQ3JHYURiRDB3dFZ6NHZzeStBUUtCZ1FEK0kvOFBueGd2OTd4ZEM3RGpcblZHMjdvbjduNzhEQjZWaUd5dDhyY3VoSkJtaVk1K2lHTkVpWTBLRHFya0pLMktKdUZ4aVZPQXpxZHJReTl2WVNcbjd1bVpJeFJ1TUJRd1o2NHVmM3IyY2gvWWgzQjVmUk1uVWpnQXJ5aVUvVHB1SWl6UU5sU3BLTFNtRitMUVJxdnlcbldtRGN5TUdTL3BoTHJHS0o0WHFSMi9qc01RS0JnUUR3bG1VTThlU3EvMmlGdU03UlZBemhDbmhXQnF2aHFYdVFcbnBHZlIyN2k0eFBpazdzS1AvL1ZJN1pZUlBnL3p5bGNpR3J1NWtwZGQyempaM3JDWDJTZm9iZnBJay9WRHJEczFcblFPbXF6T0FaRHhPblVtdmlEV0IrRm1ua0xEMW56T1MxOFFDQXBXV3I3RTVSSmZJVXNPb2piSC9PYW1UUUhNRlBcbi9jcE9wbFVReFFLQmdRQzlOZDJiS3M3ZVA2cWM5NnhOeERraW5wdXZZTi81UHhycTJEWUphamFvejcybVFkcnJcbnVCZG90c05ubGkvQys4RUxCK1VFaThPSitMQzIxUWxtRlR3VUNIc1lnbkUxakt1dzhMYUNyM3NvUWNZcW5VVmFcblhDdFh6eEQrdy8zeHF6NEVFcjg3WmhRQktQMTBKWG0xS1RhK2lqVWNsTEtjZkk2c3F4UVBibC9Jc1FLQmdGQlpcbjZtWG9ZL2E0VnJCU2lNQmcwZXhYRXRtb1lMOTlXMGR6b1RqMXFUd01qUDZJdjNKWWloTlJSazE3N05mL1BCcW5cbjB3cW5hdVp0MFE3eTBRZmwvdTRoelBWd2RQbWxEQ0U5RE0xK24xbS9MMUV5dGRWSm9uQjZDK09vNHRsSUZScXVcbjR2d1VRV0NxQzM0T3JrczZ5dmdKeEtXcjR2K2VtdkdjVVhUekdIWUJBb0dBTHl3QXQxOVlkSlYrKzMydzhrKzFcbnBBUGI4WkNwZWk3Q0E1eXhjME5uTXRkQjUvaXRjSGdQVmFYaHZVR053YUxpV0hJWGJnNmtBeStZYUtwYm1ZL0Ncbmt3Z0h2Q09saVhUNFFmVWhLMXNSVGJpU3Q5Sy8wVGR3ZGJXNm9nYnM2MkgxdHlGcjJZR0g5RmlxeHphWVA5V0Vcblc5SndxZWVpRkN3SmcrbUpOTnFvMTJFPVxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogImNzeWU2MjI1c3ctc3RvcmFnZUBjc3llNjIyNS1kZXYtNDA1NzIwLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExNDk3NTYxODg4MzQ2NjkxMzY4NSIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvY3N5ZTYyMjVzdy1zdG9yYWdlJTQwY3N5ZTYyMjUtZGV2LTQwNTcyMC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQo="

# decoded_private_key = base64.b64decode(encoded_private_key).decode('utf-8')
# private_key_json = json.loads(decoded_private_key)

# storage_client = storage.Client().from_service_account_json('/Users/haohao/Desktop/GCP_key/just-for-test-405823-07467969d801.json')
# storage_client = storage.Client().from_service_account_info(private_key_json)
# bucket = storage_client.bucket('test-bucket-sw')
# blob = bucket.blob('test/users.csv')
# blob.upload_from_filename('/usr/local/opt/users.csv')

email = 'wang.sijian1@northeastern.edu'

# requests.post(
# 		"https://api.mailgun.net/v3/demo.csye6225sw.me/messages",
# 		auth=("5d2b1caa-0cd75331", "5f158ec9655f15ced77d3b906fa998db-5d2b1caa-0cd75331"),
# 		data={"from": "Excited User <mailgun@demo.csye6225sw.me>",
# 			"to": [f'{email}'],
# 			"subject": "testMailGun",
# 			"text": "test the mailgun!"})

# assignment_id="assignment_id"
# file_url="url"
# update_date="date"
# num_of_attempts="3"


objectUrl = "csye6225-sw/wang.sijian1@northeastern.edu/b967f1b8-7b49-4936-9819-28182b79204a/6/submission.zip"
assignment_name = "Assignment chenges"
num_of_attempts = "6"
message = (
            f"Your assignment was received.<br>"
            f"Submission details:<br>"
            f"Assignment name: {assignment_name}<br>"
            f"Number of attempts: {num_of_attempts}<br>"
            f"<html><body>"
            f"Your submission saved at:{objectUrl}<br>"
            f"</body></html>"
        )

requests.post(
    "https://api.mailgun.net/v3/csye6225sw.me/messages",
    auth=("5d2b1caa-0cd75331", "5f158ec9655f15ced77d3b906fa998db-5d2b1caa-0cd75331"),
    data={"from": "Submission Notification <CSYE6225INFO@csye6225sw.me>",
        "to": [f'{email}'],
        "subject": 'Assignment6 Submission Notification',
        "html": message})

# requests.post(
#         "https://api.mailgun.net/v3/demo.csye6225sw.me/messages",
#         auth=(f'{api}', f'{api_key}'),
#         data={"from": "Webapp6225 <mailgun@demo.csye6225sw.me>",
#             "to": [f'{email}'],
#             "subject": "Your Assignment is Submitted",
#             "text": f"""Your Submission of {file_url} is recived at {update_date}
#                     Your number of attempts is: {num_of_attempts}
#                     """
#                     })

# encoded_private_key="ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAiY3N5ZTYyMjUtZGV2LTQwNTcyMCIsCiAgInByaXZhdGVfa2V5X2lkIjogIjlhYmM0ZGY1OGIwZDY3YzdlZDhiMjZlODJiYzI3MWMwZjExY2Y0ZTgiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRRHUxd3lISmNIb2txOThcbjNSbStnQjNiQjdKMXRYV0FtZk84ZzFDTnVUNFNCV0JDa1JSUzhtUWVnOWtBR3ZqU2szLzZmTmZnYnNqREZLYWJcbklzdFY4eGtwR284Y0ZFbXNUT1AveUpIQ3d6a1Zja3FSNzJBRkVZMys4ODNPN0o4R2o2MWJVRzZaby9HVEJzY3BcbmZpaWNlYlFZMVJwMWRvOXFPZ3pyNHdSTFE1ekJQclRobjl0MW5KVWlLN3UrREdaN0RRWUFBWGxreWFsandPSHlcblpveXhzQVVseFA3eWRxUGFKVVRzTTFwWWw0dld2TXZmU3V0RUNqUlkxU2dXaWJISHN3RlFZYnJGdkJIVnZkWTZcbkZtMzBTU1IyWi8vcTJ1MHRacXI0OTd4V21VK1lwbVlnU1ZLTjYwNWhMc3RaU1k1Q1AzTEd1RmFtUGVQZ28zVGhcbmc3b0hsZEcxQWdNQkFBRUNnZ0VBSTVrWjNPcmJ3L1paQVp0U3d2b0ZlU2ZraVhiS1ZLaWRrM05mQmtDZDU4RzFcblh6YVFlT3gzejdTSEcyVHB3VGtLMGlMWmFqSVk2anFodW0ydE1OcFMzYlYvcndlM0UxOUNmRlZBcEc3RWkxWEZcbmw0cStIUU5JenI4MzVhZU83RU50NnpaSnhjeVJyUUJObnZtV3cvdS94Qk8vSmRMTi9WODVuYzd3VE9kKzdhNUpcbk9uL0ZLLzVDbVRja0Q4M1Frem9QU0xrMXNuVmE4SkRhZmtDdDltMithaktFRGNpQkRFRTRueG9HV016YmZPT1VcbmVYNDhSRHZVdWhMT1BSV1piWEI4d2Q5MXNXc1Y2RlhwMmdtT0lWY1BwaDhvbWNOUWFOUlo4aThkbkJScE5jVmlcbnZKQm5vbTlicmVDQSt5MTFzZE10WUZFQ3JHYURiRDB3dFZ6NHZzeStBUUtCZ1FEK0kvOFBueGd2OTd4ZEM3RGpcblZHMjdvbjduNzhEQjZWaUd5dDhyY3VoSkJtaVk1K2lHTkVpWTBLRHFya0pLMktKdUZ4aVZPQXpxZHJReTl2WVNcbjd1bVpJeFJ1TUJRd1o2NHVmM3IyY2gvWWgzQjVmUk1uVWpnQXJ5aVUvVHB1SWl6UU5sU3BLTFNtRitMUVJxdnlcbldtRGN5TUdTL3BoTHJHS0o0WHFSMi9qc01RS0JnUUR3bG1VTThlU3EvMmlGdU03UlZBemhDbmhXQnF2aHFYdVFcbnBHZlIyN2k0eFBpazdzS1AvL1ZJN1pZUlBnL3p5bGNpR3J1NWtwZGQyempaM3JDWDJTZm9iZnBJay9WRHJEczFcblFPbXF6T0FaRHhPblVtdmlEV0IrRm1ua0xEMW56T1MxOFFDQXBXV3I3RTVSSmZJVXNPb2piSC9PYW1UUUhNRlBcbi9jcE9wbFVReFFLQmdRQzlOZDJiS3M3ZVA2cWM5NnhOeERraW5wdXZZTi81UHhycTJEWUphamFvejcybVFkcnJcbnVCZG90c05ubGkvQys4RUxCK1VFaThPSitMQzIxUWxtRlR3VUNIc1lnbkUxakt1dzhMYUNyM3NvUWNZcW5VVmFcblhDdFh6eEQrdy8zeHF6NEVFcjg3WmhRQktQMTBKWG0xS1RhK2lqVWNsTEtjZkk2c3F4UVBibC9Jc1FLQmdGQlpcbjZtWG9ZL2E0VnJCU2lNQmcwZXhYRXRtb1lMOTlXMGR6b1RqMXFUd01qUDZJdjNKWWloTlJSazE3N05mL1BCcW5cbjB3cW5hdVp0MFE3eTBRZmwvdTRoelBWd2RQbWxEQ0U5RE0xK24xbS9MMUV5dGRWSm9uQjZDK09vNHRsSUZScXVcbjR2d1VRV0NxQzM0T3JrczZ5dmdKeEtXcjR2K2VtdkdjVVhUekdIWUJBb0dBTHl3QXQxOVlkSlYrKzMydzhrKzFcbnBBUGI4WkNwZWk3Q0E1eXhjME5uTXRkQjUvaXRjSGdQVmFYaHZVR053YUxpV0hJWGJnNmtBeStZYUtwYm1ZL0Ncbmt3Z0h2Q09saVhUNFFmVWhLMXNSVGJpU3Q5Sy8wVGR3ZGJXNm9nYnM2MkgxdHlGcjJZR0g5RmlxeHphWVA5V0Vcblc5SndxZWVpRkN3SmcrbUpOTnFvMTJFPVxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogImNzeWU2MjI1c3ctc3RvcmFnZUBjc3llNjIyNS1kZXYtNDA1NzIwLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExNDk3NTYxODg4MzQ2NjkxMzY4NSIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvY3N5ZTYyMjVzdy1zdG9yYWdlJTQwY3N5ZTYyMjUtZGV2LTQwNTcyMC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQo="

# decoded_private_key = base64.b64decode(encoded_private_key).decode('utf-8')
# private_key_json = json.loads(decoded_private_key)
# assignment_id ="a"
# update_date = "b"
# num_of_attempts = "3"
# fail_content = "Your Submission for " + assignment_id + " is FAILED at " + update_date + \
#                        ". You may provided an invalid URL. Your number of attempts is: " + num_of_attempts + \
#                        "."
                       
# print(fail_content)