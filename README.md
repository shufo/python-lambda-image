# python-lambda-image

A thumbnail image generator by AWS lambda (python).

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

```bash
$ cd terraform
$ export AWS_ACCESS_KEY_ID=foo
$ export AWS_SECRET_ACCESS_KEY=bar
$ export AWS_DEFAULT_REGION=us-east-1
$ vim variable.tf
variable "assets_bucket" {
  default = "your_bucket"
}

$ terraform plan
$ terraform apply
```

Redeploy if the function has changed.

```
$ terraform apply
```
