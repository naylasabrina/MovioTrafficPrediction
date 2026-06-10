import streamlit as st
import pandas as pd
import joblib

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Traffic Prediction System",
    page_icon="🚦",
    layout="wide"
)

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(
        135deg,
        #FFFFFF 0%,
        #F5FAFF 100%
    );
}

/* Sidebar */
[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #193546 0%,
        #065B98 100%
    );
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3{
    color:white;
}

/* Title */
.main-title{
    text-align:center;
    font-size:90px;
    font-weight:900;
    color:#065B98;
    letter-spacing:4px;
    margin-top:-40px;
    margin-bottom:-10px;
}
.sub-title{
    text-align:center;
    color:#5E7388;
    font-size:24px;
    font-weight:500;
}

/* Input Box */
div[data-baseweb="input"]{
    background:white;
    border:2px solid #D8EFFF;
    border-radius:15px;
}

div[data-baseweb="select"]{
    border-radius:15px;
}


/* Metric Card */
[data-testid="metric-container"]{
    background:white;
    border-radius:20px;
    padding:15px;
    border-left:6px solid #0DB8D3;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

/* Button */
.stButton button{
    width:100%;
    height:55px;
    border:none;
    border-radius:15px;

    background: linear-gradient(
        90deg,
        #1B7FDC,
        #0DB8D3
    );

    color:white;
    font-size:18px;
    font-weight:bold;
}

.stButton button{
    width:100%;
    height:60px;

    background: linear-gradient(
        90deg,
        #065B98,
        #1B7FDC,
        #0DB8D3
    );

    color:white;
    font-size:20px;
    font-weight:700;

    border:none;
    border-radius:18px;

    box-shadow:
        0px 6px 18px rgba(27,127,220,0.35);
}

/* Result LOW */
.result-low{
    background:#E8FBFF;
    color:#0DB8D3;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

/* Result NORMAL */
.result-normal{
    background:#EAF3FF;
    color:#1B7FDC;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

/* Result HIGH */
.result-high{
    background:#D8EBFF;
    color:#065B98;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

/* Result HEAVY */
.result-heavy{
    background: linear-gradient(
        90deg,
        #193546,
        #065B98
    );
    color:white;
    padding:25px;
    border-radius:20px;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}
/* Number Input */
.stNumberInput input{
    border-radius:15px !important;
    border:2px solid #D8EFFF !important;
    background:white !important;
}

/* Dropdown */
.stSelectbox > div > div{
    border-radius:15px !important;
    border:2px solid #D8EFFF !important;
    background:white !important;
}
/* File Uploader */
[data-testid="stFileUploader"]{
    background:white;
    border-radius:20px;
    padding:15px;
    border:2px dashed #1B7FDC;
}
/* Sidebar Label */
[data-testid="stSidebar"] label{
    color:#FFFFFF !important;
    font-weight:600;
}

/* Sidebar Text */
[data-testid="stSidebar"] p{
    color:#DCEBFF !important;
}

/* Sidebar Radio */
[data-testid="stSidebar"] div[role="radiogroup"] label{
    color:#FFFFFF !important;
}
[data-testid="stSidebar"] .stRadio label{
    font-size:16px;
    font-weight:500;
}
.form-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0 4px 20px rgba(0,0,0,
</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD MODEL
# =====================================

svm_model = joblib.load("svm_modelJb_SVM-HPO.joblib")
svm_scaler = joblib.load("svm_scaler.joblib")
svm_freq = joblib.load("svm_day_freq.joblib")

knn_model = joblib.load("knn_modelJb_KNN-HPO.joblib")
knn_scaler = joblib.load("knn_scaler.joblib")
knn_freq = joblib.load("knn_day_freq.joblib")

dt_model = joblib.load("dt_modelJb_DT-HPO.joblib")
dt_freq = joblib.load("dt_day_freq.joblib")


# =====================================
# HEADER
# =====================================

st.markdown(
    "<div class='main-title'>MOVIO</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Traffic Prediction System using Machine Learning</div>",
    unsafe_allow_html=True
)



# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.header("⚙️ Configuration")

    model_option = st.selectbox(
        "Select Model",
        ["SVM", "KNN", "Decision Tree"]
    )


    input_method = st.radio(
        "Input Method",
        ["Input Manual", "Upload CSV"]
    )
# =====================================
# MANUAL INPUT
# =====================================

if input_method == "Input Manual":

    st.subheader("📝 Input Traffic Data")

    col1, col2 = st.columns(2)

    with col1:
        car = st.number_input("Car Count", min_value=0)
        bike = st.number_input("Bike Count", min_value=0)
        bus = st.number_input("Bus Count", min_value=0)

    with col2:
        truck = st.number_input("Truck Count", min_value=0)

        hour = st.number_input(
            "Hour",
            min_value=0,
            max_value=23
        )

        day = st.selectbox(
            "Day of Week",
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday"
            ]
        )

    total = car + bike + bus + truck

    st.metric("Total Vehicles", total)

    if st.button("🚀 Predict"):

        if model_option == "SVM":

            day_encoded = svm_freq[day]

            data = pd.DataFrame(
                [[
                    car,
                    bike,
                    bus,
                    truck,
                    total,
                    day_encoded,
                    hour
                ]],
                columns=[
                    "CarCount",
                    "BikeCount",
                    "BusCount",
                    "TruckCount",
                    "Total",
                    "Day of the week_freq_encode",
                    "Hour"
                ]
            )

            data = svm_scaler.transform(data)
            prediction = svm_model.predict(data)

        elif model_option == "KNN":

            day_encoded = knn_freq[day]

            data = pd.DataFrame(
                [[
                    car,
                    bike,
                    bus,
                    truck,
                    total,
                    day_encoded,
                    hour
                ]],
                columns=[
                    "CarCount",
                    "BikeCount",
                    "BusCount",
                    "TruckCount",
                    "Total",
                    "Day of the week_freq_encode",
                    "Hour"
                ]
            )

            data = knn_scaler.transform(data)
            prediction = knn_model.predict(data)

        else:

            day_encoded = dt_freq[day]

            data = pd.DataFrame(
                [[
                    car,
                    bike,
                    bus,
                    truck,
                    total,
                    day_encoded,
                    hour
                ]],
                columns=[
                    "CarCount",
                    "BikeCount",
                    "BusCount",
                    "TruckCount",
                    "Total",
                    "Day of the week_freq_encode",
                    "Hour"
                ]
            )

            prediction = dt_model.predict(data)

        result = str(prediction[0]).lower()

        st.subheader("🎯 Prediction Result")

        if result == "low":
            st.markdown(
                "<div class='result-low'>🟢 LOW TRAFFIC</div>",
                unsafe_allow_html=True
            )

        elif result == "normal":
            st.markdown(
                "<div class='result-normal'>🔵 NORMAL TRAFFIC</div>",
                unsafe_allow_html=True
            )

        elif result == "high":
            st.markdown(
                "<div class='result-high'>🟠 HIGH TRAFFIC</div>",
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                "<div class='result-heavy'>🔴 HEAVY TRAFFIC</div>",
                unsafe_allow_html=True
            )

# =====================================
# CSV INPUT
# =====================================

else:

    st.subheader("📂 Upload CSV File")

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.write("### Dataset Preview")
        st.dataframe(df.head())

        if st.button("🚀 Predict CSV"):

            df["Total"] = (
                df["CarCount"]
                + df["BikeCount"]
                + df["BusCount"]
                + df["TruckCount"]
            )

            if model_option == "SVM":

                df["Day of the week_freq_encode"] = df["Day of the week"].map(
                    svm_freq
                )

                features = df[
                    [
                        "CarCount",
                        "BikeCount",
                        "BusCount",
                        "TruckCount",
                        "Total",
                        "Day of the week_freq_encode",
                        "Hour"
                    ]
                ]

                features = svm_scaler.transform(features)
                prediction = svm_model.predict(features)

            elif model_option == "KNN":

                df["Day of the week_freq_encode"] = df["Day of the week"].map(
                    knn_freq
                )

                features = df[
                    [
                        "CarCount",
                        "BikeCount",
                        "BusCount",
                        "TruckCount",
                        "Total",
                        "Day of the week_freq_encode",
                        "Hour"
                    ]
                ]

                features = knn_scaler.transform(features)
                prediction = knn_model.predict(features)

            else:

                df["Day of the week_freq_encode"] = df["Day of the week"].map(
                    dt_freq
                )

                features = df[
                    [
                        "CarCount",
                        "BikeCount",
                        "BusCount",
                        "TruckCount",
                        "Total",
                        "Day of the week_freq_encode",
                        "Hour"
                    ]
                ]

                prediction = dt_model.predict(features)

            df["Prediction"] = prediction

            st.success("Prediction completed successfully!")

            st.dataframe(df)

            csv = df.to_csv(index=False)

            st.download_button(
                label="⬇ Download Result CSV",
                data=csv,
                file_name="prediction_result.csv",
                mime="text/csv"
            )