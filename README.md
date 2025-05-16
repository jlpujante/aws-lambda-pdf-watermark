# AWS Lambda PDF Watermark Function

## Description

This project is an **AWS Lambda function** designed to automatically process PDF files stored in an **Amazon S3 bucket**. When a PDF is uploaded or triggered, the function retrieves the file, applies a **custom watermark**, and generates a new PDF as output. The watermarked PDF is then saved back to a specified location in the S3 bucket.

## Key Features

- Serverless architecture using AWS Lambda
- Integration with Amazon S3 for file input and output
- Automatic watermarking of PDF files
- Scalable and event-driven processing

## Use Cases

- Document branding
- Confidentiality labeling
- Secure distribution of digital documents

## Technologies Used

- AWS Lambda
- Amazon S3
- Python
- PDF processing library (PyPDF4)

## Deployment Instructions

### Prerequisites

- AWS CLI configured with appropriate credentials
- An S3 bucket for input and output files
- Python 3.8+
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) or [Serverless Framework](https://www.serverless.com/framework/docs/getting-started)

### Deployment with AWS SAM (Serverless Application Model)

1. **Clone the repository:**

```bash
   git clone https://github.com/jlpujante/aws-lambda-pdf-watermark.git
   cd aws-lambda-pdf-watermark
````

2. **Build the Lambda package:**

   ```bash
   sam build
   ```

3. **Deploy the function:**

   ```bash
   sam deploy --guided
   ```

   Follow the prompts to specify the stack name, region, and S3 bucket for deployment artifacts.

4. **Set up the S3 trigger:**

   * Configure an S3 event notification to trigger the Lambda function on `ObjectCreated` events for `.pdf` files.

### Environment Variables

The Lambda function may require the following environment variables:

* `INPUT_BUCKET`: Name of the S3 bucket to read the PDF from
* `OUTPUT_BUCKET`: Name of the S3 bucket to save the watermarked PDF
* `WATERMARK_PDF`: PDF file to be used in the watermark

### Permissions

Ensure that the Lambda execution role has the following permissions:

* `s3:GetObject`
* `s3:PutObject`
* `logs:CreateLogGroup`
* `logs:CreateLogStream`
* `logs:PutLogEvents`

## Example Workflow

1. A PDF file is uploaded to the input S3 bucket.
2. The Lambda function is triggered by the upload event.
3. The function downloads the PDF, applies a watermark, and saves the new file.
4. The output watermarked PDF is uploaded to the output S3 bucket.

## License

MIT License

```
