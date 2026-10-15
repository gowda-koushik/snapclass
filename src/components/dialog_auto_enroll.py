

import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase


@st.dialog("Quick Enrollment")
def auto_enroll_dialog():

    student_id = st.session_state.student_data["student_id"]

    if "found_subject" not in st.session_state:
        st.session_state.found_subject = None

    subject_code = st.text_input("Enter the subject code")

    if st.button("Search", type="primary", width="stretch"):

        res = (
            supabase
            .table("subjects")
            .select("subject_id, name")
            .eq("subject_code", subject_code)
            .execute()
        )

        if not res.data:
            st.error("Subject code not found!")
            return

        st.session_state.found_subject = res.data[0]

    subject = st.session_state.found_subject

    if subject:

        check = (
            supabase
            .table("subject_students")
            .select("*")
            .eq("subject_id", subject["subject_id"])
            .eq("student_id", student_id)
            .execute()
        )

        if check.data:
            st.info("You're already enrolled.")
            return

        st.markdown(
            f"Would you like to enroll in **{subject['name']}**?"
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button("No thanks", width="stretch"):

                st.session_state.found_subject = None
                st.rerun()

        with c2:

            if st.button(
                "Yes, enroll now!",
                type="primary",
                width="stretch"
            ):

                enroll_student_to_subject(
                    student_id,
                    subject["subject_id"]
                )

                st.session_state.found_subject = None

                st.success("Joined successfully!")

                st.rerun()