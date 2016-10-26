resource "aws_lambda_function" "image_resize" {
    filename = "../image_resize.zip"
    source_code_hash = "${base64sha256(file("../image_resize.zip"))}"
    description =  "A resizing job for images"
    function_name = "image_resize"
    runtime = "python2.7"
    timeout = 60
    memory_size = 128
    role = "${aws_iam_role.lambda_image_resizing_role.name}"
    handler = "lambda_function.handler"
}

resource "aws_lambda_permission" "allow_transcode_bucket" {
    statement_id = "AllowExecutionFromS3Bucket"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.image_resize.arn}"
    principal = "s3.amazonaws.com"
    source_arn = "${aws_s3_bucket.assets.arn}"
}
