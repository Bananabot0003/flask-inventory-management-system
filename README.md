
# Inventory Management System

A Python and Flask REST API for managing retail inventory.

## Project Overview

This project was developed as a summative assignment for the
Python REST API with Flask module.

The application supports full CRUD functionality, barcode-based
product retrieval from Open Food Facts, and a command-line interface.

## Features

- View all inventory items
- View individual products
- Add new inventory items
- Update product information
- Delete products
- Look up products by barcode
- Import Open Food Facts products into inventory
- Validate incoming requests
- Handle HTTP errors
- Run automated tests

## Technologies

- Python 3
- Flask
- Requests
- Pytest
- Open Food Facts API
- Git and GitHub

## Installation

Clone the repository:

    git clone git@github.com:Bananabot0003/flask-inventory-management-system.git

Enter the project:

    cd flask-inventory-management-system

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

## Running the API

Start the server:

    python app.py

The server runs at:

    http://127.0.0.1:5000

## Running the CLI

Keep Flask running and open another terminal.

Activate the virtual environment and run:

    python cli.py

Use the terminal menu to view, create, update, delete,
look up, and import products.

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Welcome message |
| GET | /api/health | Health check |
| GET | /inventory | List inventory |
| GET | /inventory/<id> | Get product |
| POST | /inventory | Add product |
| PATCH | /inventory/<id> | Update product |
| DELETE | /inventory/<id> | Delete product |
| GET | /products/lookup/<barcode> | Search Open Food Facts |
| POST | /inventory/import | Import external product |

## Example Product

    {
      "name": "Milk",
      "quantity": 10,
      "price": 3.99,
      "barcode": "0123456789"
    }

## HTTP Status Codes

- 200: Successful request
- 201: Resource created
- 204: Resource deleted successfully
- 400: Invalid request
- 404: Resource not found
- 503: External service unavailable

## External API

The application integrates with Open Food Facts.

Product details can be retrieved using a barcode.

Product name and barcode are imported automatically.
Inventory quantity and selling price are provided by the user.

## Testing

Run:

    python -m pytest -v

Tests cover inventory CRUD operations, Flask endpoints,
request validation, product lookup, imports, and error handling.

External API requests are mocked during automated testing.

## Project Limitations

Inventory is currently stored in memory.

Data does not persist after the server restarts.

This is an educational prototype rather than a
production-ready application.

Future improvements could include SQLite, authentication,
persistent storage, and a graphical administrator dashboard.

## Author

Hunter Williams

## License

Created for educational purposes.
