import json
import os
import boto3
import botocore
from PyPDF4 import PdfFileWriter, PdfFileReader

S3_BUCKET_NAME_IN = "pypdfwtrmrk"
S3_BUCKET_NAME_OUT = "pypdfwtrmrk"
S3_DEFAULT_WATERMAKR_FILE = "watermark-1.pdf"
S3_DEFAULT_OUTPUT_FILE = "output.pdf"
LAMBDA_LOCAL_FOLDER = "/tmp"

s3_client = boto3.client('s3')

def generate_file_watermark(input_pdf, output_pdf, watermark):
    watermark_instance = PdfFileReader(watermark)
    watermark_page = watermark_instance.getPage(0)
    pdf_reader = PdfFileReader(input_pdf)
    pdf_writer = PdfFileWriter()
    for page in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page)
        page.mergePage(watermark_page)
        pdf_writer.addPage(page)

    with open(output_pdf, 'wb') as out:
        pdf_writer.write(out)

def s3_key_exists(bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except botocore.exceptions.ClientError as e:
        return False

def lambda_handler(event, context):
    try:
        watermark_file_name = event.get('watermark_name', S3_DEFAULT_WATERMAKR_FILE)
        bname = event.get('bname', S3_BUCKET_NAME_IN)
        outfname = event.get('outfname', S3_DEFAULT_OUTPUT_FILE)
        fname = event.get('fname', None)

        if not fname:
            return {
                'statusCode': 400,
                'body': "fname not found",
            }

        s3_bucket_name = bname
        s3_file_name = fname
        if not s3_key_exists(s3_bucket_name, s3_file_name):
            return {
                'statusCode': 400,
                'body': f"key {s3_file_name} does not exists",
            }

        bucket = boto3.resource('s3').Bucket(s3_bucket_name)

        local_input_file = LAMBDA_LOCAL_FOLDER + '/' + s3_file_name
        bucket.download_file(s3_file_name, local_input_file)

        local_watermark_file = LAMBDA_LOCAL_FOLDER + '/' + watermark_file_name
        bucket.download_file(watermark_file_name, local_watermark_file)

        local_output_file = LAMBDA_LOCAL_FOLDER + '/' + outfname
        generate_file_watermark(local_input_file, local_output_file, local_watermark_file)
        s3_client.put_object(Bucket=S3_BUCKET_NAME_OUT, Key=outfname, Body=open(local_output_file, 'rb'))
        
        resp = dict(name=s3_bucket_name, file=s3_file_name)
        return {
            'statusCode': 200,
            'body': json.dumps(resp),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as err:
        print(err)
        return {
            'statusCode': 503,
            'body': "Error"
        }
