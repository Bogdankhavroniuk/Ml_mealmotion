from django.shortcuts import render, redirect
from .models import Calories, MealPlanner,  Recomendationmodel, Dish

# View for the index page

def index(request):
    # Default values
    name = weight = height = age = sex = goal = None
    activity = time_in_hours_activity = time_from_last_eating = None

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        age = request.POST.get('age')
        sex = request.POST.get('sex')
        goal = request.POST.get('goal')
        activity = request.POST.get('activity')
        time_in_hours_activity = request.POST.get('time_in_hours_activity')
        time_from_last_eating = request.POST.get('time_from_last_eating')

        # Check if all required fields are filled
        # ... (validation logic)

        # Save data to the session
        request.session['name'] = name
        request.session['weight'] = weight
        request.session['height'] = height
        request.session['age'] = age
        request.session['sex'] = sex
        request.session['goal'] = goal
        request.session['activity'] = activity
        request.session['time_in_hours_activity'] = time_in_hours_activity
        request.session['time_from_last_eating'] = time_from_last_eating

        # Calculate calories burned (moved to this function)
        calories_burned = calculate_calories(weight, height, age, sex, activity, time_in_hours_activity, time_from_last_eating)
        request.session['calories_burned'] = calories_burned

        # Redirect to the recommendations page
        return render(request, 'Site/recommendations.html', {
            'calories_burned': calories_burned,
            'name': name,  # Pass user data to recommendations.html
            'weight': weight,
            'height': height,
            'age': age,
            'sex': sex,
            'goal': goal,
            'activity': activity,
            'time_in_hours_activity': time_in_hours_activity,
            'time_from_last_eating': time_from_last_eating,
        })

    # Render the index page
    return render(request, 'Site/index.html', {
        'name': name,
        'weight': weight,
        'height': height,
        'age': age,
        'sex': sex,
        'goal': goal,
        'activity': activity,
        'time_in_hours_activity': time_in_hours_activity,
        'time_from_last_eating': time_from_last_eating
    })


    # Render the index page
    return render(request, 'Site/index.html', {
        'name': name,
        'weight': weight,
        'height': height,
        'age': age,
        'sex': sex,
        'activity': activity,
        'time_in_hours_activity': time_in_hours_activity,
        'time_from_last_eating': time_from_last_eating
    })
    request.session['calories_burned'] = calories_burned
    request.session['weight'] = form_data["weight"]
    request.session['goal'] = form_data["goal"]

    # Redirect to the recommendations page
    return render(request, 'Site/recommendations.html')


def calculate_calories(request):
    def get_form_data(request):


        # Define required fields
        required_fields = [
             "weight", "height", "age", "sex", "goal", "activity",
            "time_in_hours_activity", "time_from_last_eating"
        ]

        # Extract data from the form
        data = {

            "weight": request.POST.get("weight"),
            "height": request.POST.get("height"),
            "age": request.POST.get("age"),
            "sex": request.POST.get("sex"),
            "goal": request.POST.get("goal"),
            "activity": request.POST.get("activity"),
            "time_in_hours_activity": request.POST.get("time_in_hours_activity"),
            "time_from_last_eating": request.POST.get("time_from_last_eating"),
        }

        # Check if all required fields are present
        missing_fields = [field for field in required_fields if not data[field]]
        if missing_fields:
            raise ValueError(f"Missing required form fields: {', '.join(missing_fields)}")

        return data

    # Example usage:
    try:
        form_data = get_form_data(request)
        # Process the form data here (e.g., save to session or database)
        print(f"Successfully extracted form data: {form_data}")
    except ValueError as e:
        print(f"Error: {e}")
    # Validate and convert data types
    data = get_form_data(request)

    weight = float(data["weight"])
    height = float(data['height'])
    age = int(data['age'])
    time_in_hours_activity = float(data['time_in_hours_activity'])
    time_from_last_eating = float(data['time_from_last_eating'])
    sex = data['sex']
    activity  = data['activity']
    goal = data['goal']

    # Create Calories instance and calculate burned calories
    calories_model = Calories(
        weight=weight,
        sex=sex,
        age=age,
        height=height,
        activity=activity,
        time_in_hours_activity=time_in_hours_activity,
        time_from_last_eating=time_from_last_eating,
    )
    calories_burned = calories_model.get_calories_burn()

    # Store calories burned in session for use in index.html
    request.session['calories_burned'] = calories_burned
    meal_planner = MealPlanner(
        weight=weight,
        calories_burned=calories_burned,
        goal=goal  # or "lose_weight"
    )


    meal_plan = meal_planner.calculate_meal()
    print(meal_plan)


    # Initialize the RecommendationModel
    recommendation_model =  Recomendationmodel(file_path="Sources/epi_r.csv")

    # Read the recipe data
    try:
        recommendation_model.read_csv()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        recommendation_model = None

    # Filter the data (if applicable)
    if recommendation_model:
        try:
            recommendation_model.filter_data()
        except Exception as e:
            print(f"Error filtering data: {e}")

    # Generate recipe recommendations

    recommendation_model.recipe_recommend(
                number_of_dishes=3,
                number_of_candidates=3,
                nut_conf=meal_plan)



    recommendation_model.get_text()

    print( recommendation_model.text )
    # Redirect to index.html or another page showing calories burned
    return render(request, 'Site/recommendations.html', {
        'calories_burned': calories_burned,
        'weight': weight,
        'recommendation': recommendation_model.text,
        'height': height,
        'nutrients': meal_plan,
        'age': age,
        'sex': sex,
        'goal': goal,
        'activity': activity,
        'time_in_hours_activity': time_in_hours_activity,
        'time_from_last_eating': time_from_last_eating,
    })


# View for the recommendation page
