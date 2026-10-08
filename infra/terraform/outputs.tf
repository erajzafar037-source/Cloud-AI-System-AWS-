output "api_url" {
  value = aws_apigatewayv2_api.http.api_endpoint
}

output "documents_bucket" {
  value = aws_s3_bucket.documents.bucket
}

output "ingestion_queue_url" {
  value = aws_sqs_queue.ingestion.url
}
