from django.conf.urls import *

from .views import *

urlpatterns = [
    url(r'^all/$', all_forms, name="all-forms"),
    url(r'^edit/(?P<uuid>[-\w\d]+)/$', edit_form, name="edit-form"),
    url(r'^options/$', form_options, name="form-options"),
    url(r'^edit/config/(?P<uuid>[-\w\d]+)/$', edit_config, name="edit-config"),
    url(r'^edit/tips/(?P<uuid>[-\w\d]+)/$', edit_tips, name="edit-tips"),
    url(r'^responses/(?P<uuid>[-\w\d]+)/$', form_responses, name="form-responses"),
    url(r'^response/(?P<uuid>[-\w\d]+)/edit/$', edit_response, name="edit-response"),
    

    # AJAX URLS
    url(r'^ajax-edit-form/$', ajax_edit_form, name="ajax-edit-form"),
    url(r'^ajax-save-form/$', ajax_save_form, name="ajax-save-form"),
    url(r'^ajax-add-cat/$', ajax_add_cat, name="ajax-add-cat"),
    url(r'^ajax-update-values/$', ajax_update_val, name="ajax-update-val"),
    url(r'^ajax-load-values/$', ajax_load_val, name="ajax-load-val"),

    # AJAX REGISTER FORM URLS
    url(r'^ajax-save-rform/$', ajax_save_rform, name="ajax-save-rform"),
]
