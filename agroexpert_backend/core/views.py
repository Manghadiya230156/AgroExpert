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
from .models import FertilizerHistory, MarketPriceSnapshot

import joblib
import os
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import hashlib
import json
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
from .models import Profile, SoilTestRequest, FertilizerHistory


@login_required
def admin_dashboard(request):

    if request.user.profile.role != "admin":
        return redirect("dashboard")

    total_users = User.objects.count()
    farmers = Profile.objects.filter(role="farmer").count()
    admins = Profile.objects.filter(role="admin").count()
    pending_soil = SoilTestRequest.objects.filter(status="Pending").count()

    fertilizer_count = FertilizerHistory.objects.count()

    context = {
        "total_users": total_users,
        "farmers": farmers,
        "admins": admins,
        "pending_soil": pending_soil,
        "fertilizer_count": fertilizer_count,
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

# State and district choices are UI metadata, not market-price claims.
INDIAN_STATES_AND_UTS = [
    "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam",
    "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir",
    "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep", "Madhya Pradesh",
    "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha",
    "Puducherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
    "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
]

# Current district names for the two focus states. For other states, the district
# endpoint falls back to districts that actually occur in the official price feed.
STATE_DISTRICTS = {
    "Gujarat": [
        "Ahmedabad", "Amreli", "Anand", "Aravalli", "Banaskantha", "Bharuch",
        "Bhavnagar", "Botad", "Chhota Udepur", "Dahod", "Dang", "Devbhoomi Dwarka",
        "Gandhinagar", "Gir Somnath", "Jamnagar", "Junagadh", "Kachchh", "Kheda",
        "Mahisagar", "Mehsana", "Morbi", "Narmada", "Navsari", "Panchmahal",
        "Patan", "Porbandar", "Rajkot", "Sabarkantha", "Surat", "Surendranagar",
        "Tapi", "Vadodara", "Valsad",
    ],
    "Punjab": [
        "Amritsar", "Barnala", "Bathinda", "Faridkot", "Fatehgarh Sahib", "Fazilka",
        "Ferozepur", "Gurdaspur", "Hoshiarpur", "Jalandhar", "Kapurthala", "Ludhiana",
        "Malerkotla", "Mansa", "Moga", "Pathankot", "Patiala", "Rupnagar",
        "Sahibzada Ajit Singh Nagar", "Sangrur", "Shaheed Bhagat Singh Nagar",
        "Sri Muktsar Sahib", "Tarn Taran",
    ],
}

MARKET_PRICE_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
MARKET_PRICE_SOURCE_URL = "https://data.gov.in/resource/current-daily-price-various-commodities-various-markets-mandi"


def _market_api_key():
    return getattr(settings, "DATA_GOV_IN_API_KEY", "") or os.environ.get("DATA_GOV_IN_API_KEY", "")


def _fetch_market_api(api_filters=None, max_records=20000):
    """Fetch paginated official AGMARKNET rows; never fabricate fallback prices."""
    api_key = _market_api_key()
    if not api_key:
        raise RuntimeError("DATA_GOV_IN_API_KEY is not configured")

    records = []
    offset = 0
    page_size = 1000
    api_total = None
    while offset < max_records:
        params = {"api-key": api_key, "format": "json", "limit": str(min(page_size, max_records - offset)), "offset": str(offset)}
        for key, value in (api_filters or {}).items():
            if value:
                api_field = "state.keyword" if key == "state" else key
                params[f"filters[{api_field}]"] = value
        url = f"https://api.data.gov.in/resource/{MARKET_PRICE_RESOURCE_ID}?" + urlencode(params)
        req = Request(url, headers={"User-Agent": "AgroExpert/1.0"})
        with urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Unexpected response from market-price API")
        page_records = data.get("records") or []
        if api_total is None:
            try:
                api_total = int(data.get("total") or 0)
            except (TypeError, ValueError):
                api_total = 0
        print(f"Market API: total={api_total or 'unknown'}, offset={offset}, received={len(page_records)}")
        if not page_records:
            break
        records.extend(page_records)
        offset += len(page_records)
        if api_total and offset >= api_total:
            break
        if not api_total and len(page_records) < min(page_size, max_records - (offset - len(page_records))):
            break
    return records, api_total


def _normalize_market_records(records):
    normalized = []
    for item in records:
        arrival = str(item.get("arrival_date", "")).strip()
        parsed_date = None
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                parsed_date = datetime.strptime(arrival, fmt).date()
                break
            except (ValueError, TypeError):
                pass

        def number(field):
            try:
                value = float(str(item.get(field, "")).replace(",", ""))
                return value if value >= 0 else None
            except (TypeError, ValueError):
                return None

        normalized.append({
            "state": str(item.get("state", "")).strip(),
            "district": str(item.get("district", "")).strip(),
            "market": str(item.get("market", "")).strip(),
            "commodity": str(item.get("commodity", "")).strip(),
            "variety": str(item.get("variety", "")).strip(),
            "grade": str(item.get("grade", "")).strip(),
            "arrival_date": parsed_date.isoformat() if parsed_date else arrival,
            "min_price": number("min_price"),
            "max_price": number("max_price"),
            "modal_price": number("modal_price"),
        })
    return normalized


def market_price_districts(request):
    """Return districts for the selected state to power the dependent dropdown."""
    from django.http import JsonResponse
    state = request.GET.get("state", "").strip()[:100]
    if not state:
        return JsonResponse({"districts": []})
    if state in STATE_DISTRICTS:
        return JsonResponse({"districts": STATE_DISTRICTS[state]})
    try:
        raw_records, _ = _fetch_market_api({"state": state}, max_records=10000)
        districts = sorted({str(row.get("district", "")).strip() for row in raw_records if row.get("district")})
        return JsonResponse({"districts": districts})
    except Exception:
        # Keep the UI usable when the official API is temporarily unavailable.
        return JsonResponse({"districts": [], "error": "Districts could not be loaded from the official source."}, status=200)


def market_prices(request):
    """Show official daily wholesale prices, with database caching and local date filtering."""
    raw_filters = {
        "state": request.GET.get("state", "Gujarat").strip()[:100],
        "district": request.GET.get("district", "").strip()[:100],
        "commodity": request.GET.get("commodity", "").strip()[:100],
        "from_date": request.GET.get("from_date", "").strip()[:10],
        "to_date": request.GET.get("to_date", "").strip()[:10],
    }
    api_filters = {key: raw_filters[key] for key in ("state", "district", "commodity") if raw_filters[key]}
    cache_key = hashlib.sha256(json.dumps(api_filters, sort_keys=True).encode("utf-8")).hexdigest()
    snapshot = MarketPriceSnapshot.objects.filter(cache_key=cache_key).first()
    now = timezone.now()
    cache_ttl = timedelta(hours=6)
    stale = True
    api_error = ""

    if snapshot and snapshot.fetched_at and now - snapshot.fetched_at < cache_ttl:
        stale = False
    elif _market_api_key():
        try:
            raw_records, api_total = _fetch_market_api(api_filters)
            normalized = _normalize_market_records(raw_records)
            reporting_dates = [r["arrival_date"] for r in normalized if len(r.get("arrival_date", "")) == 10 and r["arrival_date"][4:5] == "-"]
            latest_reporting = max(reporting_dates) if reporting_dates else None
            snapshot, _ = MarketPriceSnapshot.objects.update_or_create(
                cache_key=cache_key,
                defaults={
                    "filters": api_filters,
                    "payload": normalized,
                    "reporting_date": date.fromisoformat(latest_reporting) if latest_reporting else None,
                    "source_title": "AGMARKNET / data.gov.in",
                },
            )
            stale = False
            if api_total and len(normalized) < api_total:
                api_error = f"The source reports {api_total} matching records; this page fetched {len(normalized)} within the safe fetch limit. Narrow the filters to retrieve a smaller result set."
        except Exception:
            api_error = "The government market-data source could not be refreshed. Showing saved results if available."
            if not snapshot:
                api_error = "The government market-data source could not be reached, and no cached results are available. Check the API key and try again."
    elif not snapshot:
        api_error = "Set DATA_GOV_IN_API_KEY in your environment to load official prices. No sample prices are shown as real data."
    else:
        api_error = "The API key is not configured. Showing saved results, which may be outdated."

    records = list(snapshot.payload or []) if snapshot else []
    from_date = to_date = None
    try:
        if raw_filters["from_date"]:
            from_date = date.fromisoformat(raw_filters["from_date"])
    except ValueError:
        raw_filters["from_date"] = ""
    try:
        if raw_filters["to_date"]:
            to_date = date.fromisoformat(raw_filters["to_date"])
    except ValueError:
        raw_filters["to_date"] = ""

    def record_date(row):
        try:
            return date.fromisoformat(row.get("arrival_date", ""))
        except (ValueError, TypeError):
            return None

    if from_date:
        records = [r for r in records if record_date(r) and record_date(r) >= from_date]
    if to_date:
        records = [r for r in records if record_date(r) and record_date(r) <= to_date]
    records.sort(key=lambda r: (r.get("arrival_date", ""), r.get("commodity", "")), reverse=True)
    newest = max((record_date(r) for r in records if record_date(r)), default=None)
    cache_age_hours = max(0, int((now - snapshot.fetched_at).total_seconds() // 3600)) if snapshot and snapshot.fetched_at else None
    context = {
        "records": records,
        "filters": raw_filters,
        "states": INDIAN_STATES_AND_UTS,
        "api_error": api_error,
        "is_stale": bool(snapshot and (stale or (newest and newest < timezone.localdate() - timedelta(days=2)))),
        "fetched_at": snapshot.fetched_at if snapshot else None,
        "reporting_date": newest or (snapshot.reporting_date if snapshot else None),
        "cache_age_hours": cache_age_hours,
        "total_records": len(records),
        "source_url": MARKET_PRICE_SOURCE_URL,
    }
    return render(request, "core/market-prices.html", context)


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
from .models import Profile, SoilTestRequest
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


    context = {
        "total_users": total_users,
        "farmers": farmers,
        "admins": admins,
        "total_soil": total_soil,
        "pending": pending,
        "approved": approved,
        "completed": completed,
        "rejected": rejected,
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

# ================= PLANT DISEASE DETECTION =================
@login_required
def plant_disease_detection(request):
    """Classify an uploaded leaf image using the locally trained model."""
    import io
    from PIL import Image, UnidentifiedImageError
    from .plant_disease import predict_plant_disease
    from .plant_disease_knowledge import get_disease_guidance

    result = None
    error = None
    uploaded_image = None

    if request.method == "POST":
        image_file = request.FILES.get("leaf_image")
        if not image_file:
            error = "Choose a leaf image before submitting."
        elif image_file.size > 8 * 1024 * 1024:
            error = "The image must be 8 MB or smaller."
        else:
            try:
                raw = image_file.read()
                image = Image.open(io.BytesIO(raw))
                image.verify()
                image = Image.open(io.BytesIO(raw)).convert("RGB")
                if image.width < 64 or image.height < 64:
                    raise ValueError("Image is too small. Upload a clear image at least 64 × 64 pixels.")
                label, confidence = predict_plant_disease(image)
                result = get_disease_guidance(label)
                result["confidence"] = round(confidence, 2)
                result["label"] = label
                if confidence < 60:
                    result["confidence_note"] = "Confidence is low. Try a clearer photo with one leaf in focus and consult an agricultural expert before acting."
                elif confidence < 80:
                    result["confidence_note"] = "Treat this as a preliminary result. Similar-looking diseases may be confused by the model."
                else:
                    result["confidence_note"] = "Confidence reflects the model's class score, not a verified probability of a correct diagnosis."
                uploaded_image = True
            except FileNotFoundError:
                error = "The disease model has not been trained yet. Follow the training steps in ml_models/plant_disease/README.md, then restart the server."
            except (UnidentifiedImageError, OSError):
                error = "This file could not be read as an image. Upload a JPG, JPEG, or PNG leaf photo."
            except ValueError as exc:
                error = str(exc)
            except Exception:
                error = "Prediction failed. Check that the trained model and its class-label file are installed correctly."

    return render(request, "core/plant-disease.html", {
        "result": result,
        "error": error,
        "uploaded_image": uploaded_image,
    })
