from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    # ONBOARDING
    path('', views.splash, name='splash'),
    # location bot
    path('location_bot', views.location_bot, name='location_bot'),
    path('bot_api', views.bot_api, name='bot_api'),
    # email collector api
    path('email_collector', views.email_collector, name='email_collector'),
    path('brand_collector', views.brand_collector, name='brand_collector'),

    path('signin', views.signin, name='signin'),
    path('signup', views.splash, name='signup'),
    path('signup_two', views.signup, name='signup_two'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('activate_account', views.activate_account, name='activate_account'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('send_password_link', views.send_password_link, name='send_password_link'),
    path('faq', views.faq, name='faq'),
    path('signout', views.signout, name='signout'),
    path('home', views.dashboard, name='home'),
    path('hub_home', views.hub_dashboard, name='hub_home'),
    path('wallet', views.wallet, name='wallet'),
    path('profile', views.profile, name='profile'),
    path('notification', views.notification, name='notification'),
    path('scanner', views.scanner, name='scanner'),
    path('activate/<otp_code>', views.activate, name='activate'),
    path('change_password/<uid>', views.change_password, name='change_password'),

    # path('test', views.test, name='test'),

    # APIS
    path('signup_api', views.signup_api, name='signup_api'),
    path('hub_confirmation', views.hub_confirmation, name='hub_confirmation'),
    path('confirmation_api', views.confirmation_api, name='confirmation_api'),
    path('signin_api', views.signin_api, name='signin_api'),
    path('update_account', views.update_account, name='update_account'),
    path('contact_api', views.contact_api, name='contact_api'),
    path('update_password', views.update_password, name='update_password'),
    path('update_bio', views.update_bio, name='update_bio'),
    path('send_activation_link_api', views.send_activation_link_api, name='send_activation_link_api'),
    path('change_password_api', views.change_password_api, name='change_password_api'),
    
    # path('send_coins', views.send_coins, name='send_coins'),              # send coins with filter for existing recycled items
    path('send_coins', views.send_coins_no_filter, name='send_coins'),          # send coins with no filter
    

]

