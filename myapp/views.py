from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import*
from django.contrib.auth import authenticate
from django.contrib import messages
from django.utils import timezone
from datetime import date
from django.db.models import Q


# Create your views here.

def index(request):

    return render(request,"index.html")

def login(request):

    if request.POST:
        email=request.POST['email']
        password=request.POST['password']

        user=authenticate(username=email,password=password)

        if user:
            if user.is_active:
                if user.is_superuser:
                    return redirect('/admin_home')
                elif user.usertype=="user":
                    user = User_registration.objects.get(email=email)
                    request.session["email"] = email
                    request.session["id"] = user.id
                    return redirect('/user_home')
                
                elif user.usertype=="canteen_staff":
                    user = Staff_registration.objects.get(email=email)
                    request.session["email"] = email
                    request.session["id"] = user.id
                    return redirect('/staff_home')

    return render(request,"login.html")

def user_registration(request):

    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        contact=request.POST['contact']
        usertype=request.POST['usertype']
        email=request.POST['email']
        password=request.POST['password']
        id_card=request.FILES['id_card']
        profile_picture=request.FILES['profile_picture']

        log=Login_table.objects.create_user(username=email,password=password,usertype="user")
        log.save()

        regi=User_registration.objects.create(
            name=name,
            address=address,
            contact=contact,
            usertype=usertype,
            id_card=id_card,
            email=email,
            profile_picture=profile_picture,
            login_id=log
        )
        regi.save()
        messages.info(request,"Registration successful,You can login now")

    return render(request,"user_registration.html")

def staff_registration(request):

    if request.POST:
        name=request.POST['name']
        address=request.POST['address']
        contact=request.POST['contact']
        email=request.POST['email']
        password=request.POST['password']
        id_card=request.FILES['id_card']
        profile_picture=request.FILES['profile_picture']

        log=Login_table.objects.create_user(username=email,password=password,usertype="staff")
        log.save()

        regi=Staff_registration.objects.create(
            name=name,
            address=address,
            contact=contact,
            email=email,
            id_card=id_card,
            profile_picture=profile_picture,
            login_id=log
        )
        regi.save()
        messages.info(request,"Registration successful,Wait admin approvel")

    return render(request,"staff_registration.html")




####################### ADMIN ############################

def admin_home(request):

    return render(request,"admin/admin_home.html")

def admin_add_staff_canteen(request):

    if request.POST:
        name=request.POST['name']
        contact=request.POST['contact']
        profile_picture=request.FILES['profile_picture']
        email=request.POST['email']
        password=request.POST['password']

        log=Login_table.objects.create_user(
            username=email,password=password,usertype="canteen_staff"
        )
        log.save()

        staff=Staff_registration.objects.create(
            name=name,
            contact=contact,
            email=email,
            profile_picture=profile_picture,
            login_id=log
        )
        staff.save()
        messages.info(request,"Added successfully")

    return render(request,"admin/admin_add_staff_canteen.html")

def admin_view_canteen_staffs(request):

    staffs=Staff_registration.objects.all()

    return render(request,"admin/view_canteen_staffs_admin.html",{"staffs":staffs})

def admin_update_canteen_staff(request):

    tid=request.GET.get('id')
    staff=Staff_registration.objects.get(id=tid)
     
    if request.POST:
        name=request.POST['name']
        staff.name=name
        contact=request.POST['contact']
        staff.contact=contact
        profile_picture=request.FILES['profile_picture']
        staff.profile_picture=profile_picture

        staff.save()
        messages.info(request,"Updated successfully")
        return redirect('/admin_view_canteen_staffs')


    return render(request,"admin/admin_update_canteen_staff.html",{"staff":staff})

def admin_delete_canteen_staff(request):
    
    tid=request.GET.get('id')
    staff=Staff_registration.objects.get(id=tid)
    staff.delete()
    log=Login_table.objects.get(username=staff.login_id)
    log.delete()
    messages.info(request,"Deleted successfully")

    return redirect('/admin_view_canteen_staffs')

def admin_view_teachers(request):

    teachers=User_registration.objects.filter(usertype="teacher")

    return render(request,"admin/admin_view_teachers.html",{"teachers":teachers})

def admin_view_students(request):

    students=User_registration.objects.filter(usertype="student")

    return render(request,"admin/admin_view_students.html",{"students":students})

def admin_view_collage_staffs(request):

    collage_staffs=User_registration.objects.filter(usertype="collage_staff")

    return render(request,"admin/admin_view_collage_staffs.html",{"collage_staffs":collage_staffs})

def admin_view_feedbacks(request):

    feedbacks=User_feedbacks.objects.all()

    return render(request,"admin/admin_view_feedbacks.html",{"feedbacks":feedbacks})


####################### STAFF ############################

def staff_home(request):

    id=request.session['id']
    staff=Staff_registration.objects.get(id=id)

    return render(request,"staff/staff_home.html",{"staff":staff})

def staff_add_food(request):

    id=request.session['id']
    staff=Staff_registration.objects.get(id=id)

    if request.POST:
        name=request.POST["name"]
        price=request.POST["price"]
        category=request.POST["category"]
        quantity=request.POST["quantity"]
        food_image=request.FILES["food_image"]
        rating=request.POST["rating"]

        food=Add_food.objects.create(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            food_image=food_image,
            rating=rating,
            staff_id=staff,
            posted_date=timezone.now()
        )
        food.save()
        messages.info(request,"Added Successfully")
        return redirect('/staff_view_foods')

    return render(request,"staff/staff_add_food.html")

def staff_add_tables(request):

    id=request.session['id']
    staff=Staff_registration.objects.get(id=id)

    if request.POST:
        table_no=request.POST["table_no"]
        time_from=request.POST["time_from"]
        time_to=request.POST["time_to"]
        added_on=request.POST["added_on"]

        food=Add_table.objects.create(
            table_no=table_no,
            time_from=time_from,
            time_to=time_to,
            staff_id=staff,
            added_on=added_on
        )
        food.save()
        messages.info(request,"Added Successfully")
        return redirect('/staff_view_tables')

    return render(request,"staff/staff_add_table.html")

def staff_view_tables(request):

    id=request.session['id']
    staff_id=Staff_registration.objects.get(id=id)
    tables=Add_table.objects.all()


    return render(request,"staff/staff_view_tables.html",{"tables":tables})

def staff_remove_table(request):

    tid=request.GET.get('id')
    table=Add_table.objects.get(id=tid)
    table.delete()
    messages.info(request,"Remove table successfully")

    return redirect('/staff_view_tables')

def staff_view_foods(request):

    id=request.session['id']
    staff_id=Staff_registration.objects.get(id=id)
    foods=Add_food.objects.filter(staff_id=staff_id.id)


    return render(request,"staff/staff_view_foods.html",{"foods":foods})


def staff_update_food(request):

    fid=request.GET.get('id')
    food=Add_food.objects.get(id=fid)
    
    if request.POST:
        name=request.POST['name']
        food.name=name
        price=request.POST['price']
        food.price=price
        category=request.POST['category']
        food.category=category
        quantity=request.POST['quantity']
        food.quantity=quantity
        food_image=request.FILES['food_image']
        food.food_image=food_image
        rating=request.POST['rating']
        food.rating=rating

        food.save()
        messages.info(request,"Updated successful")
        return redirect('/staff_view_foods')

    return render(request,"staff/update_food.html",{"food":food})

def staff_delete_food(request):

    fid=request.GET.get('id')
    food=Add_food.objects.get(id=fid)
    food.delete()
    messages.info(request,"Removed Successfully")

    return redirect('/staff_view_foods')

def staff_view_bookings(request):

    id=request.session['id']
    staff_id=Staff_registration.objects.get(id=id)
    bookings=User_booking_food.objects.filter(food_id__staff_id=staff_id)

    return render(request,"staff/staff_view_bookings.html",{"bookings":bookings})



####################### USER ############################

def user_home(request):


    return render(request,"user/user_home.html")


def user_view_foods(request):

    foods=Add_food.objects.all()

    return render(request,"user/user_view_foods.html",{"foods":foods})


def user_checkout_food(request):
    fid = request.GET.get('id')
    food = Add_food.objects.get(id=fid)
    id = request.session['id']
    user = User_registration.objects.get(id=id)

    if request.POST:
        name = request.POST['name']
        quantity = request.POST['quantity']
        pick_up_time = request.POST['pick_up_time']
        
     
        quantity_int = int(quantity)
        
        if quantity_int > int(food.quantity):

            return render(request, "user/user_checkout_food.html", {
                'food': food,
                'error_message': 'Requested quantity exceeds available stock.'
            })
        
        booking = User_booking_food.objects.create(
            user_id=user,
            food_id=food,
            name=name,
            pick_up_time=pick_up_time,
            quantity=quantity_int,
            price=int(food.price) * quantity_int
        )

        booking.save()

        food.quantity = int(food.quantity)-quantity_int
        food.save()

        return redirect(f'/user_book_food?id={booking.id}')
    
    return render(request, "user/user_checkout_food.html", {'food': food})


def user_book_food(request):
    bid=request.GET.get('id')
    booking=User_booking_food.objects.get(id=bid)

    return render(request, "user/user_book_food.html",{"booking":booking})

def user_view_bookings(request):

    id=request.session['id']
    user_id=User_registration.objects.get(id=id)
    bookings=User_booking_food.objects.filter(user_id=user_id)


    return render(request,"user/user_view_bookings.html",{"bookings":bookings})

def user_cancel_food(request):

    bid=request.GET.get('id')
    booking=User_booking_food.objects.get(id=bid)
    booking.cancel_status=True
    booking.save()
    pid=booking.food_id
    booking_quantity=booking.food_id.quantity
    food=Add_food.objects.get(id=pid.id)
    food.quantity=int(food.quantity) + int(booking.quantity)
    food.save()
    messages.info(request,"Booking Cancelled")

    return redirect('/user_view_bookings')

def user_book_table(request):
    bid=request.GET.get('id')
    booking=Add_table.objects.get(id=bid)
    booking.booking_status=True,
    booking.booked_on=timezone.now()
    booking.save()
    messages.info(request,"Booked successfully")

    return render(request, "user/user_book_table.html",{"booking":booking})

def user_cancel_table(request):

    tid=request.GET.get('id')
    table=Add_table.objects.get(id=tid)
    table.booking_status=False
    table.booked_on=None
    table.user_id=None
    table.save()
    messages.info(request,"Cancellation successfull")


    return redirect('/user_view_tables')


def user_payment(request):

    bid=request.GET.get('id')
    booking=User_booking_food.objects.get(id=bid)
    booking.payment_status=True
    booking.booked_on=timezone.now()
    booking.save()
    # print(booking.price)

    if request.POST:
        pass
        return redirect('/user_view_bookings')
    messages.info(request,'Booking Confirmed')

    return render(request,"user/user_payment_page.html",{"booking":booking})

def user_view_tables(request):

    id=request.session['id']
    user_id=User_registration.objects.get(id=id)
    tables=Add_table.objects.all()

    return render(request,"user/user_view_tables.html",{"tables":tables})

def user_booking_table(request):

    id=request.session['id']
    user_id=User_registration.objects.get(id=id)
    tid=request.GET.get('id')
    table=Add_table.objects.get(id=tid)
    table.user_id=user_id
    table.booking_status=True
    table.booked_on=timezone.now()
    table.save()
    messages.info(request,"Booked successfully")

    return redirect('/user_view_tables')

def user_booked_table(request):

    id=request.session['id']
    user_id=User_registration.objects.get(id=id)
    tables=Add_table.objects.filter(user_id=user_id)

    return render(request,"user/user_booked_table.html",{"tables":tables})

def filter_food_user(request):

    category = Add_food.objects.values_list('category', flat=True).distinct()
    selected_type = request.GET.get('category', '')

    if selected_type:
        foods = Add_food.objects.filter(category=selected_type)
    else:
        foods = Add_food.objects.all()
    
    return render(request, 'user/filter_food_user.html',  {
        'foods': foods,
        'category': category,
        'selected_type': selected_type,
    })



def user_add_feedbacks(request):

    bid=request.GET.get('id')
    booking=User_booking_food.objects.get(id=bid)
    id=request.session['id']
    user=User_registration.objects.get(id=id)

    if request.POST:
        feedback=request.POST['feedback']
        rating=request.POST['rating']

        feed=User_feedbacks.objects.create(
            feedback=feedback,
            rating=rating,
            booking_id=booking,
            user_id=user,
            date=timezone.now()
        )
        feed.save()
        messages.info(request,"Feedback send successfully")
        return redirect('/user_view_feedbacks')

    return render(request,"user/user_add_feedbacks.html")

def user_view_feedbacks(request):

    feedbacks=User_feedbacks.objects.all()

    return render(request,"user/user_view_feedbacks.html",{"feedbacks":feedbacks})

