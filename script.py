import firebase_admin
from firebase_admin import credentials, storage
import os
import sys
import json

githubTempPath = '/Users/runner/work/_temp'

keyFilePath = githubTempPath  + '/service_account_key.json'

cred = credentials.Certificate(keyFilePath)
firebase_admin.initialize_app(cred, {
    'storageBucket' : 'ballwizard-app.appspot.com'
})


bucket = storage.bucket()

fileName = sys.argv[1]
dirname = os.path.dirname(os.path.realpath(__file__))
fileFullPath = dirname + '/' + fileName
blob = bucket.blob(fileName)

blob.upload_from_filename(fileFullPath)

blob.make_public()

print("your file url ", blob.public_url)
data = open(dirname + '/' + sys.argv[2])
lectures = bucket.blob("lectures.json")

file_data = lectures.download_as_bytes()
json_data = json.loads(file_data.decode('utf-8'))

json_file = json.load(data)
json_file["thumbnail"] = blob.public_url
print("before", len(json_data["lectures"]))
json_data["lectures"].append(json_file)
print("after", len(json_data["lectures"]))
json_data["id"][json_file["lecture_id"]] = json_file

for tag in json_file["tags"]:
	json_tag = json_data["tags"][tag[0]]
	if tag[1] >= 0.75:
		json_tag.insert(0, json_file["lecture_id"])
	elif 0.25 < tag[1] < 0.75:
		json_tag.insert(len(json_tag) // 2, json_file["lecture_id"])
	else:
		json_tag.append(json_file["lecture_id"])
		

lectures.upload_from_string(json.dumps(json_data), content_type="application/json")
lectures.make_public()
print(lectures.public_url)
