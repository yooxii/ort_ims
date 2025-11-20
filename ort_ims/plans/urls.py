from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name = "plans"
urlpatterns = [
    path("", views.index, name="index"),
    ################# Checkouts #################
    path("checkouts", views.CheckoutsView.as_view(), name="checkouts"),
    path("import_checkouts", views.import_checkouts, name="import_checkouts"),
    path("export_checkouts", views.export_checkouts, name="export_checkouts"),
    path("add_checkouts", views.add_checkouts, name="add_checkouts"),
    path("<int:pk>/edit_checkouts", views.edit_checkouts, name="edit_checkouts"),
    path(
        "<int:pk>/delete_checkouts",
        views.delete_checkouts,
        name="delete_checkouts",
    ),
    ################# Schedules #################
    # path("schedules", views.schedules, name="schedules"),
    path("schedules", views.SchedulesView.as_view(), name="schedules"),
    path("import_schedules", views.import_schedules, name="import_schedules"),
    path("export_schedules", views.export_schedules, name="export_schedules"),
    path("<int:pk>/add_schedules", views.add_schedules, name="add_schedules"),
    path(
        "<int:pk>/edit_schedules",
        views.EditSchedulesView.as_view(),
        name="edit_schedules",
    ),
    # path(
    #     "<int:schedule_id>/edit_schedules", views.edit_schedules, name="edit_schedules"
    # ),
    path("<int:pk>/delete_schedules", views.delete_schedules, name="delete_schedules"),
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
        "<int:testitem_id>/edit_testitems", views.edit_testitems, name="edit_testitems"
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
        "<int:customer_id>/edit_customers", views.edit_customers, name="edit_customers"
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
