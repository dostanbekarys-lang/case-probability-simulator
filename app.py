import streamlit as st
import random
import math

st.set_page_config(
    page_title="Case Probability Simulator",
    page_icon="🎁",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🎮 Case Opening Probability Simulator")
st.write(
    "An interactive simulation of probability in virtual case openings."
)

st.divider()

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("⚙️ Case Settings")

knife_probability = st.sidebar.slider(
    "Knife probability (%)",
    min_value=0.1,
    max_value=5.0,
    value=0.5,
    step=0.1
)

number_of_cases = st.sidebar.slider(
    "Number of cases",
    min_value=1,
    max_value=10000,
    value=100,
    step=1
)

# Convert percentage to decimal
knife_p = knife_probability / 100

# Other item probabilities
common_p = 70.0
rare_p = 20.0
epic_p = 8.0
legendary_p = 1.5

# Adjust common probability if knife probability changes
common_p = 100 - rare_p - epic_p - legendary_p - knife_probability

items = [
    "Common",
    "Rare",
    "Epic",
    "Legendary",
    "Knife"
]

weights = [
    common_p,
    rare_p,
    epic_p,
    legendary_p,
    knife_probability
]

# -----------------------------
# THEORETICAL PROBABILITY
# -----------------------------

probability_at_least_one = 1 - (1 - knife_p) ** number_of_cases

expected_knives = number_of_cases * knife_p

# -----------------------------
# CASE OPENING
# -----------------------------

st.subheader("🎁 Open a Case")

if st.button("OPEN CASE", use_container_width=True):

    result = random.choices(
        items,
        weights=weights,
        k=1
    )[0]

    if result == "Knife":
        st.success("🔪 YOU GOT A KNIFE!")
    elif result == "Legendary":
        st.warning("⭐ Legendary item!")
    elif result == "Epic":
        st.info("💜 Epic item!")
    elif result == "Rare":
        st.info("🔵 Rare item!")
    else:
        st.write("⚪ Common item")

    st.write(f"**Result:** {result}")

st.divider()

# -----------------------------
# PROBABILITY TABLE
# -----------------------------

st.subheader("🎯 Case Drop Probabilities")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("⚪ Common", f"{common_p:.1f}%")

with col2:
    st.metric("🔵 Rare", f"{rare_p:.1f}%")

with col3:
    st.metric("💜 Epic", f"{epic_p:.1f}%")

with col4:
    st.metric("⭐ Legendary", f"{legendary_p:.1f}%")

with col5:
    st.metric("🔪 Knife", f"{knife_probability:.1f}%")

st.divider()

# -----------------------------
# THEORETICAL CALCULATION
# -----------------------------

st.subheader("📐 Theoretical Probability")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Cases",
        number_of_cases
    )

with col2:
    st.metric(
        "Chance of ≥1 Knife",
        f"{probability_at_least_one * 100:.2f}%"
    )

with col3:
    st.metric(
        "Expected Knives",
        f"{expected_knives:.2f}"
    )

st.latex(
    r"P(X \geq 1) = 1 - (1-p)^n"
)

st.write(
    f"Where p = {knife_p:.4f} is the probability of a knife "
    f"and n = {number_of_cases} is the number of openings."
)

st.divider()

# -----------------------------
# MASS SIMULATION
# -----------------------------

st.subheader("🧪 Experimental Simulation")

if st.button(
    f"SIMULATE {number_of_cases:,} CASES",
    use_container_width=True
):

    results = random.choices(
        items,
        weights=weights,
        k=number_of_cases
    )

    common_count = results.count("Common")
    rare_count = results.count("Rare")
    epic_count = results.count("Epic")
    legendary_count = results.count("Legendary")
    knife_count = results.count("Knife")

    simulation_data = {
        "Common": common_count,
        "Rare": rare_count,
        "Epic": epic_count,
        "Legendary": legendary_count,
        "Knife": knife_count
    }

    st.subheader("📊 Simulation Results")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Common", common_count)

    with col2:
        st.metric("Rare", rare_count)

    with col3:
        st.metric("Epic", epic_count)

    with col4:
        st.metric("Legendary", legendary_count)

    with col5:
        st.metric("🔪 Knives", knife_count)

    st.bar_chart(simulation_data)

    # Experimental knife probability
    experimental_probability = knife_count / number_of_cases

    st.subheader("🔬 Theory vs Experiment")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Theoretical Knife Probability",
            f"{knife_probability:.2f}%"
        )

    with col2:
        st.metric(
            "Experimental Knife Probability",
            f"{experimental_probability * 100:.2f}%"
        )

    difference = abs(
        knife_probability -
        experimental_probability * 100
    )

    st.write(
        f"Difference between theory and experiment: "
        f"**{difference:.2f}%**"
    )

st.divider()

# -----------------------------
# PROBABILITY CURVE
# -----------------------------

st.subheader("📈 Probability of Getting At Least One Knife")

case_numbers = [
    1,
    10,
    25,
    50,
    100,
    250,
    500,
    1000,
    2500,
    5000,
    10000
]

probabilities = []

for n in case_numbers:

    probability = 1 - (1 - knife_p) ** n

    probabilities.append(
        probability * 100
    )

chart_data = {
    "Number of Cases": case_numbers,
    "Probability (%)": probabilities
}

st.line_chart(
    chart_data,
    x="Number of Cases",
    y="Probability (%)"
)

st.divider()

# -----------------------------
# EXPLANATION
# -----------------------------

st.subheader("🧠 How Does It Work?")

st.write(
    """
    Each case opening is an independent random experiment.

    The probability of getting a knife from one case is defined
    by the selected knife probability.

    The program uses random simulation to reproduce case openings.

    The theoretical formula calculates the probability of getting
    at least one knife after several openings.

    When the number of simulations increases, the experimental
    probability becomes closer to the theoretical probability.
    """
)

st.info(
    "Note: The item probabilities in this project are hypothetical "
    "and are used only for educational simulation."
)