# Purpose
The lambda function given works based on decorator principle. It serves the following purposes:
## 1. Logging Decorator
The logger_decorator logs messages before and after executing the handler function. It integrates with Python's built-in logging module to provide detailed execution logs.

## 2. Request Body Assertion Decorator
The request_body_assert_decorator ensures that required parameters are present in the HTTP request body. If any required parameter is missing, it returns a 400 HTTP response with an appropriate error message.

## 3. Parameter Validation Decorator
The parameter_validation_decorator validates parameters based on specified type and encoding requirements. It checks if the provided parameters match the expected types and formats. For instance, it verifies that the file parameter is a base64-encoded string before processing.

## 4. Excel Decoder Decorator
The excel_decoder_decorator decodes a base64-encoded Excel file from the HTTP request body. It reads the decoded data into a Pandas DataFrame, enabling data manipulation and analysis within the Lambda function.

## 5. Lambda Handler Function
The lambda_handler function serves as the main entry point. It integrates all decorators to handle the Lambda event, decode the Excel file, compute unique values for the segment column, and return the result as a JSON response with HTTP status code 200.

# Usage
To use this Lambda function:

## 1. Prepare an Excel File: Encode your Excel file in base64 format. You can use the provided encode_file_to_base64 function to convert your file.

## 2. Invoke the Lambda Function: Construct an event JSON with the base64-encoded file in the request body and invoke the Lambda function.

## 3. Result: The function will return a JSON response containing unique values counts for the specified column in the Excel file.

## 4. Replace the value of file_path variable inside main function with the actual path to your Excel file.
