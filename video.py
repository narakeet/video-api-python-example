import os
from narakeet_api import VideoAPI

api_key = os.environ['NARAKEET_API_KEY']
video_directory_relative_path = 'video'
source_file_in_zip = 'source.txt'

def show_progress(progress_data):
    # change this to do something smarter with percent, message and thumbnail
    print(progress_data)

api = VideoAPI(api_key)

# zip up the directory with video assets
video_directory_full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), video_directory_relative_path)
video_zip = api.zip_directory_into_tempfile(video_directory_full_path)

# upload the zip to Narakeet
upload_token = api.request_upload_token()
api.upload_zip_file(upload_token, video_zip)
os.remove(video_zip)

# start a build task using the uploaded zip
# and wait for it to finish
task = api.request_build_task(upload_token, source_file_in_zip)
task_result = api.poll_until_finished(task['statusUrl'])

# grab the result file
if task_result['succeeded']:
    file = api.download_to_temp_file(task_result['result'])
    print(f'downloaded to {file}')
else:
    raise Exception(task_result['message'])
