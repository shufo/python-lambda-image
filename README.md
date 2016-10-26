# python-lambda-image

A script for creating thumbnail image by AWS lambda.

## Installation


```
pip install -r requirements.txt -t .
```

## Usage


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
