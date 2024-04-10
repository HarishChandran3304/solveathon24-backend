import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(layout="wide")

def get_supergroup_data(num_entries, domain, batch, gender):
    male_names = ["John", "Michael", "Robert", "David", "James", "William", "Joseph", "Charles", "Thomas", "Daniel"]
    female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    
    fake_data = {
        "Name": np.random.choice(male_names, num_entries) if gender == "Male" else np.random.choice(female_names, num_entries),
        "Domain": np.random.choice([domain], num_entries),
        "Batch": np.random.choice([batch], num_entries),
        "Gender": np.random.choice([gender], num_entries),
        "Learning Rate": sorted([np.sort(np.random.uniform(0.6, 0.9, 5)) for _ in range(num_entries)], key=lambda x: x[-1], reverse=True),
    }

    df = pd.DataFrame(fake_data)
    
    return df


def main():
    st.title('Super Groups')

    # Dropdown inputs
    st.sidebar.header('Filters')
    domain = st.sidebar.selectbox('Domain', ["Web Dev", "CP", "AI/ML", "Blockchain"])
    batch = st.sidebar.selectbox('Batch', ["2020", "2021", "2022", "2023"])
    gender = st.sidebar.selectbox('Gender', ["Male", "Female", "Other"])

    # Checkbox inputs
    if domain == "Web Dev":
        github_contributions = st.sidebar.slider('GitHub Contributions', min_value=0, max_value=500, value=100)
        recent_achievements = st.sidebar.slider('Recent Achievements', min_value=0, max_value=10, value=2)
        js = st.sidebar.checkbox('JavaScript')
        ts = st.sidebar.checkbox('TypeScript')
        fastapi = st.sidebar.checkbox('FastAPI')
        mongodb = st.sidebar.checkbox('MongoDB')
        react = st.sidebar.checkbox('React')
        tailwind = st.sidebar.checkbox('Tailwind CSS')
        nextjs = st.sidebar.checkbox('NextJS')

    
    elif domain == "CP":
        cpp = st.sidebar.checkbox('C++')
        java = st.sidebar.checkbox('Java')
        python = st.sidebar.checkbox('Python')
        stl = st.sidebar.checkbox('STL')
        dsa = st.sidebar.checkbox('DSA')
        daa = st.sidebar.checkbox('DAA')
        
        leetcode_questions = st.sidebar.slider('LeetCode Solved Questions', min_value=0, max_value=2000, value=100)
        codeforces_rating = st.sidebar.slider('CodeForces Rating', min_value=0, max_value=4000, value=1500)
        codechef_rating = st.sidebar.slider('CodeChef Rating', min_value=0, max_value=3000, value=1200)
    
    elif domain == "AI/ML":
        deep_learning = st.sidebar.checkbox('Deep Learning')
        machine_learning = st.sidebar.checkbox('Machine Learning')
        computer_vision = st.sidebar.checkbox('Computer Vision')
        nlp = st.sidebar.checkbox('NLP')

        kaggle_rating = st.sidebar.slider('Kaggle Rating', min_value=0, max_value=2000, value=100)
    
    elif domain == "Blockchain":
        solidity = st.sidebar.checkbox('Solidity')
        ethereum = st.sidebar.checkbox('Ethereum')
        smart_contracts = st.sidebar.checkbox('Smart Contracts')
        web3 = st.sidebar.checkbox('Web3')

    # Submit button
    if st.sidebar.button('Find'):
        df = get_supergroup_data(random.randint(15, 25), domain, batch, gender)
        
        st.dataframe(
            df, 
            column_config={"Learning Rate": st.column_config.LineChartColumn("Learning Rate", y_min=0.5, y_max=1.0)},
            width=1000,
            height=500,
            hide_index=True
        )

    
if __name__ == "__main__":
    main()