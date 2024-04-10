import streamlit as st

def display_question(question, options):
    st.write(question)
    option = st.radio("Select an option:", options)
    return option

def main():
    st.title("Interests and Skills Assessment")

    # Define questions and options
    questions = [
        "In school, I enjoyed classes that involved:",
        "In my free time, I'm most likely to:",
        "If I had unlimited time and money, I would spend most of my days:",
        "I would consider working in a field that doesn't pay well if it involved:",
        "I prefer to work:",
        "I enjoy working with:",
        "I learn best by:",
        "My strongest skills include:"
    ]

    options = [
        ["Writing, analyzing, and interpreting information.",
         "Working with hands-on projects and experiments.",
         "Persuading and influencing others.",
         "Numbers, calculations, and problem-solving."],
        ["Read a book or watch a documentary.",
         "Build something, fix something, or tinker.",
         "Help others, volunteer, or socialize.",
         "Organize events, solve puzzles, or play strategy games."],
        ["Learning new things and exploring ideas.",
         "Creating or building something tangible.",
         "Connecting with others and making a difference.",
         "Analyzing data and solving complex problems."],
        ["Researching and writing about a topic I'm passionate about.",
         "Designing, crafting, or fixing things with my hands.",
         "Advocating for a cause or helping people in need.",
         "Using data and logic to solve challenging problems."],
        ["Independently, with minimal supervision.",
         "As part of a team, collaborating with others."],
        ["People and building relationships.",
         "Data and using spreadsheets or software.",
         "Abstract ideas and concepts."],
        ["Reading instructions and following procedures.",
         "Experimenting and learning through trial and error.",
         "Discussing and brainstorming ideas with others."],
        ["Communication and writing effectively.",
         "Problem-solving and critical thinking.",
         "Creativity and artistic expression.",
         "All of the above."]
    ]

    user_responses = []

    # Display questions and collect responses
    for i in range(len(questions)):
        user_response = display_question(questions[i], options[i])
        user_responses.append(user_response)

    if st.button("Submit"):
        st.title("Results")
        st.write("You seem to enjoy a variety of activities, including learning, creating, and helping others. "
                 "This suggests you might be open to a broad range of careers.")
        st.write("You indicated a preference for working independently, using both data and ideas, and having strong communication and problem-solving skills. "
                 "This combination could be a fit for many fields.")
        st.write("Here are some general career areas that might be a good starting point for your exploration, based on your answers:")
        st.markdown("""
            ### Creative Fields:
            - Graphic design
            - Web development
            - Architecture
            - Writing/Editing

            ### Problem-solving Fields:
            - Engineering
            - Data Science
            - Project Management
            - Business Analysis

            ### Helping Professions:
            - Social Work
            - Teaching
            - Counseling
            - Non-profit work

            ### Next Steps:
            - Consider taking a more comprehensive career assessment that delves deeper into specific skills and knowledge required for different careers.
            - Research the career areas mentioned above to learn more about the day-to-day work, educational requirements, and salary ranges.
            - Talk to people in different professions to gain insights and network.
            - Consider your values and long-term goals when making career decisions.
        """)

if __name__ == "__main__":
    main()
