import os
import csv
from datetime import datetime
import platform  # For detecting the operating system

def calculate_bmi(weight, height_cm):
    """Calculate BMI given weight in kg and height in cm and categorize it."""
    height_m = height_cm / 100.0
    bmi = weight / (height_m ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi <= 24.9:
        category = "Normal weight"
    elif 25 <= bmi <= 29.9:
        category = "Overweight"
    else:
        category = "Obesity"
    return bmi, category

class FitnessApp:
    def __init__(self):
        self.documents_path = self.get_documents_path()
        self.folder_path = self.ensure_folder_exists()
        print("\033[95m--- Welcome to the Fitness Tracker App! ---\033[0m")
        self.user_info = self.input_user_info()  # Collect and display BMI info at startup
        self.body_parts = ["Chest", "Back", "Arms", "Shoulders", "Legs"]
        self.exercises = {
            "Chest": [
                "Incline Smith Press", "Close Grip Flat Press", "Wide Grip Flat Press",
                "Decline Chest Press", "Pec Deck Fly", "High-To-Low Cable Fly",
                "Mid Cable Fly", "Low-To-High Cable Fly", "Bench Press", "Incline Machine Press"
            ],
            "Back": [
                "Lat Pull Down", "Lat Pull Over", "Seated Lat Pull Over",
                "Chest Supported Row", "Chest Supported T-Bar Row", "Rear Delts Fly",
                "Face Pulls", "Hyper-extensions", "Single Cable Lat Pull Over",
                "Barbell Row", "Cable Rows"
            ],
            "Arms": [
                "Bicep Curl (Free Weights)", "Hammer Curls (Free Weights)", "Bicep Curl (Cables)",
                "Bicep Curls (Machine)", "Hammer Curls (Cable)", "Tricep Pushdown (Machine)",
                "Tricep Pushdown (Rope)", "Tricep Pushdown (V-Bar)", "Tricep Pushdown (Easy Bar)",
                "Tricep Pushdown (Straight Bar)", "Single Tricep Pushdown", "Straight Bar Cable Curl",
                "Uni-Lateral Cable Curl", "Wrist Curls"
            ],
            "Shoulders": [
                "Lateral Raises (Free Weights)", "Cable Lateral Raise", "Machine Lateral Raise",
                "Shoulder Press Machine", "Rear Delt Machine", "Cable Rear Delt"
            ],
            "Legs": [
                "Leg Press", "Hack Squat", "Bulgarian Split Squat", "Leg Extension",
                "Hamstring Curl Machine", "Hamstring Curl (Free Weights)", "Abductors",
                "Standing Calf Raise", "Seated Calf Raise", "RDL's"
            ]
        }

    @staticmethod
    def get_documents_path():
        """Returns the path to the user's Documents directory."""
        return os.path.join(os.path.expanduser("~"), 'Documents')

    def ensure_folder_exists(self):
        """Ensures the 'Gym Progress' folder exists, creates it if it does not."""
        folder_path = os.path.join(self.documents_path, 'Gym Progress')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print("\033[92mSuccessfully created directory:\033[0m", folder_path)
        return folder_path

    def input_user_info(self):
        """Prompt the user for height and weight, calculate BMI, and categorize it."""
        while True:
            try:
                height_cm = float(input("\nEnter your height in cm: "))
                weight_kg = float(input("Enter your weight in kg: "))
                if height_cm > 0 and weight_kg > 0:
                    bmi, category = calculate_bmi(weight_kg, height_cm)
                    print(f"\033[96mYour BMI is: {bmi:.2f} ({category})\033[0m")  # BMI formatted to two decimal places
                    return {"height_cm": height_cm, "weight_kg": weight_kg, "BMI": bmi, "BMI Category": category}
                else:
                    print("\033[91mPlease enter positive values for height and weight.\033[0m")
            except ValueError:
                print("\033[91mInvalid input. Please enter valid numbers.\033[0m")
                
    def save_fitness_data(self, data):
        """Saves the fitness data to a file named with today's date in the 'Gym Progress' folder."""
        today = datetime.now().strftime("%Y-%m-%d")
        file_extension = 'csv' if platform.system() != 'Windows' else 'xls'
        filename = f"{today}.{file_extension}"
        file_path = os.path.join(self.folder_path, filename)

        headers = ['Date', 'Height (cm)', 'Weight (kg)', 'BMI', 'BMI Category', 'Trained Body Part', 'Exercise', 'Weight (kg)', 'Reps', 'Sets']
        file_exists = os.path.isfile(file_path)

        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)
            for entry in data:
                writer.writerow([entry[0], self.user_info['height_cm'], self.user_info['weight_kg'], self.user_info['BMI'], self.user_info['BMI Category']] + entry[1:])

        print("\033[92mData successfully saved to:\033[0m", file_path)

    def prompt_yes_no(self, message):
        """Prompts a yes/no question and returns True for 'yes' or 'y', False for 'no' or 'n'."""
        while True:
            response = input(message + " (\033[94myes/y\033[0m or \033[91mno/n\033[0m): ").lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("\033[91mInvalid input. Please enter 'yes', 'y', 'no', or 'n'.\033[0m")

    def input_body_parts_and_exercises(self):
        """Allows the user to select multiple body parts they trained and the specific exercises."""
        print("\n\033[95m--- Select Body Parts You Trained ---\033[0m")
        for i, part in enumerate(self.body_parts, start=1):
            print(f"\033[93m{i}. {part}\033[0m")
        parts_choice = input("Enter the numbers of the body parts you trained, separated by commas: ")
        selected_parts = sorted(set(parts_choice.split(',')), key=int)  # Sort numerically and remove duplicates

        exercises_data = []
        for part_index in selected_parts:
            if part_index.isdigit() and 1 <= int(part_index) <= len(self.body_parts):
                part = self.body_parts[int(part_index) - 1]
                while True:
                    print(f"\n\033[96m--- Select Exercises for {part} ---\033[0m")
                    for idx, ex in enumerate(self.exercises[part], start=1):
                        print(f"\033[94m{idx}. {ex}\033[0m")
                    ex_choice = input("Enter the number of the exercise you performed: ")
                    if ex_choice.isdigit() and 1 <= int(ex_choice) <= len(self.exercises[part]):
                        exercise = self.exercises[part][int(ex_choice) - 1]
                        while True:
                            try:
                                weight = float(input("Enter the weight used (in kg): "))
                                reps = int(input("Enter the number of reps: "))
                                sets = int(input("Enter the number of sets: "))
                                if weight > 0 and reps > 0 and sets > 0:
                                    break
                                else:
                                    print("\033[91mPlease enter positive numbers for weight, reps, and sets.\033[0m")
                            except ValueError:
                                print("\033[91mInvalid input. Please enter valid numbers.\033[0m")
                        exercises_data.append([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), part, exercise, weight, reps, sets])
                        
                        more = self.prompt_yes_no("Add another exercise for the same body part?")
                        if not more:
                            break
            else:
                print("\033[91mInvalid body part selection. Please select a valid number.\033[0m")
        return exercises_data

    def main_loop(self):
        while True:
            data = self.input_body_parts_and_exercises()
            if data:
                self.save_fitness_data(data)
                another = self.prompt_yes_no("Would you like to enter exercises for another set of body parts?")
                if not another:
                    break
            else:
                print("\033[91mSomething went wrong, please start over.\033[0m")

if __name__ == "__main__":
    app = FitnessApp()
    app.main_loop()
