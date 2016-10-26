resource "aws_s3_bucket" "assets" {
    bucket = "${var.assets_bucket}"
    acl = "public-read"

    cors_rule {
        allowed_headers = ["*"]
        allowed_methods = ["GET"]
        allowed_origins = ["*"]
        expose_headers = ["ETag"]
        max_age_seconds = 4000
    }

    tags {
        Name = "candee"
        Group = "candee"
    }

}

resource "aws_s3_bucket_notification" "assets_bucket_notification" {
    bucket = "${aws_s3_bucket.assets.id}"
    lambda_function {
        lambda_function_arn = "${aws_lambda_function.image_resize.arn}"
        events = ["s3:ObjectCreated:*"]
        ## Filter conditions
        filter_prefix = "uploads/"
        filter_suffix = ".jpg"
    }
}
