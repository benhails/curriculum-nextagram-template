from helpers import s3
from config import S3_BUCKET, S3_LOCATION, S3_PROFILE_IMAGES_FOLDER
from models.user import User
from flask import flash


'''
required kwargs: file, id, folder
'''

def upload_file_to_s3(acl="public-read", **kwargs):
    file = kwargs.get('file')
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            kwargs.get('folder') + file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
        flash('Image successfully uploaded', 'success')

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        flash("Something Happened: ", e)
        return e