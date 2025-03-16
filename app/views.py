from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionForm
from app.machinelearning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition
import os

# Create your views here.

def home(request):
    form = FaceRecognitionForm()
    if request.method == 'POST':
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)

            # Extract the image object from database
            primary_key = save.pk
            imgobj = FaceRecognition.objects.get(id=primary_key)
            print("Image Object ===========", imgobj)
            fileroot = str(imgobj.image)
            print("File Root ===========", fileroot)
            filepath = os.path.join(settings.MEDIA_ROOT, fileroot)
            print("File Path ===========", filepath)
            results = pipeline_model(filepath)
            print("Results ===========", results)
            return render(request, 'index.html', {'form': form, 'upload': True, 'results': results, 'imgpath': fileroot})



    return render(request, 'index.html', {'form': form, 'upload': False})
