import streamlit as st
from textblob import TextBlob
import pandas as pd

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon="🎭",
    layout="centered"
)

# ── Helper Functions ──────────────────────────────────────────
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity    = blob.sentiment.polarity      # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1

    if polarity > 0.1:
        sentiment = "Positive 😊"
        color     = "green"
        emoji     = "😊"
    elif polarity < -0.1:
        sentiment = "Negative 😞"
        color     = "red"
        emoji     = "😞"
    else:
        sentiment = "Neutral 😐"
        color     = "orange"
        emoji     = "😐"

    return {
        "sentiment":    sentiment,
        "polarity":     round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
        "color":        color,
        "emoji":        emoji,
    }

# ── UI ────────────────────────────────────────────────────────
st.title("🎭 Sentiment Analysis App")
st.markdown("Analyze the **emotion and tone** of any text instantly.")
st.divider()

# Tabs
tab1, tab2 = st.tabs(["📝 Single Text", "📋 Multiple Texts"])

# ── Tab 1: Single Text ────────────────────────────────────────
with tab1:
    text_input = st.text_area(
        "Enter your text below:",
        placeholder="e.g. I love this product! It works amazingly well.",
        height=150
    )

    if st.button("🔍 Analyze", use_container_width=True, type="primary"):
        if not text_input.strip():
            st.warning("⚠️ Please enter some text first.")
        else:
            result = analyze_sentiment(text_input)

            st.divider()

            # Result box
            st.markdown(
                f"""
                <div style='text-align:center; padding:30px; border-radius:15px;
                            background-color:{"#e6ffe6" if result["color"]=="green"
                                              else "#ffe6e6" if result["color"]=="red"
                                              else "#fff3e6"};
                            border: 2px solid {result["color"]};'>
                    <h1 style='color:{result["color"]}'>{result["emoji"]} {result["sentiment"]}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.divider()

            # Metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Polarity Score",
                    value=result["polarity"],
                    help="-1 = Very Negative | 0 = Neutral | +1 = Very Positive"
                )
            with col2:
                st.metric(
                    label="Subjectivity Score",
                    value=result["subjectivity"],
                    help="0 = Objective (Fact) | 1 = Subjective (Opinion)"
                )

            st.divider()

            # Polarity bar
            st.markdown("**Polarity Scale** (−1 Negative → +1 Positive)")
            normalized = (result["polarity"] + 1) / 2  # convert -1~1 to 0~1
            st.progress(normalized)

            # Subjectivity bar
            st.markdown("**Subjectivity Scale** (0 Fact → 1 Opinion)")
            st.progress(result["subjectivity"])

            # Explanation
            st.divider()
            st.markdown("### 📖 What does this mean?")
            if result["color"] == "green":
                st.success("✅ This text has a **positive** tone. It expresses happiness, satisfaction, or approval.")
            elif result["color"] == "red":
                st.error("❌ This text has a **negative** tone. It expresses sadness, anger, or dissatisfaction.")
            else:
                st.info("ℹ️ This text has a **neutral** tone. It is neither positive nor negative.")

# ── Tab 2: Multiple Texts ─────────────────────────────────────
with tab2:
    st.markdown("Enter **one sentence per line** to analyze multiple texts at once.")

    multi_input = st.text_area(
        "Enter multiple texts (one per line):",
        placeholder="I love this!\nThis is terrible.\nThe weather is okay today.",
        height=200
    )

    if st.button("🔍 Analyze All", use_container_width=True, type="primary"):
        lines = [l.strip() for l in multi_input.strip().split("\n") if l.strip()]
        if not lines:
            st.warning("⚠️ Please enter at least one line of text.")
        else:
            results = []
            for line in lines:
                r = analyze_sentiment(line)
                results.append({
                    "Text":         line,
                    "Sentiment":    r["sentiment"],
                    "Polarity":     r["polarity"],
                    "Subjectivity": r["subjectivity"],
                })

            df = pd.DataFrame(results)
            st.divider()
            st.subheader("📊 Results")
            st.dataframe(df, use_container_width=True)

            # Summary
            st.divider()
            st.subheader("📈 Summary")
            total    = len(results)
            positive = sum(1 for r in results if "Positive" in r["Sentiment"])
            negative = sum(1 for r in results if "Negative" in r["Sentiment"])
            neutral  = total - positive - negative

            c1, c2, c3 = st.columns(3)
            c1.metric("😊 Positive", f"{positive}/{total}")
            c2.metric("😞 Negative", f"{negative}/{total}")
            c3.metric("😐 Neutral",  f"{neutral}/{total}")

# ── Footer ─────────────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit + TextBlob · Internship Project 🎓")
