from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect

from .forms import ContactForm

def home_page(request):
    print(request.session.get("first_name","Unknown"))
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",

    }
    if request.user.is_authenticated:
        context["premium_content"] = "YEAHHHHHH"
    return render(request, "home_page.html", context)


def example_nav(request):
    context = {
      
    }
    return render(request, "navexample.html", context)


def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "home_page.html", context)


def react_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "react.html", context)


def context_demo(request):
    context = {
        "title":"Context Demo Page",
        "content":" Welcome to the context demo page."
    }
    return render(request,"context_example.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":" Welcome to the contact page.",
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission!"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400,content_type='application/json')

    return render(request, "contact/view.html", context)

