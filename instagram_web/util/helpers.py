from helpers import s3
from config import S3_BUCKET, S3_LOCATION, S3_PROFILE_IMAGES_FOLDER, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from models.user import User
from models.image import Image
from flask import Flask, flash
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from authlib.integrations.flask_client import OAuth


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


def send_email(user, amount, image): 
    message = Mail(
        from_email = 'notifications@benstagram.com',
        to_emails = user.email,
        subject = 'Someone has just donated to your image!',
        html_content =
             f'Hi {user.name}'
             f'<br><br>'
             f'Someone has just donated <strong>${amount}</strong> to your image!'
             f'<br><br>'
             f'<img alt="{image.blurb}" src="{image.full_url}" width=25% height=25%>'   
             )
    try:
        sg = SendGridAPIClient(os.environ.get('SG_API_KEY_NAZ'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return response
    except Exception as e:
        print(e.message)
        return e


oauth = OAuth()
oauth.register('google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)
