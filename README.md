# Avanc Project

## API Documentation

### Base URL

`http://127.0.0.1:8000/api/v1/`

### Endpoints

#### Employee List

- **GET** `/employees/`
  - Retrieves a list of all employees.
  - Response:
    ```json
    {
      "results": [
        {
          "id": "uuid",
          "full_name": "string",
          "employer": "uuid"
        },
        ...
      ]
    }
    ```

- **POST** `/employees/`
  - Creates a new employee.
  - Request Body:
    ```json
    {
      "full_name": "string",
      "email": "string",
      "phone": "string",
      "salary": "decimal",
      "employer": "uuid"
    }
    ```
  - Response:
    ```json
    {
      "id": "uuid"
    }
    ```

- **PUT** `/employees/`
  - Updates multiple employees.
  - Request Body:
    ```json
    [
      {
        "id": "uuid",
        "full_name": "string",
        "email": "string",
        "phone": "string",
        "salary": "decimal",
        "employer": "uuid"
      },
      ...
    ]
    ```
  - Response:
    ```json
    {
      "status": "success"
    }
    ```

#### Employee Detail

- **GET** `/employees/<uuid:pk>`
  - Retrieves details of a specific employee.
  - Response:
    ```json
    {
      "id": "uuid",
      "full_name": "string",
      "salary": "decimal",
      // ...other fields...
    }
    ```

- **POST** `/employees/<uuid:pk>`
  - Creates a new employee (same as POST `/employees/`).

- **PUT** `/employees/<uuid:pk>`
  - Updates a specific employee.
  - Request Body:
    ```json
    {
      "full_name": "string",
      "email": "string",
      "phone": "string",
      "salary": "decimal",
      "employer": "uuid"
    }
    ```
  - Response:
    ```json
    {
      "id": "uuid"
    }
    ```

#### Employee Transactions

- **GET** `/employees/<uuid:pk>/transactions`
  - Retrieves all transactions for a specific employee.
  - Response:
    ```json
    {
      "transactions": [
        {
          "id": "uuid",
          "amount": "decimal",
          "transaction_date": "datetime"
        },
        ...
      ]
    }
    ```

- **POST** `/employees/<uuid:pk>/transactions`
  - Creates a new transaction for a specific employee.
  - Request Body:
    ```json
    {
      "request_id": "uuid",
      "amount": "decimal"
    }
    ```
  - Response:
    ```json
    {
      "id": "uuid"
    }
    ```

#### Salary Advance Requests

- **GET** `/employees/<uuid:pk>/salary-advances`
  - Retrieves all salary advance requests for a specific employee.
  - Response:
    ```json
    {
      "salary_advance_requests": [
        {
          "id": "uuid",
          "amount_requested": "decimal",
          "status": "string",
          "request_date": "datetime",
          "review_date": "datetime"
        },
        ...
      ]
    }
    ```

- **POST** `/employees/<uuid:pk>/salary-advances`
  - Creates a new salary advance request for a specific employee.
  - Request Body:
    ```json
    {
      "amount_requested": "decimal"
    }
    ```
  - Response:
    ```json
    {
      "id": "uuid"
    }
    ```
