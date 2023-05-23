from django.urls import path
from . import views

urlpatterns = [
    path('admin/inbox', views.inbox, name='inbox'),
    path('admin/compose', views.compose, name='compose'),
    path('guest/inbox', views.inboxGuest, name='guest_inbox'),
    path('guest/compose', views.composeGuest, name='guest_compose'),
    path('register', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('admin/users_list', views.admin, name='users_list'),
    path('admin/delete_users/<int:id>', views.deleteUsers, name='delete'),
    path('admin/update_user/<int:id>', views.updateUsers, name='update_users'),
    path('admin/delete_room/<int:id>', views.deleteRoom, name='delete_room'),
    path('delete_reserve/<int:id>', views.deleteReserve, name='delete_reserve'),
    # path('admin/change_status', views.changeStatus, name='change_status'),
    path('admin/room_list', views.room, name='room_list'),
    path('admin/reservation', views.reservation, name='reservation'),
    path('admin/update_room/<int:id>', views.updateRoom, name='update_room'),
    path('rooms/<int:id>/', views.guestBookRoom, name='book_room'),
    path('book_room', views.bookRoom, name='bookroom'),
    path('home', views.home, name='home'),
    path('logout', views.login_out, name='logout'),
    path('notify', views.notify, name='notify'),
    path('rooms', views.rooms, name='rooms'),
    path('guest/update_reservation/<int:id>', views.updateReserve, name='update_reserve'),
    # path('detail/<int:message_id>/', views.message_detail, name='message_detail'),
]
