# Accuknox-Pvt-ltd-Assignment

## Features ✨

- **User Registration:** Allows new users to register.

- **User Login:** Allows users to log in and receive JWT tokens for authentication.

- **Friend Request System:**
  - **Send Friend Requests:** Users can send friend requests to other users.
  - **Rate Limiting:** Limits sending friend requests to a maximum of 3 per minute.
  - **Accept/Reject Friend Requests:** Users can accept or reject received friend requests.
  - **View Friends List:** Users can view their list of friends.
  - **Pending Friend Requests:** Users can view their pending friend requests.

- **User Search:** Allows users to search for other users by email or username.

## Tech Stack 🛠️

- **Backend Framework:** Django
- **API Framework:** Django REST Framework
- **Authentication:** JWT (JSON Web Tokens) with `djangorestframework-simplejwt`
- **Database:** MySQL
- **Environment Management:** Virtualenv (optional but recommended)
- **Dependencies Management:** pip

### Python Packages:

- Django==4.2.6
- djangorestframework==3.14.0
- djangorestframework-simplejwt==5.3.1
- mysqlclient==2.1.0




## Getting Started 🛠️

1. **Clone the Repository:**
   ```shell
   git clone https://github.com/adityaShar24/Accuknox-Pvt-ltd-Assignment.git

2. **Create and activate a virtual environment (optional but recommended)**
   ```shell
    python -m venv venv
    source venv/bin/activate  
    On Windows, use `venv\Scripts\activate`


3. **Install project Dependencies:** 
    ```shell
    pip install -r requirements.txt
 

4. **Apply Database Migrations (Step1):** 
    ```shell
    python manage.py makemigrations

6. **Apply Database Migrations (Step2):** 
    ```shell
    python manage.py migrate

7. **Create Superuser:** 
    ```shell
    python manage.py createsuperuser
    username: admin
    password: admin   

8. **Run Development Server:** 
    ```shell
    python manage.py runserver    


## Contributing 🤝

Feel free to contribute to enhance the functionality of Todo-Application. Follow the [contribution guidelines](CONTRIBUTING.md) for more details.

## License 📄
