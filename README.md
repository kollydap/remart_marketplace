# Giri Marketplace

Remart Marketplace is a Django-based application for managing products and users. This platform allows users to list and browse products, providing a seamless buying and selling experience.

## Features

- User authentication (login and signup).
- Product management (create, update, delete, and browse).
- Pagination support for product listings.
- Secure environment variable management using `.env` files.

## Installation

Follow the steps below to set up the project on your local machine:

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- virtualenv

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone https://github.com/kollydap/remart_marketplace.git
   cd remart_marketplace

   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:

   - Create a `.env` file in the project root.
   - Add the variables from the `.env.example` to the `.env` you created.

5. **Setup Database**:
   ```bash
   make setup
   ```
6. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

7. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

8. **Create Superuser**:

   ```bash
   python manage.py createsuperuser
   ```

9. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Usage

### Artisan Management

- Artisans can register and manage their products via the API endpoints.
- Users can view paginated lists of products associated with artisans.

### API Endpoints

Artisans ENdpoints

<!--
- `GET /api/v1/artisan-products/{artisan_id}/` - Retrieve
  products by a specific artisan (with pagination). -->

- `POST /api/v1/artisans/create/`
- `GET /api/v1/artisans/me/`
- `GET /api/v1/artisans/list/`
- `PUT /api/v1/artisans/update/`
- `DELETE /api/v1/artisans/delete/`

Auth Endpoints

- `POST /api/v1/auth/signup/` - Register a new user.
- `POST /api/v1/auth/login/` - Login an existing user.

Products Endpoints

- `GET /api/v1/products/` - Retrieve all products (with pagination).
- `GET /api/v1/products/:productId/` - retreive a particular product
- `POST /api/v1/products/create/` - create a product as an artisan
- `PUT /api/v1/products/update/:productId/` - update a particular product
- `DELETE /api/v1/products/delete/:productId/` - delete a particular product
- `GET /api/v1/products/artisan/:artisanId/` - get all products of an artisan

Orders Endpoints

- `GET /api/v1/orders/` - Retrieve all orders (normally should be restricted to admin, but for the sake of simplicity)
- `GET /api/v1/orders/:orderId/` - get a particular order by id
- `POST /api/v1/orders/create/` - create an order
- `PUT /api/v1/orders/update/:orderId/` - to update an order
- `DELETE /api/v1/orders/delete/:orderId/` - to delete an order

### Environment Variable Example

You can refer to `example.env` for a template of required environment variables:

```plaintext
SECRET_KEY=django-insecure-z^5*mxhz$4h%0u3iy^n_4p%!2(qd3kmwxocju0k!ebgvwcj^7c
DEBUG=True
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
NETWORK_NAME=mynetwork
POSTGRES_PORT=5432
PGADMIN_PORT=5050

```

## Development

### Git Ignore Configuration

The project uses a `.gitignore` file to avoid committing sensitive files. Files like `.env` are ignored, while `.env.example` is included as a template.

### Testing

Run tests to ensure the application works as expected:

```bash
python manage.py test
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes.
4. Push to your branch and create a pull request.

## Ideas for future

1. The status of order will be updated based on certain conditions

## License

This project is licensed under the MIT License. See the LICENSE file for details.
