# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# # from .models import Profile   # if you added profile
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required



# import joblib
# import os
# from django.conf import settings

# model_path = os.path.join(settings.BASE_DIR, 'core/ml_model/crop_model.pkl')
# model = joblib.load(model_path)

# def home(request):
#     if request.user.is_authenticated:

#         profile, _ = Profile.objects.get_or_create(user=request.user)

#         history = CropRecommendation.objects.filter(user=request.user).order_by('-created_at')

#         total = history.count()
#         last = history.first()

#         return render(request, 'core/index.html', {
#             'profile': profile,
#             'total': total,
#             'last': last,
#             'history': history[:3]
#         })

#     return render(request, 'core/index.html')
# # LOGIN
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from django.shortcuts import render, redirect

# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get('username')   # user enters email
#         password = request.POST.get('password')

#         try:
#             user_obj = User.objects.get(email=email)
#             username = user_obj.username
#         except User.DoesNotExist:
#             username = None

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             messages.error(request, "Invalid credentials")

#     return render(request, 'core/login.html')
# # SIGNUP
# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect

# from django.contrib.auth.models import User
# from django.contrib import messages
# from .models import Profile
# from django.shortcuts import render, redirect

# def signup(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         fullname = request.POST.get('fullname')
#         phone = request.POST.get('phone')
#         role = request.POST.get('role')
#         location = request.POST.get('location')

#         # prevent duplicate username
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists")
#             return render(request, 'core/signup.html')

#         # create user
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         # create profile
#         Profile.objects.create(
#             user=user,
#             full_name=fullname,
#             phone=phone,
#             role=role,
#             location=location
#         )

#         return redirect('login')

#     return render(request, 'core/signup.html')


# # # LOGOUT
# # def logout_view(request):
# #     logout(request)
# #     return redirect('login')

# # def home(request):
# #     if request.user.is_authenticated:
# #         profile = request.user.profile
# #         return render(request, 'core/index.html', {'profile': profile})
# #     return render(request, 'core/index.html')



# from .models import CropRecommendation
# from django.contrib.auth.decorators import login_required

# @login_required
# def crop_page(request):
#     crop_result = None

#     if request.method == "POST":
#         n = float(request.POST.get("n"))
#         p = float(request.POST.get("p"))
#         k = float(request.POST.get("k"))
#         temp = float(request.POST.get("temp"))
#         humidity = float(request.POST.get("humidity"))
#         ph = float(request.POST.get("ph"))
#         rain = float(request.POST.get("rain"))

#         features = [[n, p, k, temp, humidity, ph, rain]]
#         crop_result = model.predict(features)[0]

#         # SAVE TO DB
#         CropRecommendation.objects.create(
#             user=request.user,
#             nitrogen=n,
#             phosphorus=p,
#             potassium=k,
#             temperature=temp,
#             humidity=humidity,
#             ph=ph,
#             rainfall=rain,
#             crop_result=crop_result
#         )

#     # FETCH HISTORY
#     history = CropRecommendation.objects.filter(user=request.user).order_by('-created_at')
#     from collections import Counter

#     history = CropRecommendation.objects.filter(user=request.user)

#     # count crops
#     crop_list = [h.crop_result for h in history]
#     crop_counts = Counter(crop_list)

#     labels = list(crop_counts.keys())
#     values = list(crop_counts.values())

#     return render(request, 'core/crop.html', {
#         'crop_result': crop_result,
#         'history': history,
#         'labels': labels,
#         'values': values
#     })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, CropRecommendation
from .models import FertilizerHistory
from .models import YieldHistory

import joblib
import os
from django.conf import settings
from django.http import JsonResponse
from django.conf import settings

import joblib
import pandas as pd

# LOAD ML MODEL
model_path = os.path.join(settings.BASE_DIR, 'core/ml_model/crop_model.pkl')
model = joblib.load(model_path)


# ================= HOME =================
def home(request):
    return render(request, 'core/index.html')


# ================= LOGIN =================
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # role based redirect
            if user.profile.role == "admin":
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')

        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'core/login.html')




def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        fullname = request.POST.get('fullname', '').strip()
        phone = request.POST.get('phone', '').strip()
        location = request.POST.get('location', '').strip()

        role = "farmer"

        if not username or not email or not password:
            messages.error(request, "All required fields must be filled")
            return render(request, 'core/signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'core/signup.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters")
            return render(request, 'core/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'core/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'core/signup.html')

        names = fullname.split()
        first_name = names[0] if names else ""
        last_name = " ".join(names[1:]) if len(names) > 1 else ""

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        profile, created = Profile.objects.get_or_create(user=user)

        profile.full_name = fullname
        profile.phone = phone
        profile.role = "farmer"
        profile.location = location
        profile.save()

        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'core/signup.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, SoilTestRequest, FertilizerHistory, YieldHistory


@login_required
def admin_dashboard(request):

    if request.user.profile.role != "admin":
        return redirect("dashboard")

    total_users = User.objects.count()
    farmers = Profile.objects.filter(role="farmer").count()
    admins = Profile.objects.filter(role="admin").count()
    pending_soil = SoilTestRequest.objects.filter(status="Pending").count()

    fertilizer_count = FertilizerHistory.objects.count()
    yield_count = YieldHistory.objects.count()

    context = {
        "total_users": total_users,
        "farmers": farmers,
        "admins": admins,
        "pending_soil": pending_soil,
        "fertilizer_count": fertilizer_count,
        "yield_count": yield_count,
    }

    return render(request, "core/admin-dashboard.html", context)






# ================= DASHBOARD =================
@login_required
def dashboard(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    history = CropRecommendation.objects.filter(user=request.user).order_by('-created_at')
    

    return render(request, 'core/features.html', {
    'profile': profile
})
    # return render(request, 'core/dashboard.html', {
    #     'profile': profile,
    #     'history': history[:3]
    # })


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('home')


# ================= CROP PAGE =================
@login_required
def crop_page(request):
    crop_result = None

    if request.method == "POST":
        n = float(request.POST.get("n"))
        p = float(request.POST.get("p"))
        k = float(request.POST.get("k"))
        temp = float(request.POST.get("temp"))
        humidity = float(request.POST.get("humidity"))
        ph = float(request.POST.get("ph"))
        rain = float(request.POST.get("rain"))

        features = [[n, p, k, temp, humidity, ph, rain]]
        crop_result = model.predict(features)[0]

        CropRecommendation.objects.create(
            user=request.user,
            nitrogen=n,
            phosphorus=p,
            potassium=k,
            temperature=temp,
            humidity=humidity,
            ph=ph,
            rainfall=rain,
            crop_result=crop_result
        )

    history = CropRecommendation.objects.filter(user=request.user)

    from collections import Counter
    crop_list = [h.crop_result for h in history]
    crop_counts = Counter(crop_list)

    labels = list(crop_counts.keys())
    values = list(crop_counts.values())

    return render(request, 'core/crop.html', {
        'crop_result': crop_result,
        'history': history,
        'labels': labels,
        'values': values
    })


from .models import SoilTestRequest
from django.shortcuts import render, redirect
from .models import SoilTestRequest
from django.contrib.auth.decorators import login_required


@login_required
def soil_test(request):

    success = False

    if request.method == "POST":

        SoilTestRequest.objects.create(
            user=request.user,
            lab_name=request.POST.get("lab_name"),
            soil_type=request.POST.get("soil_type"),
            appointment_date=request.POST.get("appointment_date"),
            notes=request.POST.get("notes")
        )

        success = True

    history = SoilTestRequest.objects.filter(
        user=request.user
    ).order_by("-id")

    return render(request, "core/soil-test.html", {
        "success": success,
        "history": history
    })

def weather(request):
    return render(request, 'core/weather.html')


def fertilizer(request):

    result = None

    if request.method == "POST":

        temperature = float(request.POST.get("temperature"))
        humidity = float(request.POST.get("humidity"))
        moisture = float(request.POST.get("moisture"))

        soil = request.POST.get("soil")
        crop = request.POST.get("crop")

        nitrogen = float(request.POST.get("nitrogen"))
        phosphorous = float(request.POST.get("phosphorous"))
        potassium = float(request.POST.get("potassium"))

        sample = pd.DataFrame([{
        "Temperature": temperature,
        "Humidity": humidity,
        "Moisture": moisture,
        "Soil_Type": soil,
        "Crop_Type": crop,
        "Nitrogen": nitrogen,
        "Potassium": potassium,
        "Phosphorus": phosphorous
    }])

        model_path = os.path.join(
            settings.BASE_DIR,
            "core",
            "ml_model",
            "fertilizer_model.pkl"
        )

        model = joblib.load(model_path)

        result = model.predict(sample)[0]

        if request.user.is_authenticated:
            FertilizerHistory.objects.create(
                user=request.user,
                temperature=temperature,
                humidity=humidity,
                moisture=moisture,
                soil_type=soil,
                crop_type=crop,
                nitrogen=nitrogen,
                phosphorous=phosphorous,
                potassium=potassium,
                prediction=result
            )

    history = []

    if request.user.is_authenticated:
        history = FertilizerHistory.objects.filter(
            user=request.user
        ).order_by('-created_at')[:10]

    return render(request, "core/fertilizer.html", {
        "result": result,
        "history": history
    })

def yield_prediction(request):

    result = None
    history = []
    error = None

    if request.user.is_authenticated:
        history = YieldHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")[:10]

    if request.method == "POST":
        try:
            crop = request.POST.get("crop")
            crop_year = int(request.POST.get("crop_year"))
            season = request.POST.get("season")
            state = request.POST.get("state")

            area = float(request.POST.get("area"))
            annual_rainfall = float(request.POST.get("annual_rainfall"))
            fertilizer = float(request.POST.get("fertilizer"))
            pesticide = float(request.POST.get("pesticide"))

            sample = pd.DataFrame([{
                "crop": crop,
                "crop_year": crop_year,
                "season": season,
                "state": state,
                "area": area,
                "annual_rainfall": annual_rainfall,
                "fertilizer": fertilizer,
                "pesticide": pesticide
            }])

            model_path = os.path.join(
                settings.BASE_DIR,
                "core",
                "ml_model",
                "yield_model.pkl"
            )

            model = joblib.load(model_path)

            prediction = model.predict(sample)[0]
            result = round(float(prediction), 2)

            if request.user.is_authenticated:
                YieldHistory.objects.create(
                    user=request.user,
                    crop=crop,
                    crop_year=crop_year,
                    season=season,
                    state=state,
                    area=area,
                    annual_rainfall=annual_rainfall,
                    fertilizer=fertilizer,
                    pesticide=pesticide,
                    prediction=result
                )

                history = YieldHistory.objects.filter(
                    user=request.user
                ).order_by("-created_at")[:10]

        except Exception as e:
            error = str(e)

    return render(request, "core/yield.html", {
        "result": result,
        "history": history,
        "error": error
    })
























from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


@login_required
def admin_users(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    users = User.objects.all().select_related("profile").order_by("-id")

    return render(request, "core/admin_users.html", {
        "users": users
    })


@login_required
def delete_user(request, user_id):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    user = get_object_or_404(User, id=user_id)

    # prevent deleting self
    if user == request.user:
        messages.error(request, "You cannot delete yourself.")
        return redirect("admin_users")

    # prevent deleting admins
    if hasattr(user, "profile") and user.profile.role == "admin":
        messages.error(request, "Cannot delete admin user.")
        return redirect("admin_users")

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("admin_users")




from .models import SoilTestRequest
from django.contrib.auth.decorators import login_required


@login_required
def admin_soil_requests(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    requests = SoilTestRequest.objects.all().select_related("user").order_by("-id")

    return render(request, "core/admin_soil_requests.html", {
        "requests": requests
    })


@login_required
def update_soil_status(request, req_id, status):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    obj = get_object_or_404(SoilTestRequest, id=req_id)

    allowed = ["Pending", "Approved", "Rejected", "Completed"]

    if status in allowed:
        obj.status = status
        obj.save()

    return redirect("admin_soil_requests")


from django.contrib.auth.models import User
from .models import Profile, SoilTestRequest, YieldHistory
from django.contrib.auth.decorators import login_required


@login_required
def admin_reports(request):
    if request.user.profile.role != "admin":
        return redirect("dashboard")

    total_users = User.objects.count()
    farmers = Profile.objects.filter(role="farmer").count()
    admins = Profile.objects.filter(role="admin").count()

    total_soil = SoilTestRequest.objects.count()
    pending = SoilTestRequest.objects.filter(status="Pending").count()
    approved = SoilTestRequest.objects.filter(status="Approved").count()
    completed = SoilTestRequest.objects.filter(status="Completed").count()
    rejected = SoilTestRequest.objects.filter(status="Rejected").count()

    yield_count = YieldHistory.objects.count()

    context = {
        "total_users": total_users,
        "farmers": farmers,
        "admins": admins,
        "total_soil": total_soil,
        "pending": pending,
        "approved": approved,
        "completed": completed,
        "rejected": rejected,
        "yield_count": yield_count,
    }

    return render(request, "core/admin_reports.html", context)



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            subject=request.POST.get("subject"),
            message=request.POST.get("message")
        )
        messages.success(request, "Message sent successfully.")
        return redirect("contact")

    return render(request, "core/contact.html")





from django.shortcuts import render

def about(request):
    return render(request, 'core/about.html')

def scheme(request):
    return render(request, 'core/schemes.html')