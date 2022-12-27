import requests
import zipfile
import tempfile
import os
import json
import time

class VideoAPI:
    def __init__(self, api_key, api_url='https://api.narakeet.com', polling_interval=5):
        self.api_key = api_key
        self.api_url = api_url
        self.polling_interval = polling_interval

    def request_upload_token(self):
        url = self.api_url + '/video/upload-request/zip'
        headers = {'x-api-key': self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def zip_directory_into_tempfile(self, directory):
        temp = tempfile.NamedTemporaryFile(delete=False)
        zip_file = zipfile.ZipFile(temp, 'w')
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=file)
        zip_file.close()
        temp.close()
        return temp.name

    def upload_zip_file(self, upload_token, zip_archive):
        url = upload_token['url']
        headers = {'Content-Type': upload_token['contentType']}
        with open(zip_archive, 'rb') as f:
            response = requests.put(url, headers=headers, data=f)
            response.raise_for_status()


    def request_build_task(self, upload_token, source_file_in_zip):
        request = {
            'repositoryType': upload_token['repositoryType'],
            'repository': upload_token['repository'],
            'source': source_file_in_zip
        }
        url = f'{self.api_url}/video/build'
        headers = {'Content-Type': 'application/json', 'x-api-key': self.api_key}
        response = requests.post(url, headers=headers, json=request)
        response.raise_for_status()
        return response.json()

    def poll_until_finished(self, task_url, progress_callback=None):
        while True:
            response = requests.get(task_url)
            response.raise_for_status()
            data = response.json()
            if data['finished']:
                break

            if progress_callback:
                progress_callback(data)

            time.sleep(self.polling_interval)

        return data

    def download_to_temp_file(self, url):
        temp_file = tempfile.NamedTemporaryFile(prefix='video', suffix='.mp4', delete=False)
        response = requests.get(url)
        response.raise_for_status()
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

