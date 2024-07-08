# Product Management API

This repository contains the source code for the Product Management API, designed to manage products and their associated images. This API allows for CRUD operations on products, with authenticated access ensuring that users can only interact with products they own.

## Features

- **User Authentication**: Users can register, log in, and log out.
- **Product Management**: Authenticated users can create, retrieve, update, and delete products.
- **Image Uploads**: Users can upload multiple images for each product, with constraints on file size and number of images.
- **Secure Access**: Actions on products are secured, requiring users to authenticate using JWT (JSON Web Tokens).
- **Scalable Caching**: Uses Redis to manage token blacklisting and cache authentication details for performance enhancement.

## Design Patterns

- **Repository Pattern**: Used for abstracting the layer of data access logic.
- **Unit of Work Pattern**: Used for maintaining a list of objects affected by a business transaction and coordinates the writing out of changes.

## API Documentation

For detailed information about API endpoints and how to use them, refer to the API documentation hosted on Postman:

[API Documentation on Postman](https://documenter.getpostman.com/view/25778869/2sA3e2e9KD#b1e9aabc-9808-46c7-af25-dc5196e82526)
