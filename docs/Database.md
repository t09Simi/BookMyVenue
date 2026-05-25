# Venue Booking Platform Data Model

```markdown
A customer is only booking venues.

They should be able to:

Register/login
Browse approved venues
Search/filter venues
View amenities/photos/pricing
Book available slots
Pay
Cancel (within policy)
View booking history
Raise disputes
Leave reviews after completed booking.

Owners can

Create venue draft
Edit own venue
Upload photos
Set amenities
Configure pricing
Define availability
View bookings for their venue
Accept/reject booking requests (if manual approval enabled)
View payout history
Respond to disputes.

Admin can

Approve/reject venues
Suspend venues
Moderate disputes
Refund bookings
Release payouts
Review reports
Ban users/owners 
View all system analytics. 

Booking can only be done once. 

Owner cannot book own venue.
 
Users can review only if:

-booking completed
-booking belongs to them
-one review per booking     

Owner → Venue
Admin → Approves Venue

Customer creates booking
Owner approves booking

Payment verified -> Booking confirmed

Booking → Payment
Payment → Owner payout
Admin/System → Releases payout

If disputes exist:
Booking
   ↳ Customer raises dispute
   ↳ Owner responds
   ↳ Admin resolves

```


