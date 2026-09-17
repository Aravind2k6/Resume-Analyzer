import streamlit as st
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📄 AI Resume Analyzer")

st.write(
    "Upload your resume and compare it with a job description "
    "using AI-powered analysis."
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.subheader("1. Upload Your Resume")

resume = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)


# --------------------------------------------------
# JOB DESCRIPTION
# --------------------------------------------------

st.subheader("2. Enter Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250
)


# --------------------------------------------------
# ANALYZE BUTTON
# --------------------------------------------------

if st.button("🔍 Analyze Resume"):

    if resume is None:

        st.error(
            "Please upload your resume."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        files = {
            "resume": (
                resume.name,
                resume.getvalue(),
                "application/pdf"
            )
        }

        data = {
            "job_description": job_description
        }

        try:

            # ------------------------------------------
            # MATCH RESUME WITH JOB
            # ------------------------------------------

            with st.spinner(
                "Analyzing resume..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/match-job",
                    files=files,
                    data=data
                )


            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "Resume analyzed successfully! 🎉"
                )


                # --------------------------------------
                # MATCH SCORE
                # --------------------------------------

                st.subheader(
                    "📊 Resume Match Score"
                )

                match_percentage = float(
                    result["match_percentage"]
                )

                st.progress(
                    min(int(match_percentage), 100)
                )

                st.metric(
                    "Match Percentage",
                    f"{match_percentage}%"
                )


                # --------------------------------------
                # SKILLS
                # --------------------------------------

                col1, col2 = st.columns(2)


                # Matched skills
                with col1:

                    st.subheader(
                        "✅ Matched Skills"
                    )

                    if result["matched_skills"]:

                        for skill in result[
                            "matched_skills"
                        ]:

                            st.success(
                                skill
                            )

                    else:

                        st.info(
                            "No matching skills found."
                        )


                # Missing skills
                with col2:

                    st.subheader(
                        "❌ Missing Skills"
                    )

                    if result["missing_skills"]:

                        for skill in result[
                            "missing_skills"
                        ]:

                            st.warning(
                                skill
                            )

                    else:

                        st.success(
                            "No missing skills."
                        )


                # --------------------------------------
                # AI ANALYSIS
                # --------------------------------------

                st.divider()

                st.subheader(
                    "🤖 AI Resume Analysis"
                )

                if result.get("ai_analysis"):

                    st.markdown(
                        result["ai_analysis"]
                    )

                else:

                    st.info(
                        "AI analysis is not available."
                    )


            # ------------------------------------------
            # BACKEND ERROR
            # ------------------------------------------

            else:

                st.error(
                    f"Backend error: "
                    f"{response.status_code}"
                )

                st.write(
                    response.text
                )


        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to FastAPI."
            )

            st.info(
                "Make sure the FastAPI backend is running "
                "on http://127.0.0.1:8000"
            )


# --------------------------------------------------
# ANALYSIS HISTORY
# --------------------------------------------------

st.divider()

st.subheader(
    "📚 Analysis History"
)


if st.button(
    "View Previous Analyses"
):

    try:

        history_response = requests.get(
            "http://127.0.0.1:8000/analyses"
        )


        if history_response.status_code == 200:

            analyses = history_response.json()


            if analyses:

                for analysis in analyses:

                    st.markdown("---")

                    st.write(
                        f"### 📄 {analysis['filename']}"
                    )

                    st.metric(
                        "Match Percentage",
                        f"{analysis['match_percentage']}%"
                    )


                    # ----------------------------------
                    # Previous matched skills
                    # ----------------------------------

                    st.write(
                        "**Matched Skills:**"
                    )

                    st.write(
                        analysis["matched_skills"]
                    )


                    # ----------------------------------
                    # Previous missing skills
                    # ----------------------------------

                    st.write(
                        "**Missing Skills:**"
                    )

                    st.write(
                        analysis["missing_skills"]
                    )


                    # ----------------------------------
                    # Previous AI analysis
                    # ----------------------------------

                    with st.expander(
                        "🤖 View AI Analysis"
                    ):

                        if analysis.get(
                            "ai_analysis"
                        ):

                            st.markdown(
                                analysis["ai_analysis"]
                            )

                        else:

                            st.info(
                                "No AI analysis available."
                            )


            else:

                st.info(
                    "No previous analyses found."
                )


        else:

            st.error(
                "Could not retrieve analysis history."
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI."
        )