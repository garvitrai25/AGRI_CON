from django.urls import path

from .views import (add_complain, add_product, add_quantity, add_review,
                    add_to_cart, buy_page, checkout, contact, delete_product,
                    detail, edit_product, email_subscribe, home,
                    mark_notification_as_read, my_orders, order_detail,
                    order_success, payment, process_payment, remove_from_cart,
                    reply, sale_page, update_cart, update_order_status,
                    view_cart)

urlpatterns = [
    path('', home, name='home'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:id>/', edit_product, name='edit_product'),
    path('delete-product/<int:id>/', delete_product, name='delete_product'),
    path('add-quantity/<int:product_id>/', add_quantity, name='add_quantity'),
    path('sale-page/', sale_page, name='sale_page'),
    path('buy-page/', buy_page, name='buy_page'),
    path('reply/', reply, name='reply'),
    path('detail/<int:id>/', detail, name='detail'),
    path('contact/', contact, name='contact'),
    path('email-subscribe/', email_subscribe, name='email_subscribe'),
    path('add-complain/', add_complain, name='add_complain'),
    
    # Cart URLs
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('update-cart/<int:cart_id>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
    
    # Checkout and Order URLs
    path('checkout/', checkout, name='checkout'),
    path('payment/<int:order_id>/', payment, name='payment'),
    path('process-payment/<int:order_id>/', process_payment, name='process_payment'),
    path('order-success/<int:order_id>/', order_success, name='order_success'),
    path('my-orders/', my_orders, name='my_orders'),
    path('order-detail/<int:order_id>/', order_detail, name='order_detail'),
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
    
    # Review URL
    path('add-review/<int:product_id>/', add_review, name='add_review'),
    
    # Notification URL
    path('mark-notification-as-read/<int:notification_id>/', mark_notification_as_read, name='mark_notification_as_read'),
]
