import io
import numpy as np
import os

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as tf_image

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import BirdImageUploadForm
from .models import BirdsFound, UsersBirdCollection

model_path = os.path.join(settings.BASE_DIR, 'birdquest', 'models', 'bird_model.h5')
model = load_model(model_path)

class_names_path = os.path.join(settings.BASE_DIR, 'birdquest', 'models', 'birds.txt')

def dashboard(request):
    #View for signed in Users

    form = BirdImageUploadForm()  

    leaderboard_data = UsersBirdCollection.objects.select_related('user').order_by('-total_birds_found')

    if request.method == 'POST':
        form = BirdImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            predictions = predict_top_20(img)
            return JsonResponse(predictions)

    return render(request, 'dashboard.html', {'form': form, 'leaderboard_data': leaderboard_data})
@login_required
def submit_bird(request):
    if request.method == 'POST':
        bird_name = request.POST.get('bird_name')
        uploaded_image = request.FILES.get('image')

        bird, created = BirdsFound.objects.get_or_create(
            user=request.user,
            bird_name=bird_name,
            defaults={'uploaded_image': uploaded_image}
        )

        if not created:
            bird.found_count += 1
            bird.save()

        user_collection, collection_created = UsersBirdCollection.objects.get_or_create(user=request.user)

        user_collection.total_birds_found += 1
        user_collection.save()

        return JsonResponse({'status': 'success', 'bird_name': bird_name, 'found_count': bird.found_count})
    
    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

@login_required
def bird_collection(request):
    birds = BirdsFound.objects.filter(user=request.user)
    return render(request, 'collection.html', {'birds': birds})
@login_required
def leaderboard(request):
    leaderboard_data = UsersBirdCollection.objects.select_related('user').order_by('-total_birds_found')

    return render(request, 'dashboard.html', {'leaderboard_data': leaderboard_data})

def home(request):
    """View for non-signed-in users."""
    form = BirdImageUploadForm() 

    if request.method == 'POST':
        form = BirdImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            predictions = predict_top_20(img)
            return JsonResponse(predictions)

    if request.user.is_authenticated:
        return redirect('dashboard')  
    return render(request, 'home.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def get_class_names():
    with open(class_names_path, 'r') as f:
        class_names = f.read().splitlines()
    return class_names

def preprocess_image(img, target_size=(224, 224)):
    img_io = io.BytesIO(img.read())
    img = tf_image.load_img(img_io, target_size=target_size)
    img_array = tf_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    return img_array

def predict_top_20(img_path):
    class_names = get_class_names()
    img_array = preprocess_image(img_path)

    predictions = model.predict(img_array)

    top_20_indices = np.argsort(predictions[0])[-20:][::-1]
    top_20_predictions = {class_names[i]: float(predictions[0][i]) for i in top_20_indices}

    return top_20_predictions



