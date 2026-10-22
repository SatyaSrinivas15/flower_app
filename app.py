import streamlit as st
from PIL import Image
from datetime import datetime
import random
import hashlib
import io

st.set_page_config(
    page_title="FlowerCare AI",
    page_icon="🌸",
    layout="wide"
)

# ---------------- SESSION STATE INITIALIZATION ----------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "image" not in st.session_state:
    st.session_state.image = None

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_disease" not in st.session_state:
    st.session_state.selected_disease = None

if "active_organic_context" not in st.session_state:
    st.session_state.active_organic_context = None

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0


def navigate(page):
    st.session_state.page = page


def reset_scan():
    st.session_state.image = None
    st.session_state.uploader_key += 1
    navigate("Scan Plant")


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

.stApp {
    background: #f7faf7;
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 {
    color: #185c37;
}

div.stButton > button {
    border-radius: 12px;
    border: 1px solid #d7eadb;
    min-height: 42px;
    font-weight: 600;
}

div.stButton > button:hover {
    border-color: #26834c;
    color: #26834c;
}

.plant-card {
    background: white;
    border: 1px solid #deeadf;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}

.hero {
    background: linear-gradient(120deg, #dff4e2, #ffffff);
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #d5e9d8;
    margin-bottom: 24px;
}

.muted {
    color: #63776a;
}
</style>
""", unsafe_allow_html=True)


# ---------------- PLANT & DISEASE DATABASE ----------------

plants = {
    "Rose": "🌹",
    "Hibiscus": "🌺",
    "Marigold": "🌼",
    "Sunflower": "🌻",
    "Jasmine": "🌸",
    "Tulip": "🌷",
    "Chrysanthemum": "💮",
    "Gerbera": "🌼",
    "Lotus": "🪷"
}

disease_data = {
    "Rose": {
        "Black Spot": {
            "description": "A common fungal disease causing dark spots and premature leaf drop.",
            "symptoms": [
                "Dark circular spots with fringed edges on leaf tops",
                "Yellow halos developing around black lesions",
                "Premature leaf drop from the bottom upward"
            ],
            "organic": [
                "Prune and dispose of all infected leaves and fallen debris.",
                "Water directly at the base/soil; keep foliage dry.",
                "Ensure generous airflow and prune overcrowded canes.",
                "Apply organic neem oil spray or potassium bicarbonate solution early morning."
            ]
        },
        "Powdery Mildew": {
            "description": "Fungal growth appearing as white powder on new shoots and leaves.",
            "symptoms": [
                "White powdery fungal coating on leaves and stems",
                "Distorted, blistered, or curled young foliage",
                "Stunted bud and blossom development"
            ],
            "organic": [
                "Prune heavily infected shoots and leaf tips.",
                "Provide at least 6 hours of full direct sunlight.",
                "Spray with a diluted milk-water solution (1:9 ratio) in morning sun.",
                "Avoid excessive high-nitrogen fertilizers that produce vulnerable tender growth."
            ]
        }
    },
    "Hibiscus": {
        "Leaf Spot": {
            "description": "Bacterial or fungal pathogen causing necrotic spots on leaves.",
            "symptoms": [
                "Brown or black spots with yellow halos",
                "Leaves turning pale yellow and dropping prematurely",
                "Reduced blooming frequency"
            ],
            "organic": [
                "Pick off damaged leaves and clean the bed underneath.",
                "Avoid overhead irrigation or evening watering.",
                "Sterilize pruning shears between cuts with 70% alcohol.",
                "Apply copper-based organic fungicide if spots proliferate."
            ]
        }
    },
    "Marigold": {
        "Leaf Blight": {
            "description": "Alternaria fungus causing brownish concentric rings and foliage rot.",
            "symptoms": [
                "Small brown circular spots expanding into lesions",
                "Browning and crisping of lower leaves",
                "Flower buds turning brown and decaying"
            ],
            "organic": [
                "Remove and discard all affected leaves and spent blooms.",
                "Ensure plants are spaced at least 20-30 cm apart.",
                "Mulch base lightly to prevent soil spores from splashing onto foliage.",
                "Spray diluted neem oil during early onset."
            ]
        }
    },
    "Sunflower": {
        "Rust": {
            "description": "Fungal infection causing powdery rust-colored pustules on leaves.",
            "symptoms": [
                "Yellow chlorotic spots on upper leaf surfaces",
                "Reddish-brown raised pustules on the leaf undersides",
                "Foliage drying up and turning brittle"
            ],
            "organic": [
                "Gently remove heavily rusted leaves early before spores spread.",
                "Avoid sprinkling water across the leaves.",
                "Dust lightly with sulfur powder or spray wettable sulfur solution.",
                "Clear plant residues completely at the end of the season."
            ]
        }
    },
    "Jasmine": {
        "Powdery Mildew": {
            "description": "Fungal coating causing leaves and flower buds to look frosted.",
            "symptoms": [
                "White talcum-like powder on leaves and unopened buds",
                "Curling, deformed leaf tips",
                "Premature dropping of fragrant flower buds"
            ],
            "organic": [
                "Improve air circulation through gentle center thinning.",
                "Spray baking soda mixture (1 tsp baking soda + 1/2 tsp vegetable oil in 1L water).",
                "Move potted plants to a warmer, brighter spot with morning sun.",
                "Water early in the morning so moisture evaporates quickly."
            ]
        }
    },
    "Tulip": {
        "Tulip Fire (Botrytis tulipae)": {
            "description": "A severe fungal blight that spots and rots tulip flowers and foliage.",
            "symptoms": [
                "Small sunken brown spots with water-soaked margins",
                "Foliage and blooms looking burnt or scorched",
                "Gray fuzzy mold appearing in damp weather"
            ],
            "organic": [
                "Dig up and discard severely infected bulbs immediately to protect others.",
                "Do not compost infected foliage.",
                "Ensure fast-draining, sandy-loam soil.",
                "Rotate planting beds so tulips aren't grown in the same soil consecutively."
            ]
        }
    },
    "Chrysanthemum": {
        "Septoria Leaf Spot": {
            "description": "A fungal disease causing dark circular lesions from lower leaves upward.",
            "symptoms": [
                "Dark brown spots that coalesce into large dead patches",
                "Lower foliage shriveling and clinging to the stem",
                "Stunted floral growth"
            ],
            "organic": [
                "Strip off lower affected foliage up to 10 cm above ground level.",
                "Always water the soil base without wetting upper foliage.",
                "Apply organic copper fungicide or sulfur spray if conditions are humid.",
                "Ensure adequate spacing to keep humidity down."
            ]
        }
    },
    "Gerbera": {
        "Powdery Mildew & Crown Rot": {
            "description": "Fungal infection attacking leaf surfaces or crowns in poorly drained media.",
            "symptoms": [
                "White powdery film spreading over leaves",
                "Wilting foliage despite moist soil",
                "Dark, soft rot near the crown of the plant"
            ],
            "organic": [
                "Never plant the crown below soil level; keep crown slightly elevated.",
                "Spray with neem oil or mild potassium bicarbonate spray.",
                "Avoid overhead misting and improve container drainage.",
                "Discard plants with softened, rotting crowns."
            ]
        }
    },
    "Lotus": {
        "Leaf Blight": {
            "description": "Waterborne or airborne fungal spots appearing on floating lotus pads.",
            "symptoms": [
                "Brown water-soaked patches on leaf blades",
                "Margins of floating leaves curling and rotting",
                "Foliage decay in stagnant warm water"
            ],
            "organic": [
                "Cut and remove decayed, yellowing, or submerged rotting pads.",
                "Ensure clean water circulation and prevent surface scum buildup.",
                "Avoid excessive fertilization which causes overly dense, weak foliage.",
                "Ensure the pond receives at least 6 hours of unshaded sunlight."
            ]
        }
    }
}


# ---------------- PREDICTION LOGIC ----------------

def predict_disease(image_bytes):
    """
    Simulation prediction based on image hash seed.
    Ready to be swapped with a real ML model or Gemini Vision API.
    """
    seed = int(hashlib.sha256(image_bytes).hexdigest()[:8], 16)
    rng = random.Random(seed)

    plant = rng.choice(list(plants.keys()))
    options = disease_data.get(plant, {})

    # 25% chance of being diagnosed as healthy
    if rng.random() < 0.25 or not options:
        disease = "Healthy"
        description = "No visible disease symptoms or pathogen activity detected."
        symptoms = ["Vibrant leaf pigmentation", "Strong stem structure", "No spots or fungal residues"]
        organic = [
            "Provide balanced daily sunlight suitable for the species.",
            "Water only when topsoil is dry to the touch.",
            "Maintain consistent airflow around the foliage.",
            "Inspect underside of leaves weekly for early pest detection."
        ]
        healthy = True
    else:
        disease = rng.choice(list(options.keys()))
        info = options[disease]
        description = info["description"]
        symptoms = info["symptoms"]
        organic = info["organic"]
        healthy = False

    return {
        "plant": plant,
        "disease": disease,
        "confidence": round(rng.uniform(92.0, 98.8), 1),
        "description": description,
        "symptoms": symptoms,
        "organic": organic,
        "healthy": healthy,
        "date": datetime.now().strftime("%d %b %Y"),
        "time": datetime.now().strftime("%I:%M %p"),
        "image": image_bytes
    }


# ---------------- SIDEBAR NAVIGATION ----------------

with st.sidebar:
    st.markdown("# 🌸 FlowerCare AI")
    st.caption("Smart Diagnosis. Natural Solutions.")
    st.divider()

    pages = [
        "Home",
        "Scan Plant",
        "Organic Solution",
        "Disease Library",
        "Scan History",
        "Profile"
    ]

    for page_name in pages:
        is_current = (st.session_state.page == page_name)
        button_type = "primary" if is_current else "secondary"
        if st.button(page_name, key="nav_" + page_name, use_container_width=True, type=button_type):
            navigate(page_name)
            st.rerun()

    st.divider()
    st.caption("Flower plant health assistant")


# ---------------- 1. HOME ----------------

if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>🌸 FlowerCare AI</h1>
        <h3>Identify Flower Plant Diseases Instantly</h3>
        <p>
        Capture or upload a photo of your flower plant to diagnose
        diseases and discover 100% organic, natural remedies.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📷 Scan a Plant", type="primary", use_container_width=True):
            reset_scan()
            st.rerun()

    with col2:
        if st.button("🌱 Browse Organic Solutions", use_container_width=True):
            st.session_state.active_organic_context = None
            navigate("Organic Solution")
            st.rerun()

    st.subheader("Your Garden Dashboard")
    a, b, c = st.columns(3)
    a.metric("🌸 Supported Flowers", len(plants))
    b.metric("📷 Total Scans", len(st.session_state.history))
    c.metric("🌿 Healthy Plants", sum(1 for x in st.session_state.history if x.get("healthy", False)))

    st.subheader("Supported Flowers")
    cols = st.columns(3)
    for i, (plant, emoji) in enumerate(plants.items()):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="plant-card">
                    <h2>{emoji}</h2>
                    <b>{plant}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---------------- 2. SCAN PLANT ----------------

elif st.session_state.page == "Scan Plant":

    st.title("📷 Scan Your Flower Plant")
    st.write("Take a photo using your camera or upload an image from your device gallery.")

    camera_col, gallery_col = st.columns(2)

    with camera_col:
        camera_image = st.camera_input(
            "Open Camera",
            key=f"cam_input_{st.session_state.uploader_key}"
        )

    with gallery_col:
        gallery_image = st.file_uploader(
            "Choose from Gallery",
            type=["jpg", "jpeg", "png", "webp"],
            key=f"file_input_{st.session_state.uploader_key}"
        )

    selected = camera_image or gallery_image

    if selected is not None:
        st.session_state.image = selected.getvalue()
        navigate("Image Preview")
        st.rerun()

    st.subheader("📸 Tips for Better Accuracy")
    st.markdown("""
    - **Focus on the affected area:** Center the yellowing, spotted, or mildewed leaves.
    - **Good lighting:** Natural daylight produces the most reliable analysis.
    - **Sharp focus:** Avoid motion blur or extreme close-ups that obscure leaf contours.
    """)


# ---------------- 3. IMAGE PREVIEW ----------------

elif st.session_state.page == "Image Preview":

    st.title("Image Preview")
    st.write("Review your image before running the diagnosis.")

    if st.session_state.image:
        try:
            img = Image.open(io.BytesIO(st.session_state.image))
            st.image(img, use_container_width=True)

            if min(img.size) < 100:
                st.error("⚠️ Image resolution is too low. Please provide a clearer photo.")
                if st.button("↻ Retake Photo"):
                    reset_scan()
                    st.rerun()
            else:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("↻ Retake Photo", use_container_width=True):
                        reset_scan()
                        st.rerun()

                with col2:
                    if st.button("✓ Analyze Plant", type="primary", use_container_width=True):
                        with st.spinner("Analyzing plant foliage and patterns..."):
                            result = predict_disease(st.session_state.image)
                            st.session_state.result = result
                            st.session_state.history.insert(0, result.copy())

                        navigate("Diagnosis Result")
                        st.rerun()

        except Exception:
            st.error("Unable to read image. Please retake.")
            if st.button("↻ Retake"):
                reset_scan()
                st.rerun()
    else:
        st.info("No image selected.")
        if st.button("Go to Scan"):
            reset_scan()
            st.rerun()


# ---------------- 4. DIAGNOSIS RESULT ----------------

elif st.session_state.page in ["Diagnosis Result", "Healthy Result"]:

    result = st.session_state.result

    if result is None:
        st.warning("No scan available. Please scan a plant first.")
        if st.button("📷 Scan Plant"):
            reset_scan()
            st.rerun()
    else:
        st.title("Diagnosis Result")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(Image.open(io.BytesIO(result["image"])), use_container_width=True)

        with col2:
            plant = result["plant"]
            emoji = plants.get(plant, "🌸")
            st.subheader(f"{emoji} {plant}")

            if result["healthy"]:
                st.success("🌿 Plant Appears Healthy!")
            else:
                st.error(f"🦠 Detected Condition: {result['disease']}")

            st.metric("Confidence Score", f"{result['confidence']}%")
            st.progress(result["confidence"] / 100)
            st.write(result["description"])

        st.subheader("Key Symptoms Observed")
        for symptom in result["symptoms"]:
            st.markdown(f"- 🌿 {symptom}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌱 View Organic Solution", type="primary", use_container_width=True):
                st.session_state.active_organic_context = result
                navigate("Organic Solution")
                st.rerun()

        with col2:
            if st.button("📷 Scan Another Plant", use_container_width=True):
                reset_scan()
                st.rerun()


# ---------------- 5. ORGANIC SOLUTION ----------------

elif st.session_state.page == "Organic Solution":

    st.title("🌱 Organic Care & Solutions")

    # Priority: Context from library click > Context from last diagnosis > Default Rose Black Spot
    context = st.session_state.active_organic_context or st.session_state.result

    if context:
        plant = context["plant"]
        disease = context.get("disease", "Condition")
        organic = context.get("organic", [])
    else:
        plant = "Rose"
        disease = "Black Spot"
        organic = disease_data["Rose"]["Black Spot"]["organic"]

    st.subheader(f"{disease} — {plant}")

    st.markdown("""
    <div class="hero">
        <h3>🌿 Natural Gardening Philosophy</h3>
        <p>
        Always begin with cultural hygiene (removing decaying material, avoiding wet leaves)
        before applying biological or mineral controls.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🌿 Recommended Organic Treatments")
    for step in organic:
        st.markdown(f"- {step}")

    st.subheader("🛡️ Preventative Guidelines")
    st.markdown("""
    - **Irrigation:** Always water at soil level; wet leaves harbor fungal spores.
    - **Pruning:** Disinfect clippers with 70% alcohol between cuts.
    - **Sunlight & Spacing:** Maximize air passage to keep humidity low around foliage.
    - **Soil Health:** Add well-rotted compost to strengthen the plant's natural immune defenses.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📷 Scan a Plant", use_container_width=True):
            reset_scan()
            st.rerun()
    with col2:
        if st.button("🔍 Explore Disease Library", use_container_width=True):
            navigate("Disease Library")
            st.rerun()


# ---------------- 6. DISEASE LIBRARY ----------------

elif st.session_state.page == "Disease Library":

    st.title("🔍 Flower Disease Library")

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        query = st.text_input("Search disease, symptom, or plant", placeholder="e.g. Mildew, Black Spot, Rose...")
    with col_filter:
        plant_filter = st.selectbox("Filter by flower", ["All"] + list(plants.keys()))

    records = []
    for plant_name, diseases in disease_data.items():
        for d_name, info in diseases.items():
            records.append({
                "plant": plant_name,
                "disease": d_name,
                **info
            })

    filtered = [
        item for item in records
        if (plant_filter == "All" or item["plant"] == plant_filter)
        and (
            not query or
            query.lower() in (
                item["plant"] + " " + item["disease"] + " " + item["description"] + " " + " ".join(item["symptoms"])
            ).lower()
        )
    ]

    if not filtered:
        st.info("No matching diseases found. Try clearing your search filters.")

    for item in filtered:
        with st.container(border=True):
            st.subheader(f"{plants.get(item['plant'], '🌸')} {item['plant']} — {item['disease']}")
            st.write(item["description"])

            st.write("**Symptoms:**")
            for symptom in item["symptoms"][:2]:
                st.write(f"- {symptom}")

            if st.button("View Full Details & Remedies", key=f"btn_{item['plant']}_{item['disease']}"):
                st.session_state.selected_disease = item
                navigate("Disease Details")
                st.rerun()


# ---------------- 7. DISEASE DETAILS ----------------

elif st.session_state.page == "Disease Details":

    item = st.session_state.selected_disease

    if item:
        st.title(f"🦠 {item['plant']} — {item['disease']}")
        st.write(item["description"])

        st.subheader("Recognized Symptoms")
        for symptom in item["symptoms"]:
            st.write(f"🌿 {symptom}")

        st.subheader("Natural & Organic Management")
        for treatment in item["organic"]:
            st.write(f"✅ {treatment}")

        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Disease Library", use_container_width=True):
                navigate("Disease Library")
                st.rerun()
        with col2:
            if st.button("🌱 Open in Organic Solutions", type="primary", use_container_width=True):
                st.session_state.active_organic_context = item
                navigate("Organic Solution")
                st.rerun()
    else:
        st.info("No disease selected.")
        if st.button("Go to Library"):
            navigate("Disease Library")
            st.rerun()


# ---------------- 8. SCAN HISTORY ----------------

elif st.session_state.page == "Scan History":

    st.title("📋 Scan History")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    if not st.session_state.history:
        st.info("No scans recorded yet. Use the camera or upload a photo to begin.")

    for i, item in enumerate(st.session_state.history):
        with st.container(border=True):
            col_img, col_info = st.columns([1, 2])

            with col_img:
                st.image(Image.open(io.BytesIO(item["image"])), use_container_width=True)

            with col_info:
                st.subheader(f"{plants.get(item['plant'], '🌸')} {item['plant']}")
                status_text = "🌿 Healthy" if item.get("healthy") else f"🦠 {item['disease']}"
                st.write(f"**Status:** {status_text}")
                st.caption(f"Score: {item['confidence']}% · {item['date']} at {item['time']}")

                if st.button("View Full Diagnosis", key=f"history_view_{i}"):
                    st.session_state.result = item
                    navigate("Diagnosis Result")
                    st.rerun()


# ---------------- 9. PROFILE ----------------

elif st.session_state.page == "Profile":

    st.title("👤 Gardener Profile")

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Name", value="Plant Lover")
    with col2:
        st.text_input("Email", value="gardener@example.com")

    st.subheader("Your Garden Statistics")
    total = len(st.session_state.history)
    healthy = sum(1 for item in st.session_state.history if item.get("healthy"))

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Scans", total)
    m2.metric("Healthy Plants", healthy)
    m3.metric("Diseases Flagged", total - healthy)

    st.subheader("Preferences")
    st.toggle("🔔 Diagnosis Reminders & Tips", value=True)
    st.selectbox("🌐 Language", ["English", "Hindi", "Telugu", "Tamil"])

    with st.expander("ℹ️ About FlowerCare AI"):
        st.write(
            "FlowerCare AI is an interactive prototype designed for flower plant disease "
            "diagnosis and organic gardening recommendations."
        )

# ---------------- FOOTER ----------------

st.divider()
st.caption("🌸 FlowerCare AI | Smart Diagnosis & Natural Plant Solutions")
