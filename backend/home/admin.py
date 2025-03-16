from django.contrib import admin
from .models import (
TimeStampedModel,
Vendor,
Supplier,
Loan,
Payment,
Product,
LoanRepaymentSchedule,
)
admin.site.register(Vendor)
admin.site.register(Supplier)
admin.site.register(Loan)
admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(LoanRepaymentSchedule)