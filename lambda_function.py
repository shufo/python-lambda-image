from PIL import Image
from PIL import _imaging
import boto3  
import os  
import re  
import subprocess
import config

s3 = boto3.client('s3')  

max_width = config.max_width
max_height = config.max_height
image_format = config.image_format
acl = config.acl
cjpeg_options = config.cjpeg_options
output_dir = config.output_dir
output_bucket = config.output_bucket
prefix = config.prefix
suffix = config.suffix

def handler(event, context):  
  bucket = event['Records'][0]['s3']['bucket']['name']  
  key = event['Records'][0]['s3']['object']['key']

  try:
    meta = metadata(bucket, key)
    # skip if image is already processed
    if 'image-processed' in meta and meta['image-processed'] == 'true':
      raise Exception('Already processed image')

    tmp = tmp_path(key)
    s3.download_file(Bucket=bucket, Key=key, Filename=tmp)

    # resize
    resized = resized_path(key)
    resize(tmp, resized)

    # mozjpeg (optimize)
    optimized = optimized_path(key)
    optimize(resized, optimized)

    # upload resized image
    upload(optimized, bucket, upload_path(key))

    return  

  except Exception as e:  
      print(e)  
      

def tmp_path(key):
  filename = os.path.basename(key)  
  return u'/tmp/' + filename 

def resized_path(key):
  filename = os.path.basename(key)  
  return '/tmp/{}.{}'.format(filename, image_format)

def resize(src, dest):
  # pil image processing
  img = Image.open(src, 'r')  
  img.thumbnail((max_width, max_height), Image.ANTIALIAS)  
  print 'format: ' + img.format
  if img.format == 'PNG' and image_format == 'jpg':
    img = img.convert('RGB')
  print 'image resized'
  return img.save(dest)
  
def optimize(src, dest):
  # mozjpeg (optimize)
  cmd = '{}/bin/cjpeg {} -outfile {} {}'.format(os.getcwd(), cjpeg_options, dest, src)
  subprocess.call(cmd, shell=True)
  print 'image optimized'
  return

def metadata(bucket, key):
  return s3.head_objec$t(Bucket=bucket, Key=key)['Metadata']

def download(bucket, key, dest):
  return s3.download_file(Bucket=bucket, Key=key, Filename=dest)  

def upload(src, bucket, dest):
  return s3.upload_file(Filename=src, Bucket=dest_bucket(bucket), Key=dest, ExtraArgs=extra_args())

def dest_bucket(bucket):
  return bucket if not output_bucket else output_bucket

def extra_args():
  return {'ContentType': content_type(), 'Metadata': {'image-processed': 'true'}, 'ACL': acl}

def content_type():
  if image_format in ['jpg', 'jpeg']:
    return 'image/jpeg'
  elif image_format == 'png':
    return 'image/png'
  else:
    return 'application/octet-stream'

def optimized_path(key):
  return '/tmp/{}_optimized.{}'.format(filename(key), image_format)

def filename(key):
  filename = os.path.basename(key)  
  name, ext = os.path.splitext(filename)
  return name

def upload_path(key):
  dirname = os.path.dirname(key)
  filename, ext = os.path.splitext(os.path.basename(key))
  return '{0}{1}/{2}{3}{4}.{5}'.format(output_dir, dirname, prefix, filename, suffix, image_format)

