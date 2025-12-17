from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from services.crop_advisor import recommend_crops
from services.weather_risk import get_mock_weather_and_risk
from services.soil_fertilizer import calculate_fertilizer
from services.market_intel import get_best_market
from services.irrigation import plan_irrigation
from services.schemes import get_schemes_for_farmer
from services.pest_diagnosis import diagnose_pest_mock
from services.growth_prediction import predict_growth

app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-production"


# Static descriptions for key schemes shown on the home page
SCHEME_DETAILS = {
    "pm-kisan": {
        "code": "pm-kisan",
        "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "tagline": "Direct income support from Central Government",
        "summary": (
            "PM-KISAN provides an income support of ₹ 6,000 per year to all eligible "
            "small and marginal farmer families across India, paid in three equal instalments "
            "directly to the farmer's bank account."
        ),
        "benefits": [
            "₹ 2,000 is transferred three times a year to the farmer's bank account.",
            "Helps farmers manage input costs for seeds, fertilizers and small expenses.",
            "Money is sent directly (DBT) without middlemen.",
        ],
        "eligibility": [
            "Farmer families owning cultivable land as per state land records.",
            "Certain higher-income and institutional categories are excluded.",
            "Land ownership details must be updated and verified by local officials.",
        ],
        "how_to_apply": [
            "Visit your local Krishi Bhavan or village agriculture office.",
            "Carry Aadhaar card, bank passbook and land ownership documents.",
            "You can also register and check status on the official PM-KISAN portal.",
        ],
        "note": "For latest rules, always confirm with your local agriculture office or the PM-KISAN website.",
    },
    "karshaka-insurance": {
        "code": "karshaka-insurance",
        "title": "Karshaka Insurance Scheme (Kerala)",
        "tagline": "State-level crop insurance for Kerala farmers",
        "summary": (
            "Karshaka Insurance Scheme gives financial protection to registered Kerala farmers "
            "when crops are damaged due to flood, drought, pests, diseases or other natural calamities."
        ),
        "benefits": [
            "Compensation for crop loss due to notified natural calamities.",
            "Encourages farmers to continue cultivation without fear of total loss.",
            "Premium is partially supported by the Government of Kerala.",
        ],
        "eligibility": [
            "Farmer must be registered with the Kerala agriculture department.",
            "Crops and area should be enrolled under the scheme for the season.",
            "Timely premium payment and accurate crop details are required.",
        ],
        "how_to_apply": [
            "Contact your local Krishi Bhavan or agriculture officer.",
            "Fill the enrolment form with crop, area and season details.",
            "Submit any documents requested and pay the required premium, if applicable.",
        ],
        "note": "Compensation and coverage may change every year, so always check the latest circular from the department.",
    },
    "pm-kusum": {
        "code": "pm-kusum",
        "title": "PM-KUSUM / Solar Pump Support",
        "tagline": "Support for solar pumps and small solar plants",
        "summary": (
            "PM-KUSUM aims to promote the use of solar energy in agriculture by helping farmers "
            "install solar pumps and small solar power plants, reducing electricity cost for irrigation."
        ),
        "benefits": [
            "Subsidy on installation of solar-powered irrigation pumps.",
            "Less dependence on grid electricity and diesel.",
            "Surplus power from certain components can be sold to the grid (as per scheme rules).",
        ],
        "eligibility": [
            "Individual farmers and groups of farmers as per scheme guidelines.",
            "Land and location must be suitable for installing solar equipment.",
            "Additional conditions may be set by the state nodal agency (such as KSEB in Kerala).",
        ],
        "how_to_apply": [
            "Check notifications from the state nodal agency (for example, KSEB / ANERT in Kerala).",
            "Submit an application when registrations are open, with land and identity details.",
            "Work with approved vendors for installation once your application is sanctioned.",
        ],
        "note": "Subsidy percentage and components under PM-KUSUM can change; always refer to the latest official guidelines.",
    },
}


# Very simple in-memory farm diary store for demo
FARM_DIARY_ENTRIES = []

# In-memory community posts storage
COMMUNITY_POSTS = []
COMMUNITY_POST_ID = 0


def _is_strong_password(pw: str) -> bool:
    """Check that password has letters, digits and special characters."""
    if not pw:
        return False
    has_letter = any(c.isalpha() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(not c.isalnum() for c in pw)
    return has_letter and has_digit and has_special


@app.before_request
def require_login():
    """Force login before accessing any page, except login and static files."""
    # Some endpoints (like static files) should not be blocked
    exempt_endpoints = {"login_view", "logout_view", "static"}
    # request.endpoint can be None for some special cases
    if request.endpoint in exempt_endpoints or request.endpoint is None:
        return
    if "username" not in session:
        return redirect(url_for("login_view"))


@app.route("/")
def index():
    # If user is not logged in, send them to the login page first
    if "username" not in session:
        return redirect(url_for("login_view"))
    return render_template("index.html")


@app.route("/crop-advisor", methods=["GET", "POST"])
def crop_advisor_view():
    result = None
    submitted = False
    if request.method == "POST":
        submitted = True
        soil_type = request.form["soil_type"]
        land_size = float(request.form["land_size"])
        district = request.form["district"]
        season = request.form["season"]
        result = recommend_crops(soil_type, land_size, district, season)
    return render_template("crop_advisor.html", result=result, submitted=submitted)


@app.route("/weather", methods=["GET", "POST"])
def weather_view():
    alerts = None
    submitted = False
    if request.method == "POST":
        submitted = True
        district = request.form["district"]
        crop = request.form["crop"]
        alerts = get_mock_weather_and_risk(district, crop)
    return render_template("weather.html", alerts=alerts, submitted=submitted)


@app.route("/soil", methods=["GET", "POST"])
def soil_view():
    plan = None
    if request.method == "POST":
        crop = request.form["crop"]
        om = request.form["organic_matter"]
        land = float(request.form["land_size"])
        plan = calculate_fertilizer(crop, om, land)
    return render_template("soil.html", plan=plan)


@app.route("/market", methods=["GET", "POST"])
def market_view():
    markets = None
    if request.method == "POST":
        crop = request.form["crop"]
        district = request.form["district"]
        markets = get_best_market(crop, district)
    return render_template("market.html", markets=markets)


@app.route("/irrigation", methods=["GET", "POST"])
def irrigation_view():
    plan = None
    if request.method == "POST":
        crop = request.form["crop"]
        stage = request.form["stage"]
        soil_type = request.form["soil_type"]
        rain = request.form["rain_chance"]
        plan = plan_irrigation(crop, stage, soil_type, rain)
    return render_template("irrigation.html", plan=plan)


@app.route("/schemes", methods=["GET", "POST"])
def schemes_view():
    schemes = None
    if request.method == "POST":
        land = float(request.form["land_size"])
        # Show schemes only for valid land size (0.1 acre and above)
        if land >= 0.1:
            is_small = land <= 2
            schemes = get_schemes_for_farmer(land, is_small)
    return render_template("schemes.html", schemes=schemes)


@app.route("/pest", methods=["GET", "POST"])
def pest_view():
    diagnosis = None
    if request.method == "POST":
        crop = request.form.get("crop", "").strip()
        # Symptoms text box has been removed from the UI; we
        # keep this parameter for compatibility but default to empty.
        symptoms = request.form.get("symptoms", "")
        diagnosis = diagnose_pest_mock(crop, symptoms)
    return render_template("pest.html", diagnosis=diagnosis)


@app.route("/voice-assistant")
def voice_assistant_view():
    """Render a simple voice assistant UI. The actual speech recognition and
    speech synthesis are handled on the browser side using JavaScript.
    """
    return render_template("voice_assistant.html")


@app.route("/growth", methods=["GET", "POST"])
def growth_view():
    prediction = None
    if request.method == "POST":
        crop = request.form["crop"].strip()
        land = float(request.form["land_size"])
        if land >= 0.1:
            prediction = predict_growth(crop, land)
    return render_template("growth.html", prediction=prediction)


@app.route("/farm-diary", methods=["GET", "POST"])
def farm_diary_view():
    """Simple farm diary / digital notebook.

    Farmers can record key activities like seed purchase, fertilizer usage,
    pesticide application and irrigation schedule. Entries are stored only
    in memory for this demo (they reset when the server restarts).
    """
    if request.method == "POST":
        entry = {
            "date": request.form.get("date", "").strip(),
            "crop": request.form.get("crop", "").strip(),
            "seed": request.form.get("seed", "").strip(),
            "fertilizer": request.form.get("fertilizer", "").strip(),
            "pesticide": request.form.get("pesticide", "").strip(),
            "irrigation": request.form.get("irrigation", "").strip(),
        }
        # Only add if something meaningful was entered
        if any(entry.values()):
            FARM_DIARY_ENTRIES.insert(0, entry)
            # keep only recent 10 for display
            del FARM_DIARY_ENTRIES[10:]
    return render_template("farm_diary.html", entries=FARM_DIARY_ENTRIES)


@app.route("/scheme/<code>")
def scheme_detail_view(code: str):
    """Show a full explanation page for an important scheme.

    Used when the user clicks a scheme card on the home page.
    """
    scheme = SCHEME_DETAILS.get(code)
    if not scheme:
        abort(404)
    return render_template("scheme_detail.html", scheme=scheme)


@app.route("/login", methods=["GET", "POST"])
def login_view():
    """Very simple demo login page.

    Phone: 10-digit farmer phone number.
    Password: must include letters, numbers and special characters.
    """
    error = None
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "").strip()

        if not phone:
            error = "Please enter your phone number."
        elif not (phone.isdigit() and len(phone) == 10):
            error = "Phone number must be exactly 10 digits."
        elif not _is_strong_password(password):
            error = "Password must include letters, numbers and special characters."
        else:
            # Store phone number in session for greeting
            session["username"] = phone
            flash("Logged in successfully.")
            return redirect(url_for("index"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout_view():
    """Clear the session and send user back to the login page."""
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for("login_view"))


@app.route("/community", methods=["GET", "POST"])
def community_view():
    """Farmer Knowledge-Sharing Community - share problems, photos, and solutions."""
    global COMMUNITY_POST_ID
    
    if request.method == "POST":
        action = request.form.get("action", "")
        
        if action == "new_post":
            # Create a new post
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()
            category = request.form.get("category", "general")
            image_url = request.form.get("image_url", "").strip()
            
            if title and content:
                COMMUNITY_POST_ID += 1
                post = {
                    "id": COMMUNITY_POST_ID,
                    "author": session.get("username", "Anonymous"),
                    "title": title,
                    "content": content,
                    "category": category,
                    "image_url": image_url if image_url else None,
                    "likes": 0,
                    "liked_by": [],
                    "comments": [],
                    "timestamp": "Just now"
                }
                COMMUNITY_POSTS.insert(0, post)  # Add to beginning
                flash("Your post has been shared with the community!")
        
        elif action == "add_comment":
            post_id = int(request.form.get("post_id", 0))
            comment_text = request.form.get("comment_text", "").strip()
            
            if comment_text:
                for post in COMMUNITY_POSTS:
                    if post["id"] == post_id:
                        post["comments"].append({
                            "author": session.get("username", "Anonymous"),
                            "text": comment_text,
                            "timestamp": "Just now"
                        })
                        break
        
        elif action == "like_post":
            post_id = int(request.form.get("post_id", 0))
            user = session.get("username", "Anonymous")
            
            for post in COMMUNITY_POSTS:
                if post["id"] == post_id:
                    if user not in post["liked_by"]:
                        post["likes"] += 1
                        post["liked_by"].append(user)
                    break
        
        elif action == "delete_post":
            post_id = int(request.form.get("post_id", 0))
            user = session.get("username", "Anonymous")
            
            for i, post in enumerate(COMMUNITY_POSTS):
                if post["id"] == post_id and post["author"] == user:
                    COMMUNITY_POSTS.pop(i)
                    flash("Your post has been deleted.")
                    break
        
        elif action == "delete_comment":
            post_id = int(request.form.get("post_id", 0))
            comment_index = int(request.form.get("comment_index", -1))
            user = session.get("username", "Anonymous")
            
            for post in COMMUNITY_POSTS:
                if post["id"] == post_id:
                    if 0 <= comment_index < len(post["comments"]):
                        if post["comments"][comment_index]["author"] == user:
                            post["comments"].pop(comment_index)
                            flash("Your comment has been deleted.")
                    break
        
        return redirect(url_for("community_view"))
    
    # Filter by category if provided
    category_filter = request.args.get("category", "all")
    if category_filter == "all":
        filtered_posts = COMMUNITY_POSTS
    else:
        filtered_posts = [p for p in COMMUNITY_POSTS if p["category"] == category_filter]
    
    return render_template("community.html", posts=filtered_posts, current_category=category_filter)


if __name__ == "__main__":
    app.run(debug=True)
