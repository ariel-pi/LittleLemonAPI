## LittleLemon Django Project

This Django project named "LittleLemon" is a backend system for managing a food ordering service. It includes features such as managing menu items, user carts, orders, and user groups like managers, delivery crew, and customers.</b>

#### In the TryItYourself.md file, you can find examples of using the endpoints. 

### Requirements

- Python 3.x
- Django 4.1.2
- Additional Python packages can be found in the `requirements.txt` file.

### Setting Up the Project

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ariel-pi/LittleLemon.git
    cd LittleLemon
    ```

2. **Create a virtual environment:** *(recommended)*
    ```bash
    python -m venv env
    source env/bin/activate  # For Linux/Mac
    .\env\Scripts\activate  # For Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Database Setup:**
    - The project is configured to use SQLite by default. You can adjust the database settings in `LittleLemon/settings.py`.
    - Run migrations:
        ```bash
        python manage.py migrate
        ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the Admin Interface:**
    - Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and log in with the superuser credentials created.

### API Endpoints

- The project includes various API endpoints for managing categories, menu items, carts, orders, and user groups. Refer to `LittleLemonDRF/urls.py` for the API endpoints and their functionalities.

### Permissions and User Roles

- Different permissions are implemented using Django's `permissions` module. There are three user groups: Manager, Delivery crew, and Customer.
- Permissions are managed through custom `permissions.py` and implemented in views using Django's `permissions.BasePermission`.

### Contributors

- Ariel Pinhas - Sole Developer/Creator
- [GitHub](https://github.com/ariel-pi)
- [Linkdin](http://www.linkedin.com/in/ariel-pinhas)


