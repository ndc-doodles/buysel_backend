from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache

from .forms import SuperuserLoginForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from . models import *
from agents.models import *
from django.shortcuts import render, redirect, get_object_or_404, redirect
from . forms import *
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.hashers import make_password 

from django.http import JsonResponse

from django.db.models import Count











# Create your views here.
# def admin_page(request):

#     return render(request, 'admin.html')

def base(request):
    agenthouse = agenthouse.objects.all()

    context ={
        'agenthouse': agenthouse
    }
    return render(request,'base2.html',context)




from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
# def superuser_login_view(request):
#     User = get_user_model()
#     if request.method == 'POST':
#         form = SuperuserLoginForm(request.POST)
#         holder = User.objects.filter(is_superuser=True).first()
#         if holder.rate_limit >= 5 and timezone.now() < holder.last_failed_login + timedelta(hours=5):
#             print('the login is limited')
#         else:
#             holder = User.objects.filter(is_superuser=True).first()
#             if holder.rate_limit >= 5:
#                 holder.rate_limit = 0
#                 holder.save()
#             else:
#                 if form.is_valid():
#                     username = form.cleaned_data['username']
#                     password = form.cleaned_data['password']
#                     user = authenticate(request, username=username, password=password)
#                     if user is not None and user.is_superuser:
#                         holder = User.objects.filter(is_superuser=True).first()
#                         if holder:
#                             holder.rate_limit = 0
#                             holder.save()
#                         login(request, user)
#                         return redirect(reverse('admin_panel') + '#dashboard')  # custom redirect
#                     else:
#                         holder = User.objects.filter(is_superuser=True).first()
#                         if holder:
#                             holder.rate_limit += 1
#                             holder.last_failed_login = timezone.now()
#                             holder.save()
#                             print('Rate limit incremented:', holder.rate_limit)
#                         messages.error(request, 'Invalid credentials or not a superuser.')
#     else:
#         form = SuperuserLoginForm()
#     return render(request, 'login.html', {'form': form})

def superuser_login_view(request):
    User = get_user_model()
    form = SuperuserLoginForm(request.POST or None)
    holder = User.objects.filter(is_superuser=True).first()

    if request.method == 'POST':
        if holder and holder.rate_limit >= 5 and timezone.now() < holder.last_failed_login + timedelta(hours=5):
            messages.error(request, "Too many failed attempts. Try again later.")
        else:
            if holder and holder.rate_limit >= 5:
                holder.rate_limit = 0
                holder.save()

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)

                if user and user.is_superuser:
                    if holder:
                        holder.rate_limit = 0
                        holder.save()
                    login(request, user)
                    return redirect(reverse('dashboard'))  # ✅ redirect to dashboard
                else:
                    if holder:
                        holder.rate_limit += 1
                        holder.last_failed_login = timezone.now()
                        holder.save()
                    messages.error(request, 'Invalid credentials or not a superuser.')

    return render(request, 'login.html', {'form': form})


# ✅ Dashboard view (only for logged-in superusers)
def superuser_required(user):
    return user.is_authenticated and user.is_superuser

# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# def Dashboard(request):
#     return render(request, 'admin_dashboard.html')



# @never_cache
# @user_passes_test(superuser_required, login_url='superuser_login_view')
# def Dashboard(request):
#     # ✅ Total properties
#     total_active = Property.objects.count()
#     total_expired = ExpiredProperty.objects.count()
#     total_all = total_active + total_expired
#
#     # ✅ Group by purpose
#     active_by_purpose = (
#         Property.objects.values("purpose__name")
#         .annotate(total=Count("id"))
#         .order_by("purpose__name")
#     )
#
#     expired_by_purpose = (
#         ExpiredProperty.objects.values("purpose__name")
#         .annotate(total=Count("id"))
#         .order_by("purpose__name")
#     )
#
#     # ✅ Premium agent report
#     premium_report = []
#     premiums = Premium.objects.annotate(total_properties=Count("properties"))
#     for idx, premium in enumerate(premiums, start=1):
#         purpose_counts = (
#             AgentProperty.objects.filter(agent=premium)
#             .values("purpose__name")
#             .annotate(total=Count("id"))
#             .order_by("purpose__name")
#         )
#         premium_report.append({
#             "sl_no": idx,
#             "premium_name": premium.name,
#             "total_properties": premium.total_properties,
#             "by_purpose": purpose_counts,
#         })
#
#     context = {
#         "total_active": total_active,
#         "total_expired": total_expired,
#         "total_all": total_all,
#         "active_by_purpose": active_by_purpose,
#         "expired_by_purpose": expired_by_purpose,
#         "premium_report": premium_report,  # added
#     }
#
#     return render(request, "admin_dashboard.html", context)


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def Dashboard(request):
    # ✅ Total properties
    total_active = Property.objects.count()
    total_expired = ExpiredProperty.objects.count()
    total_all = total_active + total_expired

    # ✅ Get list of all purposes (for dynamic table headers)
    all_purposes = list(Property.objects.values_list("purpose__name", flat=True).distinct())

    # ✅ Premium agent report
    premium_report = []
    premiums = Premium.objects.annotate(total_properties=Count("properties"))
    for idx, premium in enumerate(premiums, start=1):
        # Build purpose → total mapping
        purpose_map = {p: 0 for p in all_purposes}
        purpose_counts = (
            AgentProperty.objects.filter(agent=premium)
            .values("purpose__name")
            .annotate(total=Count("id"))
        )
        for pc in purpose_counts:
            purpose_map[pc["purpose__name"]] = pc["total"]

        premium_report.append({
            "sl_no": idx,
            "premium_name": premium.name,
            "total_properties": premium.total_properties,
            "purpose_map": purpose_map,
        })

    context = {
        "total_active": total_active,
        "total_expired": total_expired,
        "total_all": total_all,
        "all_purposes": all_purposes,      # ✅ purposes for table headers
        "premium_report": premium_report,  # ✅ agent data
    }

    return render(request, "admin_dashboard.html", context)





from django.contrib.auth import logout

# def superuser_logout_view(request):
#     logout(request)
#     messages.success(request, "You have been logged out successfully.")
#     return render(request, 'login.html')
def superuser_logout_view(request):
    logout(request)
    return redirect('superuser_login_view')  



from uuid import UUID
from django.contrib import messages

from django.urls import reverse





@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def create_blog(request):
    if request.method == "POST":
        blog_head = request.POST.get("blog_head")
        modal_head = request.POST.get("modal_head")
        date = request.POST.get("date")
        card_paragraph = request.POST.get("card_paragraph")
        modal_paragraph = request.POST.get("modal_paragraph")
        image = request.FILES.get("image")

        Blog.objects.create(
            blog_head=blog_head,
            modal_head=modal_head,
            date=date,
            card_paragraph=card_paragraph,
            modal_paragraph=modal_paragraph,
            image=image,
        )
        return redirect(reverse('create_blog'))

    # ✅ Pagination
    blog_list = Blog.objects.all().order_by("-id")   # latest first
    paginator = Paginator(blog_list, 1)  # 5 blogs per page

    page_number = request.GET.get("page")
    blog_page = paginator.get_page(page_number)

    return render(request, "admin_blogs.html", {
        'blog': blog_page
    })

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def update_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == "POST":
        blog.blog_head = request.POST.get("blog_head")
        blog.modal_head = request.POST.get("modal_head")
        blog.date = request.POST.get("date")
        blog.card_paragraph = request.POST.get("card_paragraph")
        blog.modal_paragraph = request.POST.get("modal_paragraph")
        if request.FILES.get("image"):
            blog.image = request.FILES.get("image")
        blog.save()
        return redirect("create_blog")
    return redirect("create_blog")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    return redirect("create_blog")








@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def categories(request):
    categories = Category.objects.all()
    purposes = Purpose.objects.all()

    if request.method == 'POST':
        # Handle Category Add/Delete
        if 'add' in request.POST and 'name' in request.POST:
            name = request.POST.get('name')
            if name:
                Category.objects.create(name=name)
            return redirect('categories')

        if 'delete' in request.POST and 'category_id' in request.POST:
            category_id = request.POST.get('category_id')
            Category.objects.filter(id=category_id).delete()
            return redirect('categories')

        # Handle Purpose Add/Delete
        if 'add' in request.POST and 'purposename' in request.POST:
            name = request.POST.get('purposename')
            if name:
                Purpose.objects.create(name=name)
            return redirect('categories')

        if 'delete' in request.POST and 'purpose_id' in request.POST:
            purpose_id = request.POST.get('purpose_id')
            Purpose.objects.filter(id=purpose_id).delete()
            return redirect('categories')

    return render(request, 'admin_categories.html', {
        'categories': categories,
        'purposes': purposes
    })

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def add_property(request):
    categories = Category.objects.all()
    purposes = Purpose.objects.all()
    properties = Property.objects.all()

    if request.method == "POST":
        category_id = request.POST.get("category")
        purpose_id = request.POST.get("purpose")

        amenities = request.POST.getlist('amenities')
        amenities_str = ", ".join([a.strip() for a in amenities if a.strip()])


        uploaded_images = request.FILES.getlist("images")
        main_image = uploaded_images[0] if uploaded_images else None  

        property_obj = Property.objects.create(
            category_id=category_id,
            purpose_id=purpose_id,
            label=request.POST.get("label"),
            land_area=request.POST.get("land_area"),
            sq_ft=request.POST.get("sq_ft"),
            description=request.POST.get("description"),
            amenities=amenities_str,
            image=main_image,
            perprice=request.POST.get("perprice"),
            price=request.POST.get("price"),
            owner=request.POST.get("owner"),
            whatsapp=request.POST.get("whatsapp"),
            phone=request.POST.get("phone"),
            location=request.POST.get("location"),
            city=request.POST.get("city"),
            pincode=request.POST.get("pincode"),
            district=request.POST.get("district"),
            land_mark=request.POST.get("land_mark"),
            paid=request.POST.get("paid"),
            added_by=request.POST.get("added_by"),
            # ✅ Ensure integer
            duration_days=int(request.POST.get("duration_days") or 30),
        )


        # ✅ Save extra images
        for extra_img in uploaded_images[1:]:
            PropertyImage.objects.create(property=property_obj, image=extra_img)

        return redirect("add_property")

    return render(request, "admin_propertylistings.html", {
        "categories": categories,
        "purposes": purposes,
        "properties": properties,
    })








@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def edit_property(request, property_id):
    prop = get_object_or_404(Property, id=property_id)

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")
    prop.label = request.POST.get('label')
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    amenities = request.POST.get("amenities")
    prop.amenities = amenities
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.owner = request.POST.get("owner")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.pincode = request.POST.get("pincode")
    prop.land_mark = request.POST.get("land_mark")
    prop.paid = request.POST.get("paid") == "Yes"
    prop.added_by = request.POST.get("added_by")

    # 🔥 Cast to int to avoid TypeError
    duration_days = request.POST.get("duration_days")
    if duration_days:
        try:
            prop.duration_days = int(duration_days)
        except ValueError:
            prop.duration_days = 0  # fallback if bad input

    if category_id:
        prop.category = get_object_or_404(Category, id=category_id)
    if purpose_id:
        prop.purpose = get_object_or_404(Purpose, id=purpose_id)

    prop.save()

    # ✅ Handle multiple new images
    images = request.FILES.getlist("images")
    if images:
        for img in images:
            PropertyImage.objects.create(property=prop, image=img)

    # ✅ Handle image deletions
    delete_images = request.POST.getlist("delete_images")  # comes from checkboxes/hidden inputs
    if delete_images:
        for img_id in delete_images:
            try:
                image_obj = PropertyImage.objects.get(id=img_id, property=prop)
                image_obj.delete()
            except PropertyImage.DoesNotExist:
                pass

    messages.success(request, "Property updated successfully.")
    return redirect('add_property')


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    prop.delete()
    return redirect('add_property')



@user_passes_test(superuser_required, login_url='superuser_login_view')
def agents_login(request):
    if request.method == "POST":
        if "username" in request.POST:   # Premium Agent Login form
            name = request.POST.get("name")
            speacialised = request.POST.get("speacialised")
            phone = request.POST.get("phone")
            whatsapp = request.POST.get("whatsapp")
            email = request.POST.get("email")
            location = request.POST.get("location")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")
            username = request.POST.get("username")
            password = request.POST.get("password")
            image = request.FILES.get("image")
            duration_days = request.POST.get("duration_days")  # ✅ from POST, not FILES

            # optional: check duplicate username
            if Premium.objects.filter(username=username).exists():
                messages.error(request, "❌ This username is already registered.")
                return redirect("agents_login")

            Premium.objects.create(
                name=name,
                speacialised=speacialised,
                phone=phone,
                whatsapp=whatsapp,
                email=email,
                location=location,
                city=city,
                pincode=pincode,
                username=username,
                password=make_password(password),
                image=image,
                duration_days=duration_days,
                created_at=timezone.now()
            )
            messages.success(request, "✅ Premium Agent created successfully!")

        elif "agentname" in request.POST:   # ✅ Normal Agent form
            agentsname = request.POST.get("agentname")
            agentsspeacialised = request.POST.get("agentspeacialised")
            agentsphone = request.POST.get("agentphone")
            agentswhatsapp = request.POST.get("agentwhatsapp")
            agentsemail = request.POST.get("agentemail")
            agentslocation = request.POST.get("agentlocation")
            agentsimage = request.FILES.get("agentsimage")  # ✅ file input

            # optional: avoid duplicate phone numbers
            if Agents.objects.filter(agentsphone=agentsphone).exists():
                messages.error(request, "❌ This phone number is already registered.")
                return redirect("agents_login")

            Agents.objects.create(
                agentsname=agentsname,
                agentsspeacialised=agentsspeacialised,
                agentsphone=agentsphone,
                agentswhatsapp=agentswhatsapp,
                agentsemail=agentsemail,
                agentslocation=agentslocation,
                agentsimage=agentsimage   # ✅ matches your model
            )
            messages.success(request, "✅ Agent added successfully!")

    return render(request, "admin_agentlogin.html")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_premiumagents(request):
    premium = Premium.objects.all()
    return render(request, 'admin_premiumagents.html',{'premium':premium})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_agents(request):
    premium = Premium.objects.all()
    agents = Agents.objects.all()
    return render(request, 'admin_agents.html',{'premium':premium, 'agents':agents})


@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_premium(request, pk):
    premium = get_object_or_404(Premium, pk=pk)

    if request.method == "POST":
        premium.name = request.POST.get("name", premium.name)
        premium.speacialised = request.POST.get("speacialised", premium.speacialised)
        premium.phone = request.POST.get("phone", premium.phone)
        premium.whatsapp = request.POST.get("whatsapp", premium.whatsapp)
        premium.email = request.POST.get("email", premium.email)
        premium.location = request.POST.get("location", premium.location)
        premium.city = request.POST.get("city", premium.city)

        if "image" in request.FILES:
            premium.image = request.FILES["image"]

        premium.save()

        return redirect("admin_premiumagents")  # redirect back to list page

    return render(request, "admin_premiumagents.html", {"premium": premium})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_premium(request, pk):
    premium = get_object_or_404(Premium, pk=pk)
    premium.delete()
    messages.success(request, "🗑️ Premium Agent deleted successfully!")
    return redirect("admin_premiumagents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    if request.method == "POST":
        agent.agentsname = request.POST.get("name")
        agent.agentsspeacialised = request.POST.get("specialised")
        agent.agentsphone = request.POST.get("phone")
        agent.agentswhatsapp = request.POST.get("whatsapp")
        agent.agentsemail = request.POST.get("email")
        agent.agentslocation = request.POST.get("location")
        agent.agentspincode = request.POST.get("pincode")


        if request.FILES.get("image"):
            agent.agentsimage = request.FILES.get("image")

        agent.save()
        messages.success(request, "✅ Agent updated successfully!")
        return redirect("admin_agents")  # adjust to your listing page

    return redirect("admin_agents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent(request, pk):
    agent = get_object_or_404(Agents, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("admin_agents")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_contact(request):
    contact_list = Contact.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 contacts per page
    paginator = Paginator(contact_list, 1)
    page_number = request.GET.get("page")
    contacts = paginator.get_page(page_number)

    return render(request, 'admin_contact.html', {'contacts': contacts})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "🗑️ Contact deleted successfully!")
    return redirect("admin_contact")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_message(request):
    message_list = Inbox.objects.all().order_by("-created_at")  # latest first
    
    # pagination: 10 per page
    paginator = Paginator(message_list, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_messagebox.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_message(request, pk):
    message = get_object_or_404(Inbox, pk=pk)
    message.delete()
    messages.success(request, "🗑️ Message deleted successfully!")  # flash message
    return redirect("admin_message")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_agent_reg(request):
    agent_list = AgentForm.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(agent_list, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_agentsregisterations.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_agent_reg(request, pk):
    agent = get_object_or_404(AgentForm, pk=pk)
    agent.delete()
    messages.success(request, "🗑️ Agent deleted successfully!")
    return redirect("agent_reg")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_property_list(request):
    property_list = Propertylist.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(property_list, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_propertyregisterations.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_property_list(request, pk):
    property_list = get_object_or_404(Propertylist, pk=pk)
    property_list.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("admin_property_list")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def admin_request(request):
    requestforms = Request.objects.all().order_by("-created_at")  # latest first
    
    paginator = Paginator(requestforms, 1)  # paginate (2 per page for testing)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  

    return render(request, 'admin_requestform.html', {'page_obj': page_obj})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def delete_requestforms(request, pk):
    requestforms = get_object_or_404(Request, pk=pk)
    requestforms.delete()
    messages.success(request, "🗑️ Property deleted successfully!")
    return redirect("requestforms")

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def expired_property(request):
    expired = ExpiredProperty.objects.all()
    category = Category.objects.all()
    purpose = Purpose.objects.all()
    return render(request, 'admin_expiredproperties.html',{
        'property': expired,
        'category': category,
        'purpose':purpose
        })

@never_cache
@require_POST
def edit_exproperty(request, property_id):
    prop = get_object_or_404(ExpiredProperty, id=property_id)

    category_id = request.POST.get("category")
    purpose_id = request.POST.get("purpose")
    prop.label = request.POST.get('label')
    prop.land_area = request.POST.get("land_area")
    prop.sq_ft = request.POST.get("sq_ft")
    prop.description = request.POST.get("description")
    prop.amenities = request.POST.get("amenities")
    prop.perprice = request.POST.get("perprice")
    prop.price = request.POST.get("price")
    prop.owner = request.POST.get("owner")
    prop.whatsapp = request.POST.get("whatsapp")
    prop.phone = request.POST.get("phone")
    prop.location = request.POST.get("location")
    prop.city = request.POST.get("city")
    prop.pincode = request.POST.get("pincode")
    prop.land_mark = request.POST.get("land_mark")
    prop.paid = request.POST.get("paid") == "Yes"
    prop.added_by = request.POST.get("added_by")

    # Duration
    duration_days = request.POST.get("duration_days")
    if duration_days:
        try:
            prop.duration_days = int(duration_days)
        except ValueError:
            prop.duration_days = 0

    if category_id:
        prop.category = get_object_or_404(Category, id=category_id)
    if purpose_id:
        prop.purpose = get_object_or_404(Purpose, id=purpose_id)

    prop.save()

    # Handle new images
    for img in request.FILES.getlist("images"):
        PropertyImage.objects.create(expired_property=prop, image=img)

    # Handle image deletions
    for img_id in request.POST.getlist("delete_images"):
        try:
            image_obj = PropertyImage.objects.get(id=img_id, expired_property=prop)
            image_obj.delete()
        except PropertyImage.DoesNotExist:
            pass

    messages.success(request, "Property updated successfully.")
    return redirect('expired_property')

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
@require_POST
def delete_property(request, pk):
    prop = get_object_or_404(ExpiredProperty, pk=pk)
    prop.delete()
    return redirect('expired_property')

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def expire_premium(request):
    premium = ExpiredPremium.objects.all()
    agents = ExpireAgents.objects.all()
    return render(request, 'admin_expiredagents.html',{'premium':premium,'agents':agents})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_expirepremium(request, pk):
    premium = get_object_or_404(ExpiredPremium, pk=pk)

    if request.method == "POST":
        premium.name = request.POST.get("name", premium.name)
        premium.speacialised = request.POST.get("speacialised", premium.speacialised)
        premium.phone = request.POST.get("phone", premium.phone)
        premium.whatsapp = request.POST.get("whatsapp", premium.whatsapp)
        premium.email = request.POST.get("email", premium.email)
        premium.location = request.POST.get("location", premium.location)
        premium.city = request.POST.get("city", premium.city)
        premium.duration_days = request.POST.get("duration_days", premium.duration_days)


        if "image" in request.FILES:
            premium.image = request.FILES["image"]

        premium.save()

        return redirect("expired_agent")  # redirect back to list page

    return render(request, "admin_expiredagents.html", {"premium": premium})

@never_cache
@user_passes_test(superuser_required, login_url='superuser_login_view')
def edit_expireagent(request, pk):
    agent = get_object_or_404(ExpireAgents, pk=pk)
    if request.method == "POST":
        agent.agentsname = request.POST.get("name")
        agent.agentsspeacialised = request.POST.get("specialised")
        agent.agentsphone = request.POST.get("phone")
        agent.agentswhatsapp = request.POST.get("whatsapp")
        agent.agentsemail = request.POST.get("email")
        agent.agentslocation = request.POST.get("location")
        agent.agentspincode = request.POST.get("pincode")
        agent.agentscity = request.POST.get("city")
        agent.duration_days = request.POST.get("duration_days")



        if request.FILES.get("image"):
            agent.agentsimage = request.FILES.get("image")

        agent.save()
        messages.success(request, "✅ Agent updated successfully!")
        return redirect("expired_agent")  # adjust to your listing page

    return redirect("expired_agent")






