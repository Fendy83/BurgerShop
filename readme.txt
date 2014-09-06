version of python: Python 2.7.3

The project Burger Shop allows users to order their burgers and administrators to change the status of orders.
There are four apps:

1. accounts:
   for managing login and logout

2. burgers:
   for displaying the page with all the ingredients

3. cart:
   for managing the cart of the user

4. checkout:
   for displaying the order form to the user, creating orders and changing the order status.

More Details about the implementation:

ACCOUNTS
In order to do login and logout, I have used the django.contrib.auth views, but custom template in the frontend.
In that way the administrator can login and logout directly from the website and not from the admin backend panel.

BURGERS
Ingredients are objects with an image. I have used django-filer for managing files.
It's possible to see a big picture of each ingredient by clicking on the image. I have used fancybox for that.

CART
Users can see ingredients and add them to the cart directly in the homepage.
Each ingredient can be added only one time and can be removed from the cart.
When the user has chosen all the ingredients, he can proceed with the order.
Each cart has a unique id, create in a random way and saved inside the session.
After the order is made, the cart will be empty.

CHECKOUT
The order form has one custom widget, the time widget, for selecting hours and minutes for the delivery.
Another custom form field is the phone field, to allow insertion of complex mobile number with '+' or '-' simbol in it
and spaces.
Administrator can see all the orders, only if he is logged in. Filtering is possible by status, using jQuery
to change the window location. Clicking on a single order, the administrator can see all the details and change
the status. The order details page is also visible if the user is logged in (permission 'login required' is the url page).
I have used the Update View for managing this feature.