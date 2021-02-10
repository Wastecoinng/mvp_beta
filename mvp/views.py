from django.shortcuts import render, redirect
import datetime
import json
import requests
import jwt
# from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from mvp.models import (User,otp, HubLocation, EmailCollector,Notification, Transaction, RecycledItems, Manufacturer,BrandCollector, Hub_User)
from CustomCode import (autentication,  password_functions,
                        string_generator, validator, barcode)
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wastecoin import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import HttpResponse

# Create your views here.

# # email test screen 
# def test(request):
#     if request.method == 'GET':
#         return render(request,"onboarding/email_temp.html") 

# splash screen 
def splash(request):
    if request.method == 'GET':
        return render(request,"onboarding/splashscreen.html") 

#location bot
def location_bot(request):
    return render(request,"location_bot/bot.html") 

# signin screen  
def signin(request):
    if request.method == 'GET':
        return render(request,"onboarding/signin.html")

# contact us screen
def contact_us(request):
    user_id = request.session['user_id']
    try:
        userID = user_id
        UserInfo = User.objects.get(user_id=userID)
        return_data = {
            "error": False,
            "message": "Successfull",
            "data": {
                "user_details": {
                "first_name": f"{UserInfo.firstname}",
                "last_name": f"{UserInfo.lastname}",
                "email": f"{UserInfo.email}",
                "phone_number": f"{UserInfo.user_phone}",
                }
            }
        }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/contact.html", return_data)

# contact us screen
def faq(request):
    user_id = request.session['user_id']
    try:
        userID = user_id
        UserInfo = User.objects.get(user_id=userID)
        return_data = {
            "error": False,
            "message": "Successfull",
            "data": {
                "user_details": {
                "first_name": f"{UserInfo.firstname}",
                "last_name": f"{UserInfo.lastname}",
                "email": f"{UserInfo.email}",
                "phone_number": f"{UserInfo.user_phone}",
                }
            }
        }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/faq.html", return_data)
# signout api     
def signout(request):
    if 'is_LoggedIn' in request.session:
        del request.session['is_LoggedIn']
    if 'token' in request.session:
        del request.session['token']
    return redirect('/signin')

# signup screen 
def signup(request):
    if request.method == 'GET':
        return render(request,"onboarding/signup.html")  

# re-activate account screen 
def activate_account(request):
    if request.method == 'GET':
        return render(request,"onboarding/activate_account.html") 

# forogt password screen 
def forgot_password(request):
    if request.method == 'GET':
        return render(request,"onboarding/forgot_password.html") 
# wallet screen 
# def wallet(request):
#     if request.method == 'GET':
#         return render(request,"user/wallet.html") 

# profile screen 
def notification(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        # readMessage = notification
        notification = Notification.objects.filter(sender="Admin")
        return_data = {
            "error": False,
            "notification": notification
        }
        return render(request,"user/notification.html", return_data) 

# profile screen 
# def profile(request):
#     if request.method == 'GET':
#         return render(request,"user/profile.html") 

# scanner screen 
# def scanner(request):
#     if request.method == 'GET':
#         return render(request,"user/scanner.html") 


# ONBOARDING APIS
# SIGN UP API
@api_view(["POST"])
def signup_api(request):
    try:
        firstName = request.data.get('firstname',None)
        lastName = request.data.get('lastname',None)
        phoneNumber = request.data.get('phonenumber',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        address = request.data.get('address',None)

        council = request.data.get('council',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)
        reg_field = [firstName,lastName,phoneNumber,email,password,address]
        if not None in reg_field and not "" in reg_field:
            if User.objects.filter(user_phone =phoneNumber).exists() or User.objects.filter(email =email).exists():
                return_data = {
                    "error": True,
                    "message": "User Exists"
                }
            # elif validator.checkmail(email) == False or validator.checkphone(phoneNumber)== False:
            elif validator.checkmail(email) == False:
                return_data = {
                    "error": True,
                    "message": "Email is Invalid"
                }
            else:
                #generate user_id
                userRandomId = string_generator.alphanumeric(6)
                #encrypt password
                encryped_password = password_functions.generate_password_hash(password)
                #Save user_data
                new_userData = User(user_id=userRandomId,firstname=firstName,lastname=lastName,
                                email=email,user_phone=phoneNumber,
                                user_password=encryped_password,user_address=address, user_state=state, user_council_area=council, user_country=country)
                new_userData.save()
                #Generate OTP
                code = string_generator.numeric(6)
                #Save OTP
                user_OTP =otp(user=new_userData,otp_code=code, validated=False)
                user_OTP.save()

                # Get User Validation
                validated = otp.objects.get(user__user_id=userRandomId).validated
                #Generate token
                timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=1440) #set duration for token
                payload = {"user_id": f"{userRandomId}",
                           "validated": validated,
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                
                # send verifcation to email 
                current_site = get_current_site(request)
                mail_subject = 'Activate your WasteCoin account.'
                message = render_to_string('onboarding/activate_email.html', {
                    'user': firstName,
                    'domain': current_site.domain,
                    'otp': code,
                })
                to_email = email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.content_subtype = 'html'
                email.send()
                return_data = {
                    "error": False,
                    "message": "Registrated successfully. Kind check your email to activate your account.",
                    }
        else:
            return_data = {
                "error":True,
                "message": "One or more fields is empty!"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
            # "message": "Something went wrong!"
        }
    return Response(return_data)

# email activation 
def activate(request, otp_code):
    # try:
    otpCode = otp.objects.get(otp_code=otp_code)  
    if otpCode:
        otpCode.validated = True
        otpCode.save()
        return_data = {
            "error": False,
            "message": 'Your Account is now verified. Kindly login via the app.'
        }
        return render(request,"onboarding/email_feedback.html", return_data)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return_data = {
            "error": True,
            "message": 'Sorry, Activation link is invalid!'
        }
        return render(request,"onboarding/email_feedback.html", return_data)
        # return HttpResponse('Activation link is invalid!')

# change password page  
def change_password(request, uid):
    userDetails = User.objects.get(user_id=uid)

    if userDetails:
        return_data = {
        "error": False,
        "uid": uid,
        # "message": "Password Changed Successfully! "
        }
        return render(request,"onboarding/change_password.html", return_data)
    else:
        return_data = {
            "error": True,
            "message": 'Sorry, You are not authorised to access this link!'
        }
        return render(request,"onboarding/email_feedback.html", return_data)

@api_view(["POST"])
def change_password_api(request):
    try:
        uid = request.data.get("uid",None)
        confirm_password = request.data.get("c_confirm_new_password",None)
        new_password = request.data.get("c_new_password",None)
        user_data = User.objects.get(user_id=uid)  
        
        if user_data:
            if new_password != confirm_password:
                return_data = {
                    "error": True,
                    "uid":uid,
                    "message": "Password dont match!"
                }
            else:
                encryptpassword = password_functions.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": False,
                    "message": "Password Changed Successfully! Kindly login via the app"
                }
                return render(request,"onboarding/email_feedback.html", return_data)

        else:
            return_data = {
                "error": True,
                "message": 'Sorry, You are not Authorized to access this link!'
            }
    except Exception as e:
        return_data = {
                "error": True,
                "uid":uid,
                # "message": str(e)
                "message": 'Sorry, Something went wrong!'
            }
    return render(request,"onboarding/change_password.html", return_data)

#SEND ACTIVATION LINK API
@api_view(["POST"])
def send_activation_link_api(request):
    try:
        email = request.data.get("email",None)
        userDetails = User.objects.get(email=email) 
        userValidation = otp.objects.get(user=userDetails).validated 
        
        if userDetails and userValidation == False:
            code_retrieved = otp.objects.get(user=userDetails).otp_code
            # send activation link to email        
            current_site = get_current_site(request)
            mail_subject = 'Re-activate your WasteCoin account.'
            message = render_to_string('onboarding/activate_email.html', {
                'user': userDetails.firstname,
                'domain': current_site.domain,
                'otp': code_retrieved
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return_data = {
                "error": False,
                "message": "Kind check your email to activate your account. Thanks",
                }
        if userDetails and userValidation == True:
             return_data = {
                "error":True,
                "message": "You have an active account. Kindly login."
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
            # "message": "Something went wrong!"
        }
    return render(request,"onboarding/activate_account.html", return_data)

#SEND ACTIVATION LINK API
@api_view(["POST"])
def send_password_link(request):
    try:
        email = request.data.get("email",None)
        userDetails = User.objects.get(email=email) 
        
        if userDetails:
            # uid = userDetails.user_id
            # send activation link to email        
            current_site = get_current_site(request)
            mail_subject = 'Change your WasteCoin account Password Link.'
            message = render_to_string('onboarding/change_password_email.html', {
                'user': userDetails.firstname,
                'domain': current_site.domain,
                'uid': userDetails.user_id
            })
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            return_data = {
                "error": False,
                "message": "Kind check your email for the password change link. Thanks",
                }
        else:
             return_data = {
                "error":True,
                "message": "User does not exist!"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
            # "message": "Something went wrong!"
        }
    return render(request,"onboarding/forgot_password.html", return_data)

#SIGNIN API
@api_view(["POST"])
def signin_api(request):
    try:
        email = request.data.get("email",None)
        password = request.data.get("password",None)
        field = [email,password]
        if not None in field and not '' in field:
            validate_mail = validator.checkmail(email)
            if validate_mail == True:
                if User.objects.filter(email =email).exists() == False:
                    hub_data = Hub_User.objects.get(email=email, hub_password=password)
                    request.session['user_id'] = hub_data.email
                    if hub_data:
                        return_data = {
                        "error": False,
                        "data": hub_data
                        }
                        return render(request,"user/hub_dashboard.html", return_data)
                    else:
                        return_data = {
                            "error": True,
                            "message": "User does not exist"
                        }
                else:
                    user_data = User.objects.get(email=email)
                    is_valid_password = password_functions.check_password_match(password,user_data.user_password)
                    is_verified = otp.objects.get(user__user_phone=user_data.user_phone).validated
                    #Generate token
                    timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=1440) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "validated": is_verified,
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password and is_verified:
                        request.session['user_id'] = user_data.user_id
                        footprint = user_data.minedCoins*0.03
                        return_data = {
                            "error": False,
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": 
                                {
                                    "firstname": f"{user_data.firstname}",
                                    "lastname": f"{user_data.lastname}",
                                    "email": f"{user_data.email}",
                                    "phonenumber": f"{user_data.user_phone}",
                                    "address": f"{user_data.user_address}",
                                    "carbon_footprint": footprint
                                    # "carbon_footprint": f"{user_data.minedCoins}"
                                }
                        }
                        return render(request,"user/dashboard.html", return_data)
                    elif is_verified == False:
                        return_data = {
                            "error" : True,
                            "message": "Sorry, Your account is not yet activated. Kindly click on the Very Account Link",
                            "token": token.decode('UTF-8')
                        }
                    else:
                        return_data = {
                            "error" : True,
                            "message" : "Wrong Password"
                        }
            else:
                return_data = {
                        "error": True,
                        "message": "Email is Invalid"
                    }                    
        else:
            return_data = {
                "error" : True,
                "message" : "Invalid Parameters"
                }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"onboarding/signin.html", return_data)

@api_view(["GET"])
def hub_dashboard(request):
    try:
        user_id = request.session['user_id']
        if user_id != None and user_id != '':
            #get user info
            hub_data = Hub_User.objects.get(email=user_id)
            # footprint = user_data.minedCoins*0.03
            return_data = {
                "error": False,
                "data": hub_data,
            }
        else:
            return_data = {
                "error": True,
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/hub_dashboard.html", return_data)

@api_view(["GET"])
def dashboard(request):
    try:
        user_id = request.session['user_id']
        if user_id != None and user_id != '':
            #get user info
            user_data = User.objects.get(user_id=user_id)
            footprint = user_data.minedCoins*0.03
            return_data = {
                "error": False,
                "message": "Sucessfull",
                "user_details": 
                    {
                        "firstname": f"{user_data.firstname}",
                        "lastname": f"{user_data.lastname}",
                        "email": f"{user_data.email}",
                        "phonenumber": f"{user_data.user_phone}",
                        "address": f"{user_data.user_address}",
                        "carbon_footprint": footprint
                    }
            }
        else:
            return_data = {
                "error": True,
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/dashboard.html", return_data)

# Profile api
@api_view(["GET"])
def profile(request):
    user_id = request.session['user_id']
    try:
        userID = user_id
        UserInfo = User.objects.get(user_id=userID)
        return_data = {
            "error": False,
            "message": "Successfull",
            "data": {
                "user_details": {
                "first_name": f"{UserInfo.firstname}",
                "last_name": f"{UserInfo.lastname}",
                "email": f"{UserInfo.email}",
                "phone_number": f"{UserInfo.user_phone}",
                "address": f"{UserInfo.user_address}",
                "acc_number": f"{UserInfo.account_number}",
                "acc_name": f"{UserInfo.account_name}",
                "bank": f"{UserInfo.bank_name}",
                "council": f"{UserInfo.user_council_area}",
                "country": f"{UserInfo.user_country}",
                "state": f"{UserInfo.user_state}"
                }
            }
        }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/profile.html", return_data)

# add/update Account details
@api_view(["PUT"])
def update_account(request):
    user_id = request.session['user_id']
    try:
        accountName = request.data.get("account_name",None)
        accountNumber = request.data.get("account_number",None)
        bankName = request.data.get("bank",None)
        field = [accountName,accountNumber,bankName]
        if not None in field and not "" in field:
            user_data = User.objects.get(user_id=user_id)
            user_data.account_number = accountNumber
            user_data.account_name = accountName
            user_data.bank_name = bankName
            user_data.save()
            return_data = {
                "error": False,
                "message": "Account saved Successfully!",
            }
        else:
            return_data = {
                "error": True,
                "message": "One or more fields is Empty!"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return Response(return_data)

# add/update bio-data details
@api_view(["PUT"])
def update_bio(request):
    user_id = request.session['user_id']
    try:
        update_first_name = request.data.get("update_first_name",None)
        update_last_name = request.data.get("update_last_name",None)
        update_email = request.data.get("update_email",None)
        update_phone = request.data.get("update_phone",None)
        update_address = request.data.get("update_address",None)
        update_council = request.data.get("update_council",None)
        update_state = request.data.get("update_state",None)
        update_country = request.data.get("update_country",None)
        field = [update_first_name,update_last_name,update_email,update_phone,update_address,update_council,update_state,update_country]
        if not None in field and not "" in field:
            user_data = User.objects.get(user_id=user_id)
            user_data.firstname = update_first_name
            user_data.lastname = update_last_name
            user_data.user_phone = update_phone
            user_data.email = update_email
            user_data.user_address = update_address
            user_data.user_state = update_state
            user_data.user_council_area = update_council
            user_data.user_country = update_country
            user_data.save()
            return_data = {
                "error": False,
                "message": "Bio-Date  Updated Successfully!",
            }
        else:
            return_data = {
                "error": True,
                "message": "One or more fields is Empty!"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return Response(return_data)

# SIGN UP API
@api_view(["POST"])
def bot_api(request):
    try:
        longitude = request.data.get('longitude',None)
        hub_name = request.data.get('hub_name',None) 
        latitute = request.data.get('latitute',None)
        address = request.data.get('address',None)
        council = request.data.get('council',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)
        bot_field = [hub_name, longitude,latitute,state,country,address]
        if not None in bot_field and not "" in bot_field:
            new_hub_data = HubLocation(hub_name=hub_name,longitude=longitude,latitute=latitute,hub_address=address, hub_state=state, hub_council_area=council, hub_country=country)
            new_hub_data.save()
            return_data = {
                "error": False,
                "message": "Your location data has been successfully taken. Thanks!"
                }
        else:
            return_data = {
                "error":True,
                "message": "Either the Address , State or Country field is empty!"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
            # "message": "Something went wrong!"
        }
    return Response(return_data)

@api_view(["PUT"])
def update_password(request):
    
    try:
        user_id = request.session['user_id']
        old_password = request.data.get("old_password",None)
        new_password = request.data.get("new_password",None)
        field = [old_password,new_password]
        if not None in field and not "" in field:
            user_data = User.objects.get(user_id=user_id)
            is_valid_password = password_functions.check_password_match(old_password,user_data.user_password)
            if is_valid_password == False:
                return_data = {
                    "error": True,
                    "message": "Password is Incorrect"
                }
            else:
                #decrypt password
                encryptpassword = password_functions.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": False,
                    "message": "Password Changed Successfully! "
                }
    except Exception as e:
        return_data = {
                "error": True,
                "message": str(e)
        }
    return Response(return_data)


# Email collector api for landing page
@api_view(["POST"])
def email_collector(request):
    try:
        email = request.data.get("email",None)
        field = [email]
        if not None in field and not "" in field:
            if validator.checkmail(email) == False:
                return_data = {
                    "error": True,
                    "message": "Email is Invalid"
                }
            else:
                #Save new_gig_data
                new_email = EmailCollector(email=email)
                new_email.save()
                
                return_data = {
                    "error": False,
                    "message": "Thank you for your Interest. We shall inform you as soon as the app is launched."
                }
            
        else:
            return_data = {
                "error": True,
                "message": "Please enter your email!"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "message": "Something went wrong!"
        }
    return Response(return_data)

# Email collector api for landing page
@api_view(["POST"])
def brand_collector(request):
    try:
        brand = request.data.get("brand",None)
        brand_code = request.data.get("brand_code",None) 
        category = request.data.get("category",None)
        modal_message = request.data.get("modal_message",None)
        field = [brand, brand_code]
        if not None in field and not "" in field:
            new_brand = BrandCollector(brand=brand, barcode_identification=brand_code, message=modal_message, category=category)
            new_brand.save()
            
            return_data = {
                "error": False,
                "message": "Thank you!. Kindly check back after 24 hours."
            }
            
        else:
            return_data = {
                "error": True,
                "message": "Please enter the item brand name. Thanks!"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "message": str(e)
                # "message": "Something went wrong!"
        }
    return Response(return_data)

# Scanner Page
@api_view(["GET"])
def scanner(request):
    try:
        user_id = request.session['user_id']
        if user_id != None and user_id != '':
            #get user info
            user_data = User.objects.get(user_id=user_id)
            return_data = {
                "error": False,
                "message": "Sucessfull",
                "user_details": 
                    {
                        "firstname": f"{user_data.firstname}",
                        "lastname": f"{user_data.lastname}",
                        "email": f"{user_data.email}",
                        "phonenumber": f"{user_data.user_phone}",
                        "address": f"{user_data.user_address}",
                        "user_id": f"{user_data.user_id}"
                    }
            }
        else:
            return_data = {
                "error": True,
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message": str(e)
        }
    return render(request,"user/scanner.html", return_data)

# # Send coins
# @api_view(["POST"])
# def send_coins(request):
#     try:
#         bar_code = request.data.get("barcode",None)
#         user_id = request.data.get("user_id",None)
#         field = [barcode, user_id]
#         if not None in field and not "" in field:
#             if RecycledItems.objects.filter(item_barcode =bar_code).exists():
#                 return_data = {
#                     "error": True,
#                     "message": "Sorry, this item is already recycled!"
#                 }
#             else:
#                 # barcode_owner_six = bar_code[0:6]
#                 # barcode_manufacturer = barcode.barcode_owner(bar_code)
#                 # barcode_coin = barcode.barcode_coin(bar_code)
#                 barcode_manufacturer = "other"
#                 barcode_coin = 0.1
#                 user_data = User.objects.get(user_id=user_id)
#                 # if barcode_manufacturer:
#                 if bar_code:
#                     # pay user
#                     pay_user = Transaction(user=user_data, amount=barcode_coin,transaction_type="Credit")
#                     pay_user.save()

#                     # credit user wallet
#                     user_balance = user_data.minedCoins + barcode_coin
#                     user_data.minedCoins = user_balance
#                     user_data.save()
#                     #Save new_barcode
#                     new_barcode = RecycledItems(user=user_data, item_manufacturer=barcode_manufacturer, item_barcode=bar_code)
#                     new_barcode.save()
#                     return_data = {
#                         "error": False,
#                         "user": user_data.firstname,
#                         "message": "you just earned "+str(barcode_coin)+"WC" 
#                     }
#                 else:
#                     return_data = {
#                         "error": True,
#                         "message": "Sorry, your recyclable could not be verified. Kindly send the brand name via our contact form, so we can add it and help to earn more. Thanks"
#                     }
            
#         else:
#             return_data = {
#                 "error": True,
#                 "message": "sorry, the barcode was not captured. Please try again!"
#             }
#     except Exception as e:
#         return_data = {
#                 "error": True,
#                 # "message": str(e)
#                 "message":"Something went wrong!"
#         }
#     return Response(return_data)


# Send coins 
# @api_view(["POST"])
# def send_coins_no_filter(request):
#     try:
#         bar_code = request.data.get("barcode",None)
#         user_id = request.data.get("user_id",None)
#         field = [barcode, user_id]
#         if not None in field and not "" in field:
#             barcode_manufacturer = "Unknown"
#             barcode_coin = 0.1
#             user_data = User.objects.get(user_id=user_id)
#             if bar_code:
#                 # pay user
#                 pay_user = Transaction(user=user_data, amount=barcode_coin,transaction_type="Credit")
#                 pay_user.save()

#                 # credit user wallet
#                 user_balance = user_data.minedCoins + barcode_coin
#                 user_data.minedCoins = user_balance
#                 user_data.save()
#                 #Save new_barcode
#                 new_barcode = RecycledItems(user=user_data, item_manufacturer=barcode_manufacturer, item_barcode=bar_code)
#                 new_barcode.save()
#                 return_data = {
#                     "error": False,
#                     "user": user_data.firstname,
#                     "message": "you just earned "+str(barcode_coin)+"WC" 
#                 }
#             else:
#                 return_data = {
#                     "error": True,
#                     "message": "Sorry, your recyclable could not be verified. Kindly send the brand name via our contact form, so we can add it and help to earn more. Thanks"
#                 }
            
#         else:
#             return_data = {
#                 "error": True,
#                 "message": "sorry, the barcode was not captured. Please try again!"
#             }
#     except Exception as e:
#         return_data = {
#                 "error": True,
#                 # "message": str(e)
#                 "message":"Something went wrong!"
#         }
#     return Response(return_data)

@api_view(["POST"])
def send_coins_no_filter(request):
    try:
        bar_code = request.data.get("barcode",None)
        user_id = request.data.get("user_id",None)
        hub_name = request.data.get("hub_name",None)
        hub_address = request.data.get("hub_address",None)
        hub_state = request.data.get("hub_state",None)
        hub_council = request.data.get("hub_council",None)
        hub_country = request.data.get("hub_country",None)
        field = [barcode, user_id]
        if not None in field and not "" in field:
            if Manufacturer.objects.filter(barcode_identification =bar_code).exists():
                # barcode_owner_six = bar_code[0:6]
                barcode_data = Manufacturer.objects.get(barcode_identification =bar_code)
                barcode_manufacturer = barcode_data.manufacturer
                barcode_coin = barcode_data.amount
                # barcode_manufacturer = "other"
                # barcode_coin = 0.1
                user_data = User.objects.get(user_id=user_id)
                # if barcode_manufacturer:
                
                # pay user
                pay_user = Transaction(user=user_data, amount=barcode_coin,transaction_type="Credit")
                pay_user.save()

                # add to total recycled count
                recycledtotal = user_data.totalRecyled+1
                deliveredtotal = user_data.totalDelivered
                # credit user wallet
                user_balance = user_data.minedCoins + barcode_coin
                user_data.minedCoins = user_balance
                user_data.totalRecyled = recycledtotal
                user_data.totalNotDelivered =user_data.totalRecyled - deliveredtotal
                user_data.save()
                #Save new_barcode
                new_barcode = RecycledItems(user=user_data, item_manufacturer=barcode_manufacturer,hub=hub_name, item_barcode=bar_code,hub_address=hub_address,hub_state=hub_state,hub_council_area=hub_council,hub_country=hub_country)
                new_barcode.save()
                if new_barcode:
                    return_data = {
                    "error": False,
                    "showForm": False,
                    "user": user_data.firstname,
                    "manufacturer": barcode_manufacturer,
                    "coins":barcode_coin,
                    "message": "you just earned "+str(barcode_coin)+"WC" 
                }    
            else:
               return_data = {
                        "error": True,
                        "showForm": True,
                        "message": "Sorry, your recyclable could not be verified. Kindly send the brand name via the form below, so we can add it and help to earn more. Thanks"
                    }     
        else:
            return_data = {
                "error": True,
                "showForm": False,
                "message": "sorry, the barcode was not captured. Please try again!"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "showForm": False,
                "message": str(e)
                # "message":"Something went wrong!"
        }
    return Response(return_data)

# Wallet Page
@api_view(["GET"])
def wallet(request):
    try:
        user_id = request.session['user_id']
        if user_id != None and user_id != '':
            #get user info
            user_data = User.objects.get(user_id=user_id)
            user_transaction = Transaction.objects.filter(user=user_data).order_by('-date_added')[:5]
            return_data = {
                "error": False,
                "message": "Sucessfull",
                "user_details": 
                    {
                        "firstname": f"{user_data.firstname}",
                        "lastname": f"{user_data.lastname}",
                        "email": f"{user_data.email}",
                        "phonenumber": f"{user_data.user_phone}",
                        "balance": f"{user_data.minedCoins}",
                        "user_id": f"{user_data.user_id}",
                        "acc_number": f"{user_data.account_number}",
                        "acc_name": f"{user_data.account_name}",
                        "bank": f"{user_data.bank_name}",
                    },
                "transaction": user_transaction
            }
        else:
            return_data = {
                "error": True,
                "message": "Invalid Parameter"
            }
    except Exception as e:
        return_data = {
            "error": True,
            "message":"Something went wrong!"
        }
    return render(request,"user/wallet.html", return_data)

@api_view(["POST"])
def contact_api(request):
    try:
        sender = request.data.get("contact_email",None)
        message = request.data.get("contact_message",None)
        phone = request.data.get("contact_phone",None)
        name = request.data.get("contact_name",None)
        ratings = request.data.get("ratings",None)
        field = [message]
        if not None in field and not "" in field:
            new_message = Notification(sender=name +" - "+phone+" - "+sender, message=message, ratings=ratings)
            new_message.save()
            if new_message:
                return_data = {
                "error": False,
                "showForm": False,
                "message": "Message sent Successfully!" 
            }     
        else:
            return_data = {
                "error": True,
                "showForm": False,
                "message": "sorry, the message field was empty. Please try again!"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "showForm": False,
                "message": str(e)
                # "message":"Something went wrong!"
        }
    return Response(return_data)

# Hub collection confirmation api
@api_view(["POST"])
def hub_confirmation(request):
    try:
        phone_number = request.data.get("phone_number",None)
        field = [phone_number]
        if not None in field and not "" in field:
            user_data = User.objects.get(user_phone=phone_number)
            
            if user_data:
                # unreadMessages = Notification.objects.filter(reciever=user_details.email, beenRead ="No").count()
                delivered = user_data.totalDelivered
                recycled = user_data.totalRecyled
                not_delivered = user_data.totalNotDelivered
                # delivered = RecycledItems.objects.filter(user__user_phone=phone_number,collected=True).count()
                # not_delivered = RecycledItems.objects.filter(user__user_phone=phone_number,collected=False).count()
                return_data = {
                "error": False,
                "showForm": True,
                "user_name": user_data.firstname+" "+ user_data.lastname,
                "delivered": delivered,
                "recycled": recycled,
                "not_delivered": not_delivered,
            }     
        else:
            return_data = {
                "error": True,
                "showForm": False,
                "message": "sorry, the user does not exist!"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "showForm": False,
                "message": str(e)
                # "message":"Something went wrong!"
        }
    return Response(return_data)

# Hub collection confirmation of collected pet pottles from user api
@api_view(["POST"])
def confirmation_api(request):
    try:
        recycled_total = request.data.get("to_deliver",None)
        phone_number = request.data.get("phone_number",None)
        hub_email = request.data.get("hub_email",None)
        field = [phone_number, recycled_total, hub_email]
        if not None in field and not "" in field:
            user_data = User.objects.get(user_phone=phone_number)
            hub_data = Hub_User.objects.get(email=hub_email)
            if user_data:
                delivered = user_data.totalDelivered
                recycled = user_data.totalRecyled
                not_delivered = user_data.totalNotDelivered
                if int(recycled_total) <= not_delivered:
                    user_delievered = delivered + int(recycled_total)
                    
                    user_not_delivered = recycled - user_delievered

                    hub_collection  = hub_data.total_items_collected + int(recycled_total)
                    hub_data.total_items_collected = hub_collection
                    hub_data.save()
                    user_data.totalDelivered = user_delievered
                    user_data.totalNotDelivered = user_not_delivered
                    # user_data.totalNotDelivered =user_data.totalRecyled - deliveredtotal
                    user_data.save()
                    return_data = {
                    "error": False,
                    "showForm": True,
                    # "not_collected": not_collected,
                    "message": str(recycled_total)+" pieces recycled successfully!" 
                    } 
                else:

                    return_data = {
                    "error": True,
                    "showForm": False,
                    # "not_collected": not_collected,
                    "message": "Sorry! you entered exceeded value" 
                    }     
        else:
            return_data = {
                "error": True,
                "showForm": False,
                "message": "sorry, one or more data field is empty"
            }
    except Exception as e:
        return_data = {
                "error": True,
                "showForm": False,
                "message": str(e)
                # "message":"Something went wrong!"
        }
    return Response(return_data)