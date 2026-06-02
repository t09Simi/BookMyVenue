from django.db import models
from decimal import Decimal

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import RangeOperators
from django.db.models import Q, F, CheckConstraint

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'       
        CONFIRMED = 'confirmed', 'Confirmed' 
        REJECTED = 'rejected', 'Rejected'    
        CANCELLED = 'cancelled', 'Cancelled' 
        COMPLETED = 'completed', 'Completed'


    customer = models.ForeignKey("accounts.User", 
                                 on_delete=models.PROTECT,
                                 related_name="customer_bookings")
    
    venue = models.ForeignKey("accounts.Venue", 
                              on_delete=models.PROTECT,
                              related_name="venue_bookings")
    
    start_time = models.DateTimeField(help_text="Must be top-of-the-hour (e.g., 14:00:00)")

    end_time = models.DateTimeField(help_text="Must be top-of-the-hour (e.g., 16:00:00)")

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True) 


    def calculate_total_price(self):
        hours = (self.end_time - self.start_time).total_seconds()/3600
        return Decimal(str(hours)) * self.venue.price_per_hour
    

    def __str__(self):
        return f"{self.customer.email} has {self.venue.name} booking on {self.start_time} with a {self.status} status"
    
    
    class Meta:
        constraints = [
            # Rule 1: no two bookings overlap for the same venue
            # ...but only for "live" bookings — cancelled/rejected don't block reuse
            ExclusionConstraint(
                name="prevent_overlapping_bookings",
                expressions=[
                    ("venue", RangeOperators.EQUAL),
                    (
                        models.Func(
                            "start_time",
                            "end_time",
                            models.Value("[)"),
                            function="tstzrange",
                            output_field=models.Field(),
                        ),
                        RangeOperators.OVERLAPS,
                    ),  
                ],
                condition=Q(status__in=["pending", "confirmed"]),
            ),
            # Rule 2: end must be after start
            CheckConstraint(
                condition=Q(end_time__gt=F("start_time")),
                name="end_after_start",
            ),
            # Rule 3: total price non-negative
            CheckConstraint(
                condition=Q(total_price__gte=0),
                name="non_negative_total_price",
            ),
        ]
