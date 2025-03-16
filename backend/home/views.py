from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView
from .models import Vendor
from .forms import VendorForm
from django.contrib.auth.mixins import LoginRequiredMixin

# View to list all vendors (Admin-only view)
class VendorCreateView(LoginRequiredMixin,CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/vendor_form.html'
    context_object_name = 'vendor'


class VendorListView(LoginRequiredMixin,ListView):
    model = Vendor
    template_name = 'vendor/vendor_list.html'
    context_object_name = 'vendors'

    def get_queryset(self):
        queryset = super().get_queryset()

        min_credit_score = self.request.GET.get('min_credit_score')
        business_type = self.request.GET.get('business_type')

        # Filter by minimum credit score
        if min_credit_score:
            try:
                min_credit_score = int(min_credit_score)
                queryset = queryset.filter(credit_score__gte=min_credit_score)
            except ValueError:
                pass  # If it's not a valid integer, no filtering by credit score

        # Filter by business type
        if business_type:
            queryset = queryset.filter(business_type=business_type)

        return queryset


# View to display a single vendor's details (vendor dashboard)
class VendorDetailView(LoginRequiredMixin,DetailView):
    model = Vendor
    template_name = 'vendor/vendor_detail.html'
    context_object_name = 'vendor'

# View to update vendor information
@method_decorator(login_required, name='dispatch')
class VendorUpdateView(LoginRequiredMixin,UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor/vendor_form.html'
    success_url = '/vendor/'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Recalculate credit score after vendor information is updated
        self.object.calculate_credit_score()
        return response




# views.py for Loan Views:
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Loan
from .forms import LoanForm
from django.db.models import F
from django.views.generic import ListView
from .models import Loan
from django.utils import timezone

class LoanListView(LoginRequiredMixin,ListView):
    model = Loan
    template_name = 'loan/loan_list.html'
    context_object_name = 'loans'

    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()

        # Get filter parameters from the URL query string
        loan_status = self.request.GET.get('loan_status')
        is_repaid = self.request.GET.get('is_repaid')
        min_due_date = self.request.GET.get('min_due_date')
        max_due_date = self.request.GET.get('max_due_date')

        # Filter by loan status
        if loan_status:
            queryset = queryset.filter(status=loan_status)

        # Filter by repayment status (whether loan is repaid or not)
        if is_repaid is not None:
            is_repaid = is_repaid.lower() == 'true'  # Convert to boolean
            if is_repaid:
                queryset = queryset.filter(total_repaid__gte=F('amount'))  # Fully repaid loans
            else:
                queryset = queryset.filter(total_repaid__lt=F('amount'))  # Loans not fully repaid

        # Filter by due date range
        if min_due_date:
            queryset = queryset.filter(due_date__gte=min_due_date)
        if max_due_date:
            queryset = queryset.filter(due_date__lte=max_due_date)

        return queryset

# View to create a new loan
@login_required
def create_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            loan.vendor = request.user.vendor  # Assuming you have a relationship with the user
            loan.save()
            return redirect('loan_detail', pk=loan.pk)
    else:
        form = LoanForm()
    return render(request, 'loan/loan_form.html', {'form': form})

# View to see loan details and repayments
class LoanDetailView(LoginRequiredMixin,DetailView):
    model = Loan
    template_name = 'loan/loan_detail.html'
    context_object_name = 'loan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['repayments'] = self.object.payments.all()  # Get all payments for this loan
        return context



from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm

from django.views.generic import ListView
from .models import Payment
from django.utils import timezone
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Loan, Payment
from .forms import PaymentForm

@login_required
def make_payment(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    # Check if the loan is already fully repaid
    if loan.status == 'REPAID':
        messages.error(request, "This loan is already fully repaid.")
        return redirect('loan_list')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.loan = loan  # Associate the payment with the loan
            payment.vendor = loan.vendor  # Associate the payment with the vendor making the payment
            payment.status = 'COMPLETED'  # Mark payment as completed upon submission

            # Save the payment and update the loan's total repaid amount
            payment.save()
            payment.loan.total_repaid += payment.amount
            payment.loan.save()

            # Update loan status (REPAID or OVERDUE)
            payment.loan.check_and_update_status()

            # Recalculate the vendor's credit score
            payment.loan.vendor.calculate_credit_score()

            messages.success(request, "Payment successfully made.")
            return redirect('loan_list')  # Redirect to loan list after payment
    else:
        form = PaymentForm()

    return render(request, 'payment/make_payment.html', {'form': form, 'loan': loan})


class PaymentListView(LoginRequiredMixin,ListView):
    model = Payment
    template_name = 'payment/payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()

        # Get filter parameters from the URL query string
        payment_status = self.request.GET.get('payment_status')
        payment_method = self.request.GET.get('payment_method')
        min_payment_date = self.request.GET.get('min_payment_date')
        max_payment_date = self.request.GET.get('max_payment_date')

        # Filter by payment status
        if payment_status:
            queryset = queryset.filter(status=payment_status)

        # Filter by payment method
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        # Filter by payment date range
        if min_payment_date:
            queryset = queryset.filter(payment_date__gte=min_payment_date)
        if max_payment_date:
            queryset = queryset.filter(payment_date__lte=max_payment_date)

        return queryset


# View to make a payment (Vendor's payment page)
@login_required
def make_payment(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.vendor = request.user.vendor  # Assuming a relationship between user and vendor
            payment.loan = loan
            payment.save()
            payment.mark_as_completed()  # Mark payment as completed and update loan status
            return redirect('loan_detail', pk=loan.id)
    else:
        form = PaymentForm()
    return render(request, 'payment/payment_form.html', {'form': form, 'loan': loan})

# View for payment details
class PaymentDetailView(LoginRequiredMixin,DetailView):
    model = Payment
    template_name = 'payment/payment_detail.html'
    context_object_name = 'payment'


from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# View to list all available products
class ProductListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Only show products that are available for vendors to buy
        return Product.objects.filter(is_available_for_vendors=True)


# Supplier Views

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Supplier

# views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Supplier
from .forms import SupplierForm

class SupplierCreateView(LoginRequiredMixin,CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'supplier/supplier_form.html'  # The template we'll create
    success_url = reverse_lazy('supplier_list')  # Redirect to the supplier list page after creating


# View to list all suppliers
class SupplierListView(LoginRequiredMixin,ListView):
    model = Supplier
    template_name = 'supplier/supplier_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()

        # Get the 'is_verified' filter parameter from the URL query string
        is_verified = self.request.GET.get('is_verified')

        # Filter the queryset if 'is_verified' is provided
        if is_verified is not None:
            # Convert the string 'True' or 'False' to actual boolean
            is_verified = is_verified.lower() == 'true'
            queryset = queryset.filter(is_verified=is_verified)

        return queryset


# View to view a single supplier's details
class SupplierDetailView(LoginRequiredMixin,DetailView):
    model = Supplier
    template_name = 'supplier/supplier_detail.html'
    context_object_name = 'supplier'



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Vendor, Product

@login_required
def vendor_dashboard(request):
    vendor = request.user #.vendor  # Assuming that the user is related to the Vendor model
    
    # Get the available products for vendors to buy
    available_products = Product.objects.filter(is_available_for_vendors=True)

    context = {
        'vendor': vendor,
        'available_products': available_products
    }
    return render(request, 'vendor/vendor_dashboard.html', context)


from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Vendor, Loan, Payment

@staff_member_required
def admin_dashboard(request):
    total_vendors = Vendor.objects.count()
    total_loans = Loan.objects.count()
    total_payments = Payment.objects.count()
    pending_payments = Payment.objects.filter(status='PENDING').count()

    context = {
        'total_vendors': total_vendors,
        'total_loans': total_loans,
        'total_payments': total_payments,
        'pending_payments': pending_payments,
    }

    return render(request, 'admin_dashboard.html', context)


from django.views.generic import ListView
from .models import LoanRepaymentSchedule
from django.utils import timezone

class LoanRepaymentScheduleListView(LoginRequiredMixin,ListView):
    model = LoanRepaymentSchedule
    template_name = 'loan_repayment_schedule/loan_repayment_schedule_list.html'
    context_object_name = 'repayment_schedules'

    def get_queryset(self):
        # Get the default queryset
        queryset = super().get_queryset()

        # Get filter parameters from the URL query string
        status = self.request.GET.get('status')
        loan_id = self.request.GET.get('loan_id')
        min_due_date = self.request.GET.get('min_due_date')
        max_due_date = self.request.GET.get('max_due_date')

        # Filter by repayment status (e.g., 'PENDING', 'PAID')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by loan (if a loan is selected)
        if loan_id:
            queryset = queryset.filter(loan__id=loan_id)

        # Filter by due date range
        if min_due_date:
            queryset = queryset.filter(due_date__gte=min_due_date)
        if max_due_date:
            queryset = queryset.filter(due_date__lte=max_due_date)

        return queryset

class LoanRepaymentScheduleDetailView(LoginRequiredMixin,DetailView):
    model = LoanRepaymentSchedule
    template_name = 'vendor/vendor_detail.html'
    context_object_name = 'vendor'



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.contrib.sessions.models import Session
from django.utils.decorators import method_decorator

# Cache the login page for 15 minutes (for performance)
# @cache_page(60 * 15)  # Cache for 15 minutes
def login_view(request):
    # Check if the user is already authenticated (use cache to optimize check)
    user = request.user
    if user.is_authenticated:
        return redirect('admin_dashboard')  # Or the home page or dashboard

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Manually cache the user's login information (e.g., user ID, username, etc.)
                cache.set(f'user_{user.id}_authenticated', True, timeout=60*15)  # Cache for 15 minutes

                # Log the user in
                login(request, user)
                
                # After successful login, redirect to the home page or dashboard
                return redirect('admin_dashboard')
            else:
                # Invalid login credentials
                return HttpResponse('Invalid credentials', status=401)

    else:
        form = AuthenticationForm()

    return render(request, 'auth/login.html', {'form': form})

# Example logout view to clear the cache and session
@login_required
def logout_view(request):
    # Clear cache for the logged-in user
    cache.delete(f'user_{request.user.id}_authenticated')  # Delete the cached data

    # Log the user out
    logout(request)
    
    # Redirect to login page after logout
    return redirect('login')

