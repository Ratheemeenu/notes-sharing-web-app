# notes/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DocumentForm
from .models import Document

@login_required
def home(request):
    # Retrieve documents belonging to the current user
    documents = Document.objects.filter(user=request.user)
    return render(request, 'notes/home.html', {'documents': documents})

@login_required
def upload(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Document object but do not save it to the database yet
            document = form.save(commit=False)
            # Assign the current user to the document's user field
            document.user = request.user
            # Save the document to the database
            document.save()
            # Redirect to the home page after successful upload
            return redirect('home')
    else:
        # If the request method is GET, create a new empty form
        form = DocumentForm()
    return render(request, 'notes/upload.html', {'form': form})

