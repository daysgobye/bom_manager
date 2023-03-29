from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

class HomePageView(TemplateView):
    template_name = "pages/home.html"


# class LibraryPageView(TemplateView):
#     template_name = "pages/library.html"
def find(request):

    message=""
    template_name = "pages/library/findcheckout.html"
    user=request.user
    lists=[
        {
        "title":"Your Mats",
        "list":user.part_libary_lookup.all()
        }
    ]
    if request.method == 'DELETE':
        user.delete_lookup()
        return HttpResponse("")

    context = {'message':message,
                'user_lists':lists,
                "part_list":lists[0]}
    return render(request, template_name, context)

def libraryPageView(request):
    message=""
    template_name = "pages/library/library.html"
    user=request.user
    lists=[
        {
        "title":"Your Mats",
        "list":user.part_libary.all()
        }
    ]
    locations_needed=user.check_if_locations_are_needed()
    if locations_needed:
        message="you need to add locations to your resent import"
    context = {'message':message,
                'user_lists':lists}
    return render(request, template_name, context)

def checkout(request):
    message=""
    template_name = "pages/library/checkout.html"
    user=request.user
    lists=[
        {
        "title":"Last Look-up",
        "list":user.part_libary_lookup.all()
        },
        {
        "title":"Your Mats",
        "list":user.part_libary.all()
        },
     
    ]
    
    if request.method == 'POST':
        csv_file = request.FILES.get('csv',False)
        lookup_value = request.POST.get('value',False)
        lookup_package = request.POST.get('package',False)
        lookup_part_number= request.POST.get('part_number',False)
        checkout= request.POST.get('method',False)
        if csv_file:
            if csv_file.name.endswith('.csv'):
                file_data = csv_file.read().decode("utf-8")	
                user.lookup_csv(file_data)
            else:
                message="need to upload .csv file"
        elif lookup_package or lookup_value or lookup_part_number:
            lookup_qty= request.POST.get('qty',False)
            if lookup_qty:
                user.lookup_single_part(lookup_value,lookup_package,lookup_part_number,lookup_qty)
            else:
                message= "qty is missing"
        elif checkout:
            user.checkout_lookup()
            return HttpResponseRedirect('checkout/find/')


        else:
           message="need to upload a file full of parts you want to check out"

    context = {'message':message,
                'user_lists':lists,
                "part_list":lists[0]}
    return render(request, template_name, context)


def add(request):
    message=""
    template_name = "pages/library/add.html"
    user=request.user
    lists=[
          {
        "title":"Incoming parts",
        "list":user.incoming_part_libary.all()
        },
        {
        "title":"Your Mats",
        "list":user.part_libary.all()
        }
      
    ]
    
    if request.method == 'POST':
        csv_file = request.FILES.get('csv',False)
        if csv_file:
            if csv_file.name.endswith('.csv'):
                file_data = csv_file.read().decode("utf-8")	
                user.add_csv(file_data)
            else:
                message="need to upload .csv file"
        else:
            new_location = request.POST.get('location',False)
            part_id = request.POST.get('id',False)
            if new_location and new_location!=""and part_id:
                message=user.add_location_to_incoming_part(int(part_id),new_location)
            else:
                message="location is empty"
    context = {'message':message,
                'user_lists':lists}
    return render(request, template_name, context)
