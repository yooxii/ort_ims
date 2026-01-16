from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

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
]
urlpatterns += staticfiles_urlpatterns()
