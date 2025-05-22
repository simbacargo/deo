from django.db import models
from django.db.models import Model, CharField, DateTimeField,TextField, CASCADE,Sum
from authentication.models import User
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(TimeStampedModel):
    BUSINESS_TYPE_CHOICES = [
        ('SMALL_BUSINESS', 'Small Business'),
        ('STARTUP', 'Startup'),
        ('SOLOPRENEUR', 'Solopreneur'),
        ('CORPORATION', 'Corporation'),
    ]
    # user = models.OneToOneField(User,null=True, on_delete=models.CASCADE, related_name='vendor_profile')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, default='SMALL_BUSINESS')
    credit_score = models.PositiveIntegerField(help_text="Vendor's credit score for loan approval")
    address = models.TextField()
    account_number = models.CharField(max_length=30)
    bank_name = models.CharField(max_length=255)
    photo=models.ImageField(null=1 ,blank=1)
    credit_score = models.PositiveIntegerField(default=650, help_text="Vendor's credit score for loan approval")
    
    def __str__(self):
        return self.name

    def calculate_credit_score(self):
        """
        Calculate the credit score of the vendor based on their loan repayment history.
        This includes on-time payments, overdue loans, and other factors.
        """
        credit_score = 650  # Starting score (neutral score)

        # Impact based on loan repayments
        loans = Loan.objects.filter(vendor=self)

        # Calculate positive impact for on-time payments
        on_time_payments = 0
        overdue_loans = 0
        total_loan_amount = 0
        for loan in loans:
            total_loan_amount += loan.amount
            if loan.status == 'REPAID':
                # Calculate how many payments were made on time
                on_time_payments += loan.payments.filter(status='COMPLETED').count()
            elif loan.is_overdue():
                overdue_loans += 1

        # Positive impact: +1 point for every on-time payment made
        credit_score += on_time_payments * 5

        # Negative impact: -20 points for each overdue loan
        credit_score -= overdue_loans * 20

        # If the loan amount is higher, it might reduce the credit score (e.g., higher risk)
        if total_loan_amount > 10000:  # Arbitrary threshold, adjust as needed
            credit_score -= 10

        # Ensure the credit score stays within a reasonable range (300-850)
        credit_score = max(300, min(850, credit_score))

        self.credit_score = credit_score
        self.save()

        return credit_score

    def get_outstanding_loans(self):
        """Return total outstanding loan amount for the vendor."""
        loans = Loan.objects.filter(vendor=self, status__in=['PENDING', 'APPROVED'])
        return sum([loan.amount - loan.payments.all().aggregate(models.Sum('amount'))['amount__sum'] for loan in loans])


class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255)
    # user = models.OneToOneField(User,null=True, on_delete=models.CASCADE, related_name='supplier_profile')
    contact_person = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    is_verified = models.BooleanField(default=False, help_text="Whether the supplier is verified by your platform")

    def __str__(self):
        return self.name




class Loan(TimeStampedModel):
    LOAN_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REPAID', 'Repaid'),
        ('OVERDUE', 'Overdue'),
    ]
    
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_date = models.DateTimeField()
    due_date = models.DateTimeField()
    repayment_frequency = models.CharField(max_length=20, choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly')], default='MONTHLY')
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='PENDING')
    total_repaid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual interest rate on loan amount")
    
    def __str__(self):
        return f"Loan {self.id} for {self.vendor.name}"

    def is_repaid(self):
        """Returns whether the loan is fully repaid."""
        if not self.pk:  # Check if the Loan object has a primary key
            return False  # If no primary key, return False, meaning it's not fully repaid
        
        # If it has a primary key, proceed to aggregate payments
        total_paid = self.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        return total_paid >= self.amount


    def check_and_update_status(self,skip_check=False):
        if not skip_check:
            """Check and update the loan status (REPAID, OVERDUE, or PENDING)."""
            if self.is_repaid():
                self.status = 'REPAID'
            elif self.due_date < timezone.now() and not self.is_repaid():
                self.status = 'OVERDUE'
            else:
                self.status = 'PENDING'
            self.save()

    def save(self, *args, **kwargs):
        """Override save to automatically check loan status upon saving."""
        self.check_and_update_status(skip_check=True)
        super().save(*args, **kwargs)

    
class Payment(TimeStampedModel):
    PAYMENT_METHOD_CHOICES = [
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('MOBILE_MONEY', 'Mobile Money'),
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
    ]

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status_choices = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Payment {self.id} - {self.vendor.name} - {self.amount}"

    def mark_as_completed(self):
        """Mark this payment as completed and update loan repayment."""
        self.status = 'COMPLETED'
        self.loan.total_repaid += self.amount
        self.loan.save()
        self.save()

        # Check and update loan status (whether it's fully repaid, overdue, etc.)
        self.loan.check_and_update_status()

        # Recalculate vendor's credit score based on payment changes
        self.loan.vendor.calculate_credit_score()



class Product(TimeStampedModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField(default=10, help_text="Minimum stock level before reordering.")
    is_available_for_vendors = models.BooleanField(default=True, help_text="Indicates if this product is available for purchase by vendors.")

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.quantity_in_stock > 0

class LoanRepaymentSchedule(TimeStampedModel):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayment_schedules')
    due_date = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING')

    def __str__(self):
        return f"Repayment {self.id} for Loan {self.loan.id}"

    def mark_as_paid(self):
        self.status = 'PAID'
        self.save()

