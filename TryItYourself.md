# Try it yourself! #
## what is here? ##  
Examples of using the endpointsץ
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
         "category_id": 1
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
