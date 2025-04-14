"""
### Run using:
`streamlit run streamlit_app.py`
"""

import streamlit as st
from Solvers import *

st.set_page_config(page_title="Recurrence Relation Solver")
st.title("Recurrence Relation Solver")

tab1, tab2 = st.tabs(["Master's Theorem", "Akra-Bazzi Method"])

with tab1:
    st.subheader("Master's Theorem")
    type_option = st.radio(
        "Choose recurrence type:",
        [
            r"Decreasing T(n) = aT(n - b) + f(n)",
            r"Dividing T(n) = aT(n/b) + f(n)",
        ],
    )
    is_decreasing = type_option == "Decreasing T(n) = aT(n - b) + f(n)"

    st.latex(rf"T(n) = a T(n {'-' if is_decreasing else '/'} b) + f(n)")

    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("a", key="mt_a", min_value=1, value=1)
    with col2:
        b = st.number_input("b", key="mt_b", min_value=1 if is_decreasing else 2, value=2)
    col1, col2 = st.columns(2)
    with col1:
        k = st.number_input("k", key="mt_k", min_value=0, value=1)
    with col2:
        p = st.number_input("p", key="mt_p", min_value=0, value=0)

    st.markdown("##### Generated Equation:")
    recurrence_eq = rf"T(n) = {a} T(n {'-'if is_decreasing else '/'} {b}) + n^{{{k}}} \log^{{{p}}}(n)"
    st.latex(rf"{recurrence_eq} \text{{ where }} f(n) = O(n^k \log^p n)")

    mt = MastersTheorem(a, b, is_decreasing, k, p)

    if st.button("Solve", key="solve_mt"):
        try:
            latex_result = mt.get_ans()
            st.markdown("##### Result:")
            st.latex(latex_result)
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("Akra-Bazzi Method")
    st.latex(r"T(n) = a_1 T(n/b_1) + a_2 T(n/b_2) + ... + f(n)")

    num_terms = st.number_input("Number of dividing terms:", min_value=1, max_value=5, value=2, step=1)

    terms = []
    for i in range(num_terms):
        st.markdown(f"##### Term {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            a_i = st.number_input(f"a{i+1}", value=1, step=1, key=f"a{i}")
        with col2:
            b_i = st.number_input(f"b{i+1}", min_value=2, value=2, step=1, key=f"b{i}")
        terms.append((a_i, b_i))

    st.markdown("##### f(n)")
    col1, col2 = st.columns(2)
    with col1:
        k3 = st.number_input("k", min_value=0, value=1, step=1, key="k3")
    with col2:
        p3 = st.number_input("p", min_value=0, value=0, step=1, key="p3")

    st.markdown("##### Generated Equation:")
    latex_eq = r"T(n) = "
    for i, (a, b) in enumerate(terms):
        latex_eq += f"{a} T(n/{b})"
        if i < num_terms - 1:
            latex_eq += " + "
    latex_eq += rf"n^{{{k3}}} \log^{{{p3}}}(n)"
    st.latex(rf"{latex_eq} \text{{ where }} f(n) = \Theta(n^k \log^p n)")

    ab = AkraBazzi(terms, k3, p3)

    if st.button("Solve", key="solve_ab"):
        try:
            latex_result = ab.get_ans()
            st.markdown("##### Result:")
            st.latex(latex_result)
        except Exception as e:
            st.error(f"Error: {e}")
