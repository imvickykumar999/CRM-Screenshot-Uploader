import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def upload_screenshot(request):
    """Handle screenshot upload."""
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        
        # Ensure the screenshots folder exists
        screenshots_folder = os.path.join(settings.MEDIA_ROOT, 'screenshots')
        os.makedirs(screenshots_folder, exist_ok=True)
        
        # Save the uploaded file
        file_path = os.path.join(screenshots_folder, file.name)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        return JsonResponse({"message": "File uploaded successfully", "url": f"{settings.MEDIA_URL}screenshots/{file.name}"})
    
    return JsonResponse({"message": "Invalid request"}, status=400)

def list_screenshots(request):
    """Fetch and display uploaded screenshots."""
    screenshots_folder = os.path.join(settings.MEDIA_ROOT, 'screenshots')
    screenshots = []

    if os.path.exists(screenshots_folder):
        for filename in os.listdir(screenshots_folder):
            if filename.endswith(('jpg', 'jpeg', 'png', 'gif')):
                screenshots.append({
                    'filename': filename,
                    'url': f"{settings.MEDIA_URL}screenshots/{filename}"
                })
    screenshots.reverse()

    return JsonResponse(screenshots, safe=False)

def render_screenshots_page(request):
    """Render the HTML page for displaying screenshots."""
    return render(request, 'screenshots.html')
