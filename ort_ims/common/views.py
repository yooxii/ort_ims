from django import forms
from django.db import models
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

################# Common Functions #################


def render_edit_form(  # noqa: PLR0913
    request: HttpRequest,
    model_class: models.Model,
    form_class: forms.ModelForm,
    object_id: int,
    template_name: str,
    redirect_view_name: str,
    title_text: str,
):
    """编辑函数模板

    Args:
        request (request): 网络请求
        model_class (model_class): 模型类
        form_class (form_class): 表单类
        object_id (int): 要编辑的对象ID
        template_name (str): 渲染的html模板名
        redirect_view_name (str): 重定向的视图名
        title_text (str): 网页标题

    Returns:
        (HttpResponse|redirect): 渲染的html或重定向
    """
    if request.method == "GET":
        obj = get_object_or_404(model_class, id=object_id)
        form = form_class(instance=obj)
        return render(request, template_name, {"title": title_text, "form": form})

    obj = get_object_or_404(model_class, id=object_id)
    form = form_class(request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(redirect_view_name)
    return render(request, template_name, {"title": title_text, "form": form})


def render_add_form(request, form_class, template_name, redirect_view_name, title_text):
    """添加函数模板

    Args:
        request (request): 网络请求
        form_class (form_class): 表单类
        template_name (str): 渲染的html模板名
        redirect_view_name (str): 重定向的视图名
        title_text (str): 网页标题

    Returns:
        (HttpResponse|redirect): 渲染的html或重定向
    """

    if request.method == "GET":
        form = form_class()
        return render(request, template_name, {"title": title_text, "form": form})

    form = form_class(request.POST)
    if form.is_valid():
        form.save()
        return redirect(redirect_view_name)
    return render(request, template_name, {"title": title_text, "form": form})


def handle_delete(request, model_class, object_id, redirect_view_name):
    obj = get_object_or_404(model_class, id=object_id)
    obj.delete()
    return redirect(redirect_view_name)
