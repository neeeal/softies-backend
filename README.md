
# Skanin Backend
Make sure that the following are already installed in your workstation:
1. Python >=3.11.0 (https://www.python.org/downloads/)
> Python 3.11.4 was used in the development of this project.
2. Xampp (https://www.apachefriends.org/download.html)
> For running the databse locally, you will need to install Xampp.
3. Postman (https://www.postman.com/downloads/)
> Postman is optional and only for testing routes and endpoints.

## Flask Local Backend Documentation

This documentation explains how to interact with the provided Flask local backend for user-based requests, AI model transactions, and historical data retrieval. The backend comprises three files: `users.py`, `recommendation.py`, and `history.py`.

> Note that as of this writing November 11, 2023, all parameters should be submitted to the routes, even empty if must. Handling of imcomplete submissions will be done in future versions.

## users.py

### User Registration

- **URL:** `/signup` (POST)

- **Parameters:**
    - `username` (string): Desired username.
    - `password` (string): User's password.
    - `email` (string): User's email address.
    - `first_name` (string): User's first name.
    - `last_name` (string): User's last name.
    - `contact` (string): User's contact number.

- **Response:** A new user account is created if the credentials are valid.

### User Login

- **URL:** `/login` (POST)

- **Parameters:**
    - `username` (string): User's username.
    - `password` (string): User's password.

- **Response:** If the provided credentials are correct, the user is logged in.

### Update User Information

- **URL:** `/update_user` (POST)

- **Parameters:**
    - `username` (optional): New username.
    - `email` (optional): New email address.
    - `first_name` (optional): New first name.
    - `last_name` (optional): New last name.
    - `contact` (optional): New contact number.
    - `password` (string): Current password.
    - `new_password` (optional): New password.

- **Response:** User information is updated if the current password is valid.

### Get User Information

- **URL:** `/get_user` (GET)

- **Response:** Returns user information if the user is logged in.

### User Logout

- **URL:** `/logout` (GET)

- **Response:** Logs the user out.

## recommendation.py

### Predict Stress from Image

- **URL:** `/skan` (POST)

- **Parameters:**
    - `image` (file): Image data.

- **Response:** The AI model predicts stress from the image, and recommendations and stress details are returned.

## history.py

### Get Historical Data

- **URL:** `/get_history` (GET)

- **Response:** Returns the user's historical transaction data.

### Get Image from History

- **URL:** `/get_image/<int:image_num>` (GET)

- **Parameters:**
    - `image_num` (integer): Index of the image to retrieve.

- **Response:** Returns the requested image.
