import boto3
import argparse
import json
import os
import hashlib


def main(file_name, bucket_name, access_key, secret_key, upload_key_name="ohdsi_vocab.zip"):

    print(bucket_name)

    s3 = boto3.client("s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    bucket = s3.create_bucket(Bucket=bucket_name, ACL="public-read")

    upload_result = s3.upload_file(file_name, bucket_name, upload_key_name, ExtraArgs={'ACL': 'public-read'})

    with open("s3.ohdsi_vocab.download.txt", "w") as fw:
        fw.write("https://s3.amazonaws.com/%s/%s" % (bucket_name, upload_key_name))


if __name__ == "__main__":

    arg_parse_obj = argparse.ArgumentParser(description="Upload vocabulary files")
    arg_parse_obj.add_argument("-c", "--config-json-file-name", dest="config_json_file_name", default="config.json")

    arg_obj = arg_parse_obj.parse_args()
    config_json_file_name = arg_obj.config_json_file_name

    with open(config_json_file_name, "r") as f:
        config = json.load(f)

    access_key = config["ACCESS_KEY"]
    secret_key = config["SECRET_KEY"]

    ohdsi_vocabulary_path = config["ohdsi_vocabulary_path"]
    ohdsi_vocabulary_file_name = config["ohdsi_vocabulary_file_name"]
    s3_bucket_name = config["s3_ohdsi_bucket_name"]

    file_to_upload = os.path.join(ohdsi_vocabulary_path, ohdsi_vocabulary_file_name)

    raw_encrypted_bucket_name = s3_bucket_name

    encrypted_bucket_name = hashlib.sha1(raw_encrypted_bucket_name.encode("utf8")).hexdigest()

    main(file_to_upload, encrypted_bucket_name, access_key, secret_key)
