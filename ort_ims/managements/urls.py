from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from . import views

app_name = "managements"
urlpatterns = [
    ################# Technicians #################
    path("technicians", views.technicians, name="technicians"),
    path(
        "<int:technician_id>/edit_technicians",
        views.edit_technicians,
        name="edit_technicians",
    ),
    path("add_technicians", views.add_technicians, name="add_technicians"),
    path(
        "<int:technician_id>/delete_technicians",
        views.delete_technicians,
        name="delete_technicians",
    ),
    ################# TestItems #################
    path("testitems", views.testitems, name="testitems"),
    path(
        "<int:testitem_id>/edit_testitems",
        views.edit_testitems,
        name="edit_testitems",
    ),
    path("add_testitems", views.add_testitems, name="add_testitems"),
    path(
        "<int:testitem_id>/delete_testitems",
        views.delete_testitems,
        name="delete_testitems",
    ),
    ################# CustProducts #################
    path("custproducts", views.custproducts, name="custproducts"),
    path(
        "<int:customer_id>/edit_customers",
        views.edit_customers,
        name="edit_customers",
    ),
    path("<int:product_id>/edit_products", views.edit_products, name="edit_products"),
    path("add_customers", views.add_customers, name="add_customers"),
    path("add_products", views.add_products, name="add_products"),
    path(
        "<int:customer_id>/delete_customers",
        views.delete_customers,
        name="delete_customers",
    ),
    path(
        "<int:product_id>/delete_products",
        views.delete_products,
        name="delete_products",
    ),
]
urlpatterns += staticfiles_urlpatterns()
