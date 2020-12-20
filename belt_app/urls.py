from django.urls import path     
from . import views


urlpatterns = [
    path('', views.display_login_reg),
    path('add_user', views.add_user),
    path('login', views.login),
    path('logout', views.logout),
    path('display_quotes', views.display_quotes),
    path('add_Quote', views.add_Quote),
    path('quotes/<int:user_id>', views.display_userPage),
    path('add_toLikes/<int:quote_id>', views.add_toLikes),
    path('delete/<int:user_id>/<int:quote_id>', views.delete_quote),
    path('edit_account/<int:user_id>', views.edit_account),
    path('display_edit/<int:user_id>', views.display_edit)

]

