from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .models import Material, DonationRequest
from .forms import MaterialForm, DonationRequestForm


# ---------------------- PUBLIC VIEWS ----------------------

def home(request):
    return render(request, 'home.html')


def browse(request):
    materials = Material.objects.all().order_by('-added_on')
    return render(request, 'browse.html', {'materials': materials})


def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)
    return render(request, 'materialbank/material_detail.html', {'material': material})


def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('browse')
    else:
        form = MaterialForm()
    return render(request, 'upload.html', {'form': form})


def donate_material(request):
    if request.method == 'POST':
        form = DonationRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation submitted for approval!')
            return redirect('home')
    else:
        form = DonationRequestForm()
    return render(request, 'materialbank/donate.html', {'form': form})

# def use_material(request, material_id):
#     material = get_object_or_404(Material, id=material_id)
#     if request.method == "POST":
#         used_qty = int(request.POST.get("used_quantity", 0))
#         if used_qty > 0 and used_qty <= material.quantity:
#             material.quantity -= used_qty
#             if material.quantity == 0:
#                 material.delete()  # remove if fully used
#             else:
#                 material.save()
#     return redirect('browse')



# ---------------------- ADMIN / RITI MEMBER VIEWS ----------------------

def is_riti_member(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_riti_member)
def manage_requests(request):
    # Show only pending requests
    requests = DonationRequest.objects.filter(status='Pending').order_by('-created_at')
    return render(request, 'manage_requests.html', {'requests': requests})



from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import DonationRequest, Material, Points
@login_required
@user_passes_test(is_riti_member)
def approve_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)
    # if request.method == "POST":
    #     points_given = int(request.POST.get("points", 0))  # get points manually entered
    # # Mark as approved
    #     donation_request.status = 'approved'
    #     donation_request.save()

    #     # Move to MaterialBank
    #     Material.objects.create(
    #         name=donation_request.name,
    #         category=donation_request.category,
    #         quantity=donation_request.quantity,
    #         description=donation_request.description,
    #         image=donation_request.image,
    #         email=donation_request.email,
    #         donator_name=donation_request.donator_name,
    #         current_with=donation_request.donator_name  # corrected field name
    #     )

    #     # ✅ Add points to donor
    #     # donation_points = donation_request.quantity * 10  # customize multiplier
    #     # points, created = Points.objects.get_or_create(email=donation_request.email)
    #     # points.total_points += donation_points
    #     # points.save()

    #     points, created = Points.objects.get_or_create(email=donation_request.email)
    #     points.total_points += points_given
    #     points.save()

    #     # ✅ Send email notification
    #     send_mail(
    #         subject="🎉 Your donation was approved!",
    #         message=f"Hi {donation_request.donator_name},\n\n"
    #                 f"Your donation of '{donation_request.name}' has been accepted by Riti.\n"
    #                 f"You’ve earned {points_given} Riti Points!\n"
    #                 f"Your total points: {points.total_points}\n\n"
    #                 f"Keep up the great work!\n– Team Riti 💚",
    #         from_email=settings.DEFAULT_FROM_EMAIL,
    #         recipient_list=[donation_request.email],
    #         fail_silently=False,
    #     )

    #     messages.success(request, f"Request for {donation_request.name} approved and added to Material Bank.")
    #     return redirect('manage_requests')
    # return render(request, 'materialbank/approve_request.html', {'donation_request': donation_request})
    donation_request.status = 'approved'
    donation_request.save()

        # Move to MaterialBank
    Material.objects.create(
        name=donation_request.name,
        category=donation_request.category,
        quantity=donation_request.quantity,
        description=donation_request.description,
        image=donation_request.image,
        email=donation_request.email,
        donator_name=donation_request.donator_name,
        current_with=donation_request.donator_name  # corrected field name
    )

        # ✅ Add points to donor
    donation_points = donation_request.quantity * 10  # customize multiplier
    points, created = Points.objects.get_or_create(email=donation_request.email)
    points.total_points += donation_points
    points.save()

    # points, created = Points.objects.get_or_create(email=donation_request.email)
    # points.total_points += points_given
    # points.save()

        # ✅ Send email notification
    send_mail(
        subject="🎉 Your donation was approved!",
        message=f"Hi {donation_request.donator_name},\n\n"
                f"Your donation of '{donation_request.name}' has been accepted by Riti.\n"
                f"You’ve earned {donation_points} Riti Points!\n"
                f"Your total points: {points.total_points}\n\n"
                f"Keep up the great work!\n– Team Riti 💚",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[donation_request.email],
        fail_silently=False,
    )

    messages.success(request, f"Request for {donation_request.name} approved and added to Material Bank.")
    return redirect('manage_requests')

@login_required
@user_passes_test(is_riti_member)
def decline_request(request, request_id):
    donation_request = get_object_or_404(DonationRequest, id=request_id)
    donation_request.status = 'rejected'
    donation_request.save()

    messages.info(request, f"Request for {donation_request.name} has been declined.")
    return redirect('manage_requests')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from .models import Material

def is_riti_member(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_riti_member)
def use_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == "POST":
        used_qty = int(request.POST.get("used_quantity", 0))
        if used_qty > 0 and used_qty <= material.quantity:
            material.quantity -= used_qty
            if material.quantity == 0:
                material.delete()
            else:
                material.save()
    return redirect('browse')
