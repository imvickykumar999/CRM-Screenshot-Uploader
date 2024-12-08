
## Port 80 forwarded using ngrok

python -m http.server 80
ipconfig
    http://192.168.0.105/

https://dashboard.ngrok.com/get-started/setup/windows
    ngrok config add-authtoken 2izwMIwxxxxxxxxxxxxxxxxxxxxxPgbqGi5h

ngrok http --url=free-camel-deadly.ngrok-free.app 80
    https://free-camel-deadly.ngrok-free.app/

---

### Steps to Use ngrok with Django:

1. **Run Your Django App**
   First, make sure your Django app is running on a specific port (e.g., `8000`).
   - If you haven't already started the Django development server, run it with this command:
   
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

   The `0.0.0.0` part allows the server to accept connections from any network interface (not just `localhost`), which is necessary for ngrok to work.

   Your Django app should now be accessible at `http://127.0.0.1:8000/` locally.

---

2. **Start ngrok to Forward to Django**
   In a separate terminal window, run ngrok to expose the local port `8000` (or whichever port your Django app is running on):

   ```bash
   ngrok http 8000
   ```

   After running this command, ngrok will generate a public URL like:
   ```
   http://abc123.ngrok.io
   ```

   This URL will tunnel requests to your local Django application.

---

3. **Access Your Django App via ngrok**
   You can now open the public URL (`http://abc123.ngrok.io`) in a browser to access your Django app globally.

---

### Example Django Application (Optional)
If you don't have a Django app yet, here's a basic setup:

1. **Create a Django Project:**
   ```bash
   django-admin startproject myproject
   cd myproject
   ```

2. **Create a Django App:**
   ```bash
   python manage.py startapp myapp
   ```

3. **Set up the URL in `myproject/urls.py`:**
   Add the following line to route requests to your app:
   ```python
   from django.contrib import admin
   from django.urls import path
   from myapp import views

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', views.index),
   ]
   ```

4. **Create a simple view in `myapp/views.py`:**
   ```python
   from django.http import HttpResponse

   def index(request):
       return HttpResponse("Hello, World!")
   ```

5. **Run the Django Server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

6. **Run ngrok:**
   In a new terminal window, run:
   ```bash
   ngrok http 8000
   ```

7. **Access the Django App:**
   Visit the ngrok URL (e.g., `http://abc123.ngrok.io`) to see your Django application running.

---

### Additional Notes:
- **Security Consideration**: While ngrok is great for development and testing, avoid using it for production applications without proper security, as the public URL can be accessed by anyone.
- **Accessing from Mobile**: Once ngrok is running, you can use the public URL from mobile devices or share it with others.

---

Let me know if you need further assistance with the Django app or ngrok setup!
