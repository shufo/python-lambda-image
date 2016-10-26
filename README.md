# python-lambda-image

A script for creating thumbnail image by AWS lambda.

## Installation


```
pip install -r requirements.txt -t .
```

## Usage

- Set config

`config.py`

```python
max_width = 800
max_height = 800
image_format = 'jpg'
acl = 'public-read'
cjpeg_options = '-optimize -progressive'
output_dir = '/resized'
output_bucket = 'output_bucket'
prefix = 'thumb_'
suffix = '_resized'
```

- make package for lambda


```bash
$ make package
# Generates image_resize.zip
```

### Cygwin

If you're using cygwin, please make package in linux environment because cygwin can't holds permission while make package.

## Deployment

This will create an s3 bucket, a lambda function and an iam role for lambda.

```
$ cd terraform
$ terraform plan
$ terraform apply
```

Redeploy if the function has changed.

```
$ terraform apply
```
