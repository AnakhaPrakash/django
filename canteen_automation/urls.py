
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login',views.login),
    path('user_registration',views.user_registration),
    path('staff_registration',views.staff_registration),
    path('admin_home',views.admin_home),
    path('staff_home',views.staff_home),
    path('user_home',views.user_home),

    ############## Admin #################
    path('admin_add_staff_canteen',views.admin_add_staff_canteen),
    path('admin_view_canteen_staffs',views.admin_view_canteen_staffs),
    path('admin_update_canteen_staff',views.admin_update_canteen_staff),
    path('admin_delete_canteen_staff',views.admin_delete_canteen_staff),
    path('admin_view_teachers',views.admin_view_teachers),
    path('admin_view_students',views.admin_view_students),
    path('admin_view_collage_staffs',views.admin_view_collage_staffs),
    path('admin_view_feedbacks',views.admin_view_feedbacks),

    ############## Staff #################

    path('staff_add_food',views.staff_add_food),
    path('staff_view_foods',views.staff_view_foods),
    path('staff_update_food',views.staff_update_food),
    path('staff_delete_food',views.staff_delete_food),
    path('staff_view_bookings',views.staff_view_bookings),
    path('staff_add_tables',views.staff_add_tables),
    path('staff_view_tables',views.staff_view_tables),
    path('staff_remove_table',views.staff_remove_table),

    ############## User #################

    path('user_view_foods',views.user_view_foods),
    path('user_checkout_food',views.user_checkout_food),
    path('user_book_food',views.user_book_food),
    path('user_payment',views.user_payment),
    path('user_view_bookings',views.user_view_bookings),
    path('user_view_tables',views.user_view_tables),
    path('user_booking_table',views.user_booking_table),
    path('user_booked_table',views.user_booked_table),
    path('user_cancel_table',views.user_cancel_table),
    path('filter_food_user',views.filter_food_user),
    path('user_cancel_food',views.user_cancel_food),
    path('user_add_feedbacks',views.user_add_feedbacks),
    path('user_view_feedbacks',views.user_view_feedbacks),

]
