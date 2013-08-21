from django.shortcuts import render
from imdbaccount.forms import IMDBAccountForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

def form(request):
    if request.method == 'POST': # If the form has been submitted...
        form = IMDBAccountForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = IMDBAccountForm() # An unbound form

    return render(request, 'form.html', {
        'form': form,
    })        