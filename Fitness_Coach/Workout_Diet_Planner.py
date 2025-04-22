import os
from dotenv import load_dotenv
from agno.agent import Agent 
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ✅ Create Gemini model instance with API key
gemini_model = Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY)

# Dietary Planner Agent
dietary_planner = Agent(
    model=gemini_model,
    description="Creates personalized dietary plans based on user input.",
    instructions=[
        "Generate a diet plan with breakfast, lunch, dinner, and snacks.",
        "Consider dietary preferences like Keto, Vegetarian, or Low Carb.",
        "Ensure proper hydration and electrolyte balance.",
        "Provide nutritional breakdown including macronutrients and vitamins.",
        "Suggest meal preparation tips for easy implementation.",
        "If necessary, search the web using DuckDuckGo for additional information.",
    ],
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

# Fitness Trainer Agent
fitness_trainer = Agent(
    model=gemini_model,
    description="Generates customized workout routines based on fitness goals.",
    instructions=[
        "Create a workout plan including warm-ups, main exercises, and cool-downs.",
        "Adjust workouts based on fitness level: Beginner, Intermediate, Advanced.",
        "Consider weight loss, muscle gain, endurance, or flexibility goals.",
        "Provide safety tips and injury prevention advice.",
        "Suggest progress tracking methods for motivation.",
        "If necessary, search the web using DuckDuckGo for additional information.",
    ],
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True
)

# Team Lead Agent (combines both meal and fitness plans)
team_lead = Agent(
    model=gemini_model,
    description="Combines diet and workout plans into a holistic health strategy.",
    instructions=[
        "Merge personalized diet and fitness plans for a comprehensive approach, use tables if possible.",
        "Ensure alignment between diet and exercise for optimal results.",
        "Suggest lifestyle tips for motivation and consistency.",
        "Provide guidance on tracking progress and adjusting plans over time."
    ],
    markdown=True
)

# Meal plan function
def get_meal_plan(age, weight, height, activity_level, dietary_preference, fitness_goal):
    prompt = (f"Create a personalized meal plan for a {age}-year-old person, weighing {weight}kg, "
              f"{height}cm tall, with an activity level of '{activity_level}', following a "
              f"'{dietary_preference}' diet, aiming to achieve '{fitness_goal}'.")
    return dietary_planner.run(prompt)

# Fitness plan function
def get_fitness_plan(age, weight, height, activity_level, fitness_goal):
    prompt = (f"Generate a workout plan for a {age}-year-old person, weighing {weight}kg, "
              f"{height}cm tall, with an activity level of '{activity_level}', "
              f"aiming to achieve '{fitness_goal}'. Include warm-ups, exercises, and cool-downs.")
    return fitness_trainer.run(prompt)

# Full health plan function
def get_full_health_plan(name, age, weight, height, activity_level, dietary_preference, fitness_goal):
    meal_plan = get_meal_plan(age, weight, height, activity_level, dietary_preference, fitness_goal)
    fitness_plan = get_fitness_plan(age, weight, height, activity_level, fitness_goal)
    
    return team_lead.run(
        f"Greet the customer, {name}.\n\n"
        f"User Information: {age} years old, {weight}kg, {height}cm, activity level: {activity_level}.\n\n"
        f"Fitness Goal: {fitness_goal}\n\n"
        f"Meal Plan:\n{meal_plan}\n\n"
        f"Workout Plan:\n{fitness_plan}\n\n"
        f"Provide a holistic health strategy integrating both plans."
    )

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="AI Health & Fitness Plan", page_icon="🏋️‍♂️", layout="wide")

# Custom Styles
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #FF6347;
        }
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: #4CAF50;
        }
        .goal-card {
            padding: 20px;
            margin: 10px;
            background-color: #FFF;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title">🏋️‍♂️ AI Health & Fitness Plan Generator</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Personalized fitness and nutrition plans to help you achieve your health goals!</p>', unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("⚙️ Health & Fitness Inputs")
st.sidebar.subheader("Personalize Your Fitness Plan")

age = st.sidebar.number_input("Age (in years)", min_value=10, max_value=100, value=25)
weight = st.sidebar.number_input("Weight (in kg)", min_value=30, max_value=200, value=70)
height = st.sidebar.number_input("Height (in cm)", min_value=100, max_value=250, value=170)
activity_level = st.sidebar.selectbox("Activity Level", ["Low", "Moderate", "High"])
dietary_preference = st.sidebar.selectbox("Dietary Preference", ["Keto", "Vegetarian", "Low Carb", "Balanced"])
fitness_goal = st.sidebar.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Endurance", "Flexibility"])

# Name input
name = st.text_input("What's your name?", "John Doe")

st.markdown("---")
st.markdown("### 🏃‍♂️ Personal Fitness Profile")

# Button to generate plan
if st.sidebar.button("Generate Health Plan"):
    if not age or not weight or not height:
        st.sidebar.warning("Please fill in all required fields.")
    else:
        with st.spinner("💥 Generating your personalized health & fitness plan..."):
            full_health_plan = get_full_health_plan(name, age, weight, height, activity_level, dietary_preference, fitness_goal)
        
            st.subheader("Your Personalized Health & Fitness Plan")
            st.markdown(full_health_plan.content)

            st.info("This is your customized health and fitness strategy, including meal and workout plans.")

        st.markdown("""
            <div class="goal-card">
                <h4>🏆 Stay Focused, Stay Fit!</h4>
                <p>Consistency is key! Keep pushing yourself, and you will see results. Your fitness journey starts now!</p>
            </div>
        """, unsafe_allow_html=True)
