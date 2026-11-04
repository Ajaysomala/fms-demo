# FMS Chef module: design analysis (from Figma PDF exports)

Source: `FMS_Customer_and_Vendor_APP__1__1.zip`. Everything below is what the DESIGNS show. It is an expectation, not proof of how the app behaves. Nothing here is a bug.

## 1. What is in the zip

- 160 files, all PDF, one page each. No .fig, no links, no videos. Nothing important is unreadable.
- 47 "Connector line-N" files + "Vector 2463": arrows only, no text. I cannot tell from them which screen links to which (they carry no anchors). Flow order below comes from the screen names, the Frame labels and the arrows I could see on the boards.
- 20 "Frame 21472..." files: label strips (Registration, Home, Booking Combo Packages, My Orders, Filters, Find Home Chef, Booking Custom Dishes, Ceckout [sic], Find Catering Providers, "If the kitchen is closed", "Updated").
- 92 screen or board files. `My Orders`, `Splash/Registeration`, `Profile/Settings`, `Edit Location`, `Order Cancellation`, `Order rate`, `Chat`, `Referred person different screens` are multi-frame boards.
- How I read them: text of all PDFs extracted; about 15 key screens and boards also viewed as images (category, where/when, providers list, kitchen profile, booking option, dishes, combo, quote, order details, checkout and cancellation policy, cancel dialogs, My Orders board). Where text extraction and image disagreed (cancellation policy percentages), the image wins.
- Duplicates: several screens exist twice (name and name-1): Select booking option, Kitchen Profile, Checkout, Success Message, Notifications, Calendar, Cuisines filter, Mobile Dial Input, Service Tiers, Find Chef categories. They look the same unless noted.

## 2. Not stated in the designs

- Role per screen (customer or kitchen/partner). The zip name says "Customer and Vendor", but I found no kitchen-side screen (no screen where the kitchen accepts, rejects or writes a quote). The screens in the Chef flow read like the customer side. TO CONFIRM.
- Which app (Customer or Partner), which build, which environment.
- Device: iOS-style status bar (9:41) everywhere, plus one Android-style time dial ("Mobile Dial Input- if android").
- Who or what triggers each order status change.
- Any API, endpoint, field name, testID.
- Time zone, currency rules (AED is shown), languages in the Chef flow (the registration board shows English, Arabic, Hindi, Urdu and others in the language list; Arabic/RTL screens not provided).

## 3. Screens: what I see (no conclusions)

| Screen (file) | What it shows |
|---|---|
| Splash/Registeration (board) | Language choice (English and others), region choice, phone or email entry, "Enter 4-digit code", "Resend OTP in 60s", "Wrong OTP entered", "Code expired! Resend Code", name entry, "Keep me signed in", "Continue As Guest", "You have to register first / Please sign up or log in to continue / Sign Up", "Almost there!" address step with "Skip". |
| Home New, Home_Guest view, Home_ if no address, Home_ First time, Home_ Welcome message, Home_ On scroll | "Hello, John", address line or "Set your address", "Search Product", category row (Family Care, Auto Parts, Pet Care, Towing, Find Chef), "Top Services" (Auto Parts, Mechanic, Find My Chef), "Popular Services" (Family Care), "Want to Pay Less? Invite a friend and earn 50 AED on your next purchase" + "Invite Friends", welcome card "Welcome to FMS, Your account has been created successfully!" with "Claim Offer", "Complete Profile", "Do it Later". |
| All Services, All Services_ Search result (+ -1) | Grid of services (Auto Parts, Mechanic, Towing, Packers & Movers, Find My Chef, Baby/Elder Care, Home Nursing, Fitness Trainer, Pet Care, Laundry, Accountant, Lawyer). Search "nanny" gives "Baby/Elder Care"; a typo search gives "No Results Fount / Try searching again with a different key word". |
| Search | "Search chef, nanny, nurse,.." , "Search by Category", "Recent Searches" and "Popular Searches" (engine oil, brake pads and similar). |
| Find Chef categories (+ -1) | "Find Chef", "What type of service do you need?", two cards: "Home Chef" and "Catering Services". |
| Find Chef_ Where / Where open (+ -1) | Header "Home Chef" + "Discard". Three collapsed rows: "Where?" (address), "When?", "Ingredients & Cuisines?" and "Next". Open "Where?" shows a saved address "Home" with an edit icon. |
| Find Chef_ When (+ -1), Calendar, Mobile Dial Input | "When?" with "Select Date" (example "16 Sep. 2021") and "Select Time". Calendar "September 2021". Android time dial with "CANCEL / OK". |
| Find Chef_ When is filled, ...Cuisines is open | "When?" shows "26, May- 10:00 AM". "Ingredients & Cuisines?": "Will you provide ingredients?*" with "Yes, I will provide" / "No, Chef provides", "Which cuisines are you looking for?" dropdown (example "Indian food, Halal food"). One of these two frames has the header "Catering Services" instead of "Home Chef". |
| Cuisines, Cuisines filter | List: Indian Food, Halal Food, Russian Food (+ Arab Food in the filter sheet), "Reset", "Show Results". |
| Home chef_ Providers list | Search bar, filter icon, chips "Indian Food, Halal food" and "I'll provide ingredients", cards with tags "Top Rated" and "Providing Ingredients", "30 Km Away", rating 4.8, names "Eaz Chef" and "Chef at Home", "Packages starting price AED 100". |
| Private chef_ Providers list | Same cards. Chips: cuisine, "Price", "Rating". One card tagged "CLOSED". |
| Catering_ Providers list | Same cards. Chips: "Indian Food", "I'll provide ingredients". |
| Filters_ Individual Chef | "Filters / Reset": Cuisine, Availability ("24/7", "Available Now"), Price Range (Min/Max AED 0 to 10000, quick picks "Less than 100/500/1000"), Distance (slider km, "Within 2km/20km/100km"), Ratings (5, 4 & up ... 1 & up), "Show Results". |
| Filters_ Catering | Same plus "Event Type" (Birthday Party, Sohour, Iftar, Graduation), "Service Tier" (Chef only, Chef & Food, Full Service), "Number of Guests" (2-10, 10-20, 20-40, 40-100, 100 & Up). |
| Filter by Price Range | Price filter sheet with "Reset" and "Show Results". |
| Kitchen Profile (+ -1, -2) | Food photo, "Eaz Chef", tag "Providing Ingredients", "All chefs are verified", "4.7 (2 reviews)", "Available", "30 Km Away", "3 Years of Experience", "About Kitchen" text, "Cuisines" chips, (-1 adds "Event Types": Birthday Party, Graduation Party, Iftar), "Customer Reviews 4.7 (156)", "View All Reviews", "Recommended Kitchens", buttons "View Packages" and "Book a Chef". (-2) tagged "CLOSED". |
| Select booking option (+ -1, min & max) | Modal "Select Booking Option": "Custom Dishes - Customize your own menu and quantities" and "Combo Packages - Ready-made meals for easy booking". Behind it a chef card ("Omar Khaled", "AED 30/hr", "About Chef"), button "Book Chef". The min/max variant adds "Min: 5 dishes" and "Max: 20 dishes". |
| Add dishes details (+ -1) | "Book Custom Dishes / Discard", "Add Your Dishes", "Dish 1": "Dish Category*" (Select here), "Dish Name*" (Search your dish), "Add Quantity*" (e.g. 10), "Select Unit*" (e.g. kg), "Note for Chef (optional)" with "0/500 characters", buttons "Add Dish" and "Confirm Request" (-1 has "Add Dish" and "Next"). |
| Add dishes details_ Dish 2 is added (+ -1) | Dish 1 and Dish 2 each with "Remove". Red banner: "Error! You can't add more, Max no. of dishes you can add is 20 dish." |
| The customer will provide the ingredients | Dishes form with banner "Error! Please check the check box below to confirm your request." and checkbox "I will provide the ingredients". |
| Book Combo Packages (variant A) | "Book Combo Packages", "0 Packages Selected", "Family dinner combo AED 299, serves 4-6 people, 5 dishes, ~5 kg", dish list, "Including ingredients", "Most Popular" tag, "Proceed to Checkout". |
| Book Combo Packages_ Packages selected | "2 Packages Selected", per-package "How many of this package?" with minus/plus, "Proceed to Checkout AED 600". |
| Book combo packages (variant B) | "0 Selected", per-person packages: "Essential Package", "Premium Package", "Royal Package" (each AED 299 /Person in this frame), "10% off for 20+ guests", "Add-Ons": Live Stations, Desserts Bar (AED 30/Person), "Next". |
| Book combo packages_ Add special notes | Sheet "Special Notes": "Any special notes for the chef?", "0/500 characters", "Send Notes", "Skip". |
| Book Combo packages_ Packages selected (+ guests reaches offer) | "How many guests?" stepper (12; then 21), "Payment Details" (Essential Package AED 300/Person, Lives Station AED 100/Person, Delivery fees AED 50, No. of Guests 80, Total Amount AED 6000), "Confirm Booking AED 6000". At 21 guests: "You unlocked a 10% group discount!" and Premium shows AED 270. |
| Error message for the min. number of guests | Premium Package card, "How many guests?" 10, red text "Minimum no. of guests is 10". |
| Book Combo Packages_ adding required info (4 variants) | "We want to know more about the event": "What is the event type?*", "Select service tier*" (Food Only / Full Service), "Where will the event happen?*" Indoor/Outdoor (Full Service), "How many guests?*" (min 10), "Note for Chef (optional)", Payment Details, "Proceed to Checkout AED 6000 / 7000", or "Confirm & Request Final Quote" when the customer provides ingredients (with the checkbox). |
| Service Tiers (+ -1) | Food Only ("Prepared in our kitchen and delivered ready to serve"), Food+ Chef ("Chef cooks at your location. No serving staff included."), Full Service ("Food prepared & delivered, setup, serving staff, cleanup"), each with a price per guest. |
| Success Message (5 files) | Green tick. "Your request has been sent successfully! Please wait, The kitchen will review and confirm the final price within 2 hours." / "Your request has been cancelled successfully!" / "Your request has been resent successfully!" |
| Final quote from the kitchen | "Final Quote", "Final Cost" lines (Briany Chicken cost/kg AED 20 x3, Sambosa cost/Piece AED 5 x10, Ingredients cost AED 200.00, Platform fees AED 10.00), "Total Cost AED 305", "Proceed to Checkout", "Cancel Request". |
| Order Details (final quote sent, waiting for customer reply, +1) | "Order Details", order number "ORD-2024-001", "Order Tracking: Waiting for your reply", "Final Cost" block (AC Compressor Replacement AED 450, Gas Refill AED 120, Ingredients cost, Labor Fee, Platform Fee, Total Cost AED 650), "Accept & Pay", "Cancel Request", "Service Request Summary" (Order ID #256589 ...). (-1) adds "Required Ingredients" (Flour 10 kg, Chicken 5 kg, Rice 3 kg ...) and per-person lines. |
| Checkout (4 files) | Payment Method (Master Card, Visa, Apple Pay, Stripe, Cash), Service Request Summary, Kitchen Details, Coupon Code ("Save10", "Apply", "10% off on orders above AED 150", "Copy code: SAVE10"), "Your Wallet Balance" ("Use your cashback on this purchase."), Bill Summary, checkbox "Agree to Our Cancellation Policy", "Pay Now AED ...". Error banner "You should agree to our cancellation policy first." Policy sheet "Find Chef Cancellation Policy" with "I Agree". Result screen "Payment Successful!", "Your order has been confirmed", Order Number, buttons "Go to Home", "Go to My Order". |
| My Orders (board) | Four sections: "Private Chef- Custom Dishes", "Private chef- Combo packages", "Catering- Custom dishes", "Catering- Combo packages", each for "Ingredients provided by chef" and "by customer". List with tabs (Total, Processing, Delivered, Canceled) and order cards; Order Details screens with tracking timeline, banners ("Free Cancellation!", "Cancellation Fee Applies!"), a 4-digit code popup with "Copy Code", "Call Chef / Call Kitchen", "Chat Kitchen", "Report an Issue", "Rate", "Reorder", issue form (type, description, photo upload JPG/PNG up to 5MB), "Photo Received!". |
| Order Cancellation (board) | "Order Cancellation / Discard", "Important Notice!" ("Once cancelled, this order cannot be restored..."), "Reason for Cancel" list, "Describe the Issue", "0/500 characters", refund box "Cancellation Refund AED 89.00" (5-7 business days, confirmation email), "Next", "Confirm Cancelation", success "Cancellation request is placed successfully!". Also an Order Details state "Rejected" with "Kitchen Rejection Reason" (example "Our chefs are busy") and "Cancelled" with "Cancellation Reason". |
| Order rate (board) | Delivered order, "Rate Service", "Rate Kitchen Eaz Chef", "Write a Review (Optional)", "Submit Review", "Thank you for your review!". |
| Chat (board) | Chat with "Louis Gozal", "Online", message bubbles, "Type your message". |
| Notifications (3 files) | "Notifications 1 New", "Mark All As Read", items: cashback "Congrats!", "Back to stock!", "Only 2 days before expire!", "Order Shipped"; acceptance version: "Kitchen approved your request! Kitchen Eaz Chef sent you a quote: 240 AED for your order" + "Review Final Quote", "Your service is just done?" + "View code". Empty state "No Notifications Yet" + "Go Home". |
| Location screens, Edit Location (board), Confirmation message | Map with pin, "Where to get your service?", "Search location", saved address "Office Default", "Add a New Address", "Deliver Here", "Out of delivery area! Sorry, we don't deliver here yet", address form fields, "Save Address", delete dialog "Are you sure you want to delete this? This is your default address", "Yes, Sure", "Cancel". |
| Profile/Settings, Home_ Refer app, Referred person (boards) | General app screens (profile, wishlist, tickets, referral). Not Chef-specific. Not analysed further. |
| Important Note (sticky) | "personal chef has to have place to cook. Catering, fine to have place or work onsite." signed "Naved khan". |

## 4. Flows

Role for every flow: not labelled in the designs. They read like the customer side. Kitchen-side actions are not designed in this zip.

| # | Flow | Screens in order | Buttons and actions | Status | Validation and messages |
|---|---|---|---|---|---|
| F1 | Find Chef | Home -> Find Chef categories -> Where / When / Ingredients & Cuisines -> Providers list (Home / Private / Catering variants) -> Filters | Home Chef or Catering Services; Next; Discard; filter, Reset, Show Results | none shown | "Will you provide ingredients?*" required (asterisk). No message shown if fields are empty. |
| F2 | Kitchen profile and booking option | Providers list -> Kitchen Profile -> Select Booking Option | View Packages, Book a Chef, Custom Dishes, Combo Packages | none | "CLOSED" kitchens exist; what the button does is not shown. "Min: 5 dishes / Max: 20 dishes" when the kitchen sets them. |
| F3 | Custom dishes request | Add Your Dishes (Dish 1..n) -> [Catering: event info] -> Confirm Request / Confirm & Request Final Quote -> Success | Add Dish, Remove, Confirm Request, Discard | Order enters "Waiting for final quote" (order list label) | Max 20 dishes error; checkbox "I will provide the ingredients" required when the customer provides ingredients; "Minimum no. of guests is 10"; note max 500 characters. Success text promises a final price within 2 hours. |
| F4 | Final quote | Notification "Kitchen approved your request!" -> Final Quote (or Order Details "Waiting for your reply") | Review Final Quote, Proceed to Checkout, Accept & Pay, Cancel Request | "Waiting for your reply" | none shown |
| F5 | Combo packages | Book Combo Packages -> select packages (count or guests) -> add-ons -> special notes (Send Notes / Skip) -> event info -> Checkout | plus/minus steppers, Next, Confirm Booking, Proceed to Checkout | none | Min guests 10; 10% group discount at 20+ guests; Indoor/Outdoor only for Full Service. |
| F6 | Checkout and payment | Checkout -> cancellation policy sheet -> Payment Successful | pick method, coupon Apply, wallet Apply, tick policy, Pay Now, I Agree, Go to Home, Go to My Order | After payment: order confirmed (label not stated; list later shows Pending/Processing) | "You should agree to our cancellation policy first." |
| F7 | My Orders and tracking | My Orders -> Order Details | tabs, Call Chef/Kitchen, Chat Kitchen, Copy Code, Report an Issue, Reorder | Labels seen: Waiting for final quote, Waiting for your reply, Pending, Processing, Delivered, Completed, Canceled/Cancelled, Rejected. Timeline steps: Order Placed, Order Accepted, Order Confirmed, Chef on the way, Arrived, Service completed (also Order Shipped, Out for Delivery, Delivered in some frames). Trigger for each: not shown. | Banner "Free Cancellation!" (48-hour window) then "Cancellation Fee Applies!" (10%). Code text: "Please share your OTP with the chef/kitchen only after your service is completed successfully." |
| F8 | Cancel | (a) Cancel Request -> dialog -> success. (b) Cancel Order -> Order Cancellation -> reason -> refund -> Confirm Cancelation -> success. (c) "Cancel Booking?" dialogs with "Keep Booking". | Yes, Cancel / No, Continue; Next; Confirm Cancelation | Cancelled; Rejected (by kitchen, reason shown) | Policy tiers (from the image): over 48h 100% refund; 24-48h 90% refund, 10% charge; 12-24h 75% refund, 25% charge; under 12h 50% refund, 50% charge; same day / after start no refund, 100% charge. |
| F9 | Rate and report | Order Details (Delivered/Completed) -> rate -> review; Report an Issue | stars, Submit Review, Submit Issue | Completed | Review optional, 500 characters; photo JPG/PNG up to 5MB. |
| F10 | Notifications | Notifications list / empty state | Mark All As Read, Review Final Quote, View code, Go Home | none | none |
| F11 | Address | Location, Edit Location | Deliver Here, Save Address, Make as Default, delete confirm | none | "Out of delivery area! Sorry, we don't deliver here yet". |

## 5. Output A: flow map

| Flow | Screens in order | Actions | States | Role |
|---|---|---|---|---|
| F1 Find Chef | Home, Find Chef categories, Where/When/Ingredients, Providers list, Filters | Pick Home Chef or Catering; set address, date, time, ingredients, cuisines; Next; filter | none | Not stated (customer-like) |
| F2 Kitchen and option | Providers list, Kitchen Profile, Select Booking Option | View Packages, Book a Chef, Custom Dishes, Combo Packages | CLOSED tag | Not stated |
| F3 Custom dishes | Add Your Dishes, event info (catering), Success | Add Dish, Remove, Confirm Request, Discard | Waiting for final quote | Not stated |
| F4 Final quote | Notification, Final Quote / Order Details | Review Final Quote, Accept & Pay, Proceed to Checkout, Cancel Request | Waiting for your reply | Not stated |
| F5 Combo packages | Book Combo Packages, notes sheet, event info | Select, steppers, add-ons, Send Notes/Skip, Proceed to Checkout | none | Not stated |
| F6 Checkout | Checkout, policy sheet, Payment Successful | Method, coupon, wallet, I Agree, Pay Now | order confirmed | Not stated |
| F7 My Orders | My Orders, Order Details | tabs, Call/Chat, Copy Code | Pending, Processing, Delivered, Completed, Canceled, Rejected | Not stated |
| F8 Cancel | Cancel dialogs, Order Cancellation | Yes, Cancel; Confirm Cancelation | Cancelled, Rejected | Not stated |
| F9 Rate/Report | Order Details, rate, issue form | Submit Review, Report an Issue | Completed | Not stated |

## 6. Output B: test cases

Layer: API / UI / Manual. "Expected" is the design expectation. "to confirm" means the design does not say.

| ID | Case | Steps | Expected (from the design) | Layer | Automate |
|---|---|---|---|---|---|
| CHEF-001 | Category screen | Open Find Chef | Title "Find Chef", "What type of service do you need?", cards "Home Chef" and "Catering Services" | UI | yes |
| CHEF-002 | Home Chef opens request form | Tap Home Chef | Rows "Where?", "When?", "Ingredients & Cuisines?", "Next" | UI | yes |
| CHEF-003 | Saved address is prefilled | Open Where with a saved address | Address shown (design: "Home", "Dubai, Business Bay, Tower A, A...") with edit icon | UI | yes (data TODO) |
| CHEF-004 | Next with empty fields | Tap Next with nothing filled | Not shown (to confirm) | Manual | no |
| CHEF-005 | Date and time | Open When, pick date and time | Row shows picked value (design example "26, May- 10:00 AM") | UI | partly (native pickers) |
| CHEF-006 | Ingredients choice | Pick "Yes, I will provide" then "No, Chef provides" | One option selected at a time; question marked required (*) | UI | yes |
| CHEF-007 | Cuisines select | Open cuisines, pick two | Row shows chosen cuisines (design: "Indian food, Halal food") | UI | yes |
| CHEF-008 | Discard | Tap Discard | Leaves the form (what happens to the data: to confirm) | Manual | no |
| CHEF-009 | Providers list | Tap Next | Cards with name, "30 Km Away", rating, "Packages starting price", tags "Top Rated" / "Providing Ingredients" | UI | yes |
| CHEF-010 | Provider search results match request | Compare list with cuisine and ingredient choices | Chips on the list reflect the choice (design: "Indian Food, Halal food", "I'll provide ingredients") | API | yes (needs endpoint from Swagger) |
| CHEF-011 | Filters, individual chef | Open filters, set price, distance, rating, Show Results | Filters: Cuisine, Availability, Price Range, Distance, Ratings. "Reset" clears | UI + API | yes |
| CHEF-012 | Filters, catering | Open filters in Catering | Adds Event Type, Service Tier, Number of Guests | UI + API | yes |
| CHEF-013 | Closed kitchen | Open a "CLOSED" kitchen | Tag "CLOSED" visible; booking behaviour: to confirm | Manual | no |
| CHEF-014 | Kitchen profile | Open a kitchen | Name, rating, "All chefs are verified", "Available", distance, experience, cuisines, reviews, "View Packages", "Book a Chef" | UI | yes |
| CHEF-015 | Booking option modal | Tap Book a Chef | "Select Booking Option" with "Custom Dishes" and "Combo Packages" | UI | yes |
| CHEF-016 | Min/max dishes info | Open a kitchen that sets limits | Shows "Min: 5 dishes", "Max: 20 dishes" | UI + API | yes |
| CHEF-017 | Required dish fields | Open Custom Dishes | Fields marked required: Dish Category, Dish Name, Add Quantity, Select Unit | UI | yes |
| CHEF-018 | Add and remove dish | Tap Add Dish; tap Remove | Dish 2 appears with Remove; removing returns to one dish | UI | yes |
| CHEF-019 | Max 20 dishes | Add dishes until the limit | Banner "You can't add more, Max no. of dishes you can add is 20 dish." | UI | yes |
| CHEF-020 | Below minimum dishes | Confirm with fewer than the kitchen minimum | Not shown (to confirm) | Manual | no |
| CHEF-021 | Note length | Type in Note for Chef | Counter "0/500 characters"; limit 500 | UI | yes |
| CHEF-022 | Send custom request | Fill valid dishes, Confirm Request | "Your request has been sent successfully!" and "...confirm the final price within 2 hours."; order shows "Waiting for final quote" | UI + API | yes |
| CHEF-023 | Customer-provided ingredients checkbox | Choose "Yes, I will provide", do not tick, Confirm | Banner "Please check the check box below to confirm your request." | UI | yes |
| CHEF-024 | Minimum guests | Set guests below 10 (catering) | "Minimum no. of guests is 10" | UI | yes |
| CHEF-025 | Combo list and counter | Open Combo Packages, select 2 | Counter changes ("0 Packages Selected" -> "2 Packages Selected") | UI | yes |
| CHEF-026 | Package quantity | Change "How many of this package?" | Total updates | UI + API | yes |
| CHEF-027 | Group discount | Set guests 21 on a per-person package | "You unlocked a 10% group discount!", price per person lower (design 300 -> 270) | UI + API | yes |
| CHEF-028 | Add-ons | Select an add-on | Add-on line appears in Payment Details | UI | yes |
| CHEF-029 | Special notes sheet | Open notes | "Any special notes for the chef?", "Send Notes", "Skip", 500 characters | UI | yes |
| CHEF-030 | Event info required | Leave event type empty, proceed | Not shown (to confirm); fields marked required | Manual | no |
| CHEF-031 | Indoor/Outdoor only for Full Service | Switch tier | "Where will the event happen?*" appears only for Full Service | UI | yes |
| CHEF-032 | Combo price math | Create a combo booking | Total equals line items (design amounts do not reconcile, see Output C) | API | yes, after formula is confirmed |
| CHEF-033 | Final quote view | Open the quote | Lines, "Total Cost", "Proceed to Checkout", "Cancel Request" | UI | yes (needs a quote) |
| CHEF-034 | Quote math | Open a quote | Total equals the sum of lines (design amounts do not reconcile) | API | yes, after formula is confirmed |
| CHEF-035 | Pay without agreeing to policy | Tap Pay Now unticked | "You should agree to our cancellation policy first." | UI | yes |
| CHEF-036 | Cancellation policy sheet | Tap the policy link | Five tiers: 100% / 90% / 75% / 50% / 0% refund; "I Agree" | UI | yes |
| CHEF-037 | Pay with card | Agree, Pay Now (staging test card) | "Payment Successful!", "Your order has been confirmed", Order Number, "Go to Home", "Go to My Order" | UI + API | yes |
| CHEF-038 | Coupon | Apply "Save10" | Total reduced; rule "10% off on orders above AED 150" (below 150: to confirm) | UI + API | yes after rules confirmed |
| CHEF-039 | Wallet balance | Apply wallet | Cashback used reduces total | UI + API | yes after rules confirmed |
| CHEF-040 | My Orders tabs | Open My Orders | Tabs Total, Processing, Delivered, Canceled with counts | UI | yes |
| CHEF-041 | Status after quote | Kitchen sends a quote | Order shows "Waiting for your reply"; "Accept & Pay" and "Cancel Request" | API + UI | needs partner side or seed |
| CHEF-042 | Status timeline | Move order forward | Timeline steps in order (Order Placed, Order Accepted, ... Service completed); who triggers: to confirm | API + UI | needs partner side |
| CHEF-043 | Completion code | Open the code popup | 4-digit code, "Copy Code", warning to share only after the service | Manual | no |
| CHEF-044 | Call and chat | Tap Call Chef / Chat Kitchen | Opens phone or chat | Manual | no |
| CHEF-045 | Cancel before quote | Cancel Request | Dialog "Are you sure you want to cancel your request?" -> "Your request has been cancelled successfully!" | UI + API | yes |
| CHEF-046 | Cancel paid order | Cancel Order, reason, Confirm Cancelation | Refund box, then "Cancellation request is placed successfully!" | UI + API | yes |
| CHEF-047 | Refund by policy | Cancel at different times to the event | Refund follows the tiers in CHEF-036 | API | yes after amounts confirmed |
| CHEF-048 | Kitchen rejects | Kitchen rejects | "Rejected" with "Kitchen Rejection Reason" | API + UI | needs partner side |
| CHEF-049 | Rate order | Rate service and kitchen, Submit Review | "Thank you for your review!"; review optional, 500 chars | UI + API | yes |
| CHEF-050 | Report an issue | Choose type, describe, upload JPG/PNG | "Photo Received!"; 5MB limit | Manual | no |
| CHEF-051 | Notifications | Open list; empty state | Items listed; "Mark All As Read"; empty "No Notifications Yet" + "Go Home" | UI | yes |
| CHEF-052 | Push for quote | Kitchen sends quote | Push and notification "Kitchen approved your request!" | Manual | no |
| CHEF-053 | Guest user | Continue As Guest, try to book | "You have to register first / Please sign up or log in to continue." (frame placement: to confirm) | UI | yes after confirmed |
| CHEF-054 | Out of delivery area | Pick address outside area | "Out of delivery area! Sorry, we don't deliver here yet" | UI + API | yes |
| CHEF-055 | Arabic / RTL | Switch language | Layout and text mirror | Manual | no |

## 7. Output C: questions for the team (not bugs)

**Placeholder text and wording from other services**
1. Kitchen Profile "About Kitchen" and Select Booking Option "About Chef" show motor-oil text ("This premium synthetic motor oil is engineered...").
2. Kitchen Profile review shows "Verified Purchase" and "My engine runs smoother than ever. Highly recommended for Toyota vehicles."
3. Order Details final cost lists "AC Compressor Replacement" and "Gas Refill"; Order rate shows "Mechanic on the way" and "Brake Pad Replacement"; My Orders shows "Premium Engine Oil, Size: 1 L, Arrives by Fri, Dec 19".
4. "Note for Chef" is "Figma ipsum component variant main layer..." in every summary. Placeholder?
5. Delivery wording in a service order: "Order Shipped", "Out for Delivery", "Your order is shipped on 11 Dec", "Take a Photo on Delivery", "Just received your order?", "Back to stock!", "Delivery fees AED 50", "Delivery Address".
6. Chef naming: "Home Chef", "Private Chef", "Individual Chef", "personal chef" (sticky note). One name, or different services?
7. Home screen says "Find Chef" in the category row and "Find My Chef" in Top Services and All Services. Search categories shows "Find Che".
8. Providers cards: second card is named "Chef at Home". Is that a kitchen name or a tag?

**Amounts that do not add up (from what is shown)**
9. Final quote: 20 x 3 + 5 x 10 + 200 + 10 = 320. Design total: 305.
10. Order Details quote: 450 + 120 + 80 + 80 + 80 = 810. Design total: 650.
11. Catering quote: three lines of 200.00/Person + Full Service fee 5/Person, 10 guests, platform 10. Design total: 305. Also "Total No. of Guests x10" while the summary says "No. of Guests 30".
12. Combo bill: Essential 300/Person + Live Station 100/Person (+ Bar 100) + Full Service 5/Person, 80 guests, platform fee 10. Design total 6000 (Food Only) and 7000 (Full Service). A difference of 1000, while the service fee at 5/Person x 80 is 400.
13. Guest count shows 12 or 21 in the stepper, 80 in Payment Details, 15 in the order summary.
14. Add-ons list AED 30/Person, but the bill shows "Lives Station AED 100/Person" and "Bar AED 100/Person".
15. Checkout-3: Family dinner combo "cost 200 x5" + Lunch combo "200 x2" = 1400. Bill total AED 6010. Pay Now AED 6000.
16. Combo list: 2 selected at AED 299 shows "Proceed to Checkout AED 600" (598?). Package cards also show a second price "AED 120" without a label. All three per-person packages show AED 299 in one frame, Premium shows AED 300 in another.
17. Payment Successful shows "Total Amount AED 107.45" while Pay Now was AED 305 (or 6000).
18. Notification says the quote is "240 AED". Final Quote screen shows 305, order details 650.
19. Cancellation Refund AED 89.00 for an order total of AED 450.00 is about 20 percent. It matches none of the policy tiers (100, 90, 75, 50, 0 percent).
20. Policy tiers: banner on My Orders says "A 10% cancellation fee will apply" inside 48 hours, matching the 24-48h tier. What about the 12-24h and under-12h tiers on the banner? Also the "Cancel Booking?" dialog mentions a full refund "until August 20, 8:30 PM", which is an absolute date, not "48 hours".

**Identifiers and dates**
21. Three order identifiers: "ORD-2024-001" (header), "#256589" (Order ID), "#FMS4722" (Order Number after payment). Which one is shown, and are they the same thing?
22. Calendar header reads "SAN MON TUE ..." and September 2021 shows day 31. Example dates are 2021 and 2024 and 2026 (reviews dated Dec 2025).
23. Date format differs: "16 Sep. 2021 9:00 PM" vs "26, May- 10:00 AM".

**Missing states (not in the designs)**
24. No kitchen-side screens: accept request, reject, write the final quote, mark arrived, complete. Are they in another file?
25. What happens when the kitchen does not answer in 2 hours? Quote expiry? Customer declines the quote (Cancel Request vs reject)?
26. Closed kitchen: can the customer still book? What does "Book a Chef" do?
27. Empty providers list, no packages for a kitchen, no kitchens for the chosen cuisines.
28. Validation when "Next" is tapped with empty Where/When/Ingredients. Past dates, lead time before the event.
29. Payment failure or cancelled payment. Cash method: does it skip Stripe? How is card entered?
30. Under minimum dishes (Min: 5) error text. Minimum guests error is shown only for 10; filters offer "2-10".
31. Guest: which actions require login? The "You have to register first" frame sits on the registration board without a trigger.
32. Completion: who enters the 4-digit code (the kitchen app)? One code per order?
33. Status names differ: "Canceled" (tab) vs "Cancelled" (order); "Completed" vs "Delivered"; "Processing" vs "Pending". Single list please.
34. The mixed headers: the "Find Chef_ When is filled" frame has the header "Catering Services" in a Home Chef flow. Catering flow also shows "Where? Home". Which is right?
35. "Important Note": a personal chef needs a place to cook; catering can be onsite. Is that checked in the app (address type, kitchen at home), and where does the customer see it?
36. Order cancellation reasons list shows "Compatibility Issue" repeated. Real reasons?
37. Typos in design texts we would assert on: "Confirm Cancelation", "dish" in "20 dish", "Ceckout", "No Results Fount", "Briany", "Lives Station", "Service Tire". Fix in app or keep?
38. Time of 2 hours for the final price: fixed rule or per kitchen?
39. Payment methods: Master Card, Visa, Apple Pay, Stripe, Cash. Are all live on staging?

## 8. Output D

Seven DRAFT Maestro flows are in `flows/`: `chef_01_find_chef.yaml`, `chef_02_custom_dishes.yaml`, `chef_03_combo_package.yaml`, `chef_04_final_quote_pay.yaml`, `chef_05_cancel_before_quote.yaml`, `chef_06_cancel_order.yaml`, `chef_07_rate_order.yaml`. Only design texts are used. Login, navigation and data are marked TODO. Each flow ends with `assertVisible`.
