## LittleLemon Django Project

This Django project named "LittleLemon" is a backend system for managing a food ordering service. It includes features such as managing menu items, user carts, orders, and user groups like managers, delivery crew, and customers.

### Requirements

- Python 3.x
- Django 4.1.2
- Additional Python packages can be found in the `requirements.txt` file.

### Setting Up the Project

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LittleLemon.git
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


## Try it yourself!
## what is here? ##  
This file contains the tests that must be done for the project.  
## How to use the file? ##  
- For each test it is written what is the endpoint that allows the test to be performed, what method to use and what payload is required to be attached if required.  
- For those who use Insomnia, the payload can be attached as a URL Encoded Form.  
- Please note that the parameters in the payload are examples only and other parameters can also be inserted.  

## Which django libraries are required to be installed by pip? ##  
- django  
- django-filter  
- djangorestframework  
- djangorestframework-xml  
- djoser  

## the tests ##
1. **The admin can assign users to the manager group**  
   - endpoint: /api/groups/manager/users  
   - method: POST  
   - payload: {"username":"Mario"}

2. **You can access the manager group with an admin token**  
   - endpoint: /api/groups/manager/users  
   - method: GET

3. **The admin can add menu items**  
   - endpoint: /api/menu-items  
   - method: POST  
   - payload:  
     {
         "id": 1,
         "title": "Vegan Pasta",
         "price": "7.00",
         "featured": 0,
         "category": 1
     }

4. **The admin can add categories**  
   - from the admin panel

5. **Managers can log in**  
   - endpoint: api/token/login/  
   - method: POST  
   - payload: {"username":"Mario", "password":"lemon@mar!"}

6. **Managers can update the item of the day**  
   - endpoint: /api/menu-items/{menuItem}  
   - Note: {menuItem} == id  
   - method: PATCH  
   - payload: {"featured":1}

7. **Managers can assign users to the delivery crew**  
   - endpoint: /api/groups/delivery-crew/users  
   - method: POST  
   - payload: {"username":"Adrian"}

8. **Managers can assign orders to the delivery crew**  
   - endpoint: /api/orders/{orderId}  
   - method: PATCH  
   - payload: {"delivery_crew_name":"Adrian"}

9. **The delivery crew can access orders assigned to them**  
   - endpoint: /api/orders  
   - method: GET

10. **The delivery crew can update an order as delivered**  
    - endpoint: /api/orders/{orderId}  
    - method: PATCH  
    - payload: {"status":1}

11. **Customers can register**  
    - endpoint: /api/users/  
    - method: POST  
    - payload: {"username":"Alex", "password":"lemon@ale!", "email":"alex@littlelemon.com"}

12. **Customers can log in using their username and password and get access tokens**  
    - endpoint: /api/token/login/  
    - method: POST  
    - payload: {"username":"Alex", "password":"lemon@ale!"}

13. **Customers can browse all categories**  
    - endpoint: /api/categories  
    - method: GET

14. **Customers can browse all the menu items at once**  
    - endpoint: /api/menu-items

15. **Customers can browse menu items by category**  
    - endpoint: /api/menu-items?category={category}  
    - method: GET

16. **Customers can paginate menu items**  
    - endpoint: /api/menu-items?page_size=3&page=2  
    - Note: page_size=3 and page=2 is just an example  
    - method: GET

17. **Customers can sort menu items by price**  
    - endpoint: /api/menu-items?ordering=price  
    - method: GET

18. **Customers can add menu items to the cart**  
    - endpoint:/api/cart/menu-items  
    - method: POST  
    - payload: {'menuitem_id: 1}

19. **Customers can access previously added items in the cart**  
    - endpoint:/api/cart/menu-items  
    - method: GET

20. **Customers can place orders**  
    - endpoint: /api/orders  
    - method: POST

21. **Customers can browse their own orders**  
    - endpoint: /api/orders  
    - method: GET
