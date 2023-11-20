import atexit # For playing a sound when the program finishes
import numpy as np # For the data manipulation
import os # For running a command in the terminal
import platform # For getting the operating system name
import time # For the timer
from colorama import Style # For coloring the terminal
from sklearn import svm # For the SVM classifier
from sklearn import tree # For the decision tree classifier
from sklearn.ensemble import RandomForestClassifier # For the random forest classifier
from sklearn.metrics import classification_report # For the classification report
from sklearn.model_selection import GridSearchCV # For the grid search
from sklearn.naive_bayes import GaussianNB # For the Naive Bayes classifier
from sklearn.neighbors import KNeighborsClassifier # For the k-NN classifier
from sklearn.neural_network import MLPClassifier # For the MLP classifier
from sklearn.pipeline import Pipeline # For the pipeline
from sklearn.preprocessing import StandardScaler # For the standard scaler

# Macros:
class BackgroundColors: # Colors for the terminal
   CYAN = "\033[96m" # Cyan
   GREEN = "\033[92m" # Green
   YELLOW = "\033[93m" # Yellow
   RED = "\033[91m" # Red
   BOLD = "\033[1m" # Bold
   UNDERLINE = "\033[4m" # Underline
   CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Sound Constants:
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"}
SOUND_FILE = "./.assets/NotificationSound.wav" # The path to the sound file

# Constants:
INPUT_FILES = ["./", "./"] # The input files

# This function defines the command to play a sound when the program finishes
def play_sound():
   if os.path.exists(SOUND_FILE):
      if platform.system() in SOUND_COMMANDS: # If the platform.system() is in the SOUND_COMMANDS dictionary
         os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
      else: # If the platform.system() is not in the SOUND_COMMANDS dictionary
         print(f"{BackgroundColors.RED}The {BackgroundColors.CYAN}platform.system(){BackgroundColors.RED} is not in the {BackgroundColors.CYAN}SOUND_COMMANDS dictionary{BackgroundColors.RED}. Please add it!{Style.RESET_ALL}")
   else: # If the sound file does not exist
      print(f"{BackgroundColors.RED}Sound file {BackgroundColors.CYAN}{SOUND_FILE}{BackgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

# This function loads the data from the dataset files and returns the training and test sets
def load_data():
   print(f"{BackgroundColors.BOLD}{BackgroundColors.YELLOW}Remember to remove the header line from the dataset files. They should be in the format: {BackgroundColors.CYAN}label feature1 feature2 ... featureN{Style.RESET_ALL}")
   print(f"\n{BackgroundColors.GREEN}Loading data...{Style.RESET_ALL}")
   tr = np.loadtxt(f"{INPUT_FILES[0]}") # Load the training data
   ts = np.loadtxt(f"{INPUT_FILES[1]}") # Load the test data
   train_label = tr[:, 0] # The first column is the label
   test_label = ts[:, 0] # The first column is the label
   train_features_values = tr[:, 1:] # The second column to the last is the feature vector
   test_features_values = ts[:, 1:] # The second column to the last is the feature vector
   return train_features_values, train_label, test_features_values, test_label # Return the data

# This function creates a k-NN classifier and prints the classification report
def knn(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}1º {BackgroundColors.CYAN}K-NN Classifier{BackgroundColors.GREEN}.{Style.RESET_ALL}")
   start_time = time.time() # Start the timer
   neigh = KNeighborsClassifier(n_neighbors=1, metric="euclidean") # Instantiate the classifier
   neigh.fit(train_features_values, train_label) # Train the classifier
   y_pred = neigh.predict(test_features_values) # Predict the test set
   accuracy = neigh.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"N Neighbors": 1, "Metric": "Euclidean", "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function creates a Decision Tree classifier with grid search and prints the classification report
def decision_tree(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}2º {BackgroundColors.CYAN}Decision Tree Classifier{BackgroundColors.GREEN}.{Style.RESET_ALL}")
   start_time = time.time() # Start the timer
   clf = tree.DecisionTreeClassifier() # Instantiate the classifier
   clf.fit(train_features_values, train_label) # Train the classifier
   y_pred = clf.predict(test_features_values) # Predict the test set
   accuracy = clf.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"Criterion": "Gini", "Splitter": "Best", "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function creates a SVM classifier with grid search and prints the classification report
def svm_with_grid_search(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}3º {BackgroundColors.CYAN}Support Vector Machine Classifier with Grid Search{BackgroundColors.GREEN}.{Style.RESET_ALL}")
   start_time = time.time() # Start the timer
   C_range = 2. ** np.arange(-5, 15, 2) # The range of C values
   gamma_range = 2. ** np.arange(3, -15, -2) # The range of gamma values which defines the influence of a single training example
   k = ["rbf"] # The kernel

   # Instantiate the classifier with probability
   srv = svm.SVC(probability=True, kernel="rbf") # Instantiate the classifier
   ss = StandardScaler() # Instantiate the standard scaler
   pipeline = Pipeline([("scaler", ss), ("svm", srv)]) # Instantiate the pipeline

   # Define the parameters for the grid search
   param_grid = {
      "svm__C": C_range,
      "svm__gamma": gamma_range
   }

   # Perform Grid Search
   grid = GridSearchCV(pipeline, param_grid, n_jobs=-1, verbose=0) # Instantiate the grid search
   grid.fit(train_features_values, train_label) # Train the classifier

   # Retrieve the best model
   y_pred = grid.predict(test_features_values) # Predict the test set
   accuracy = grid.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"C": grid.best_params_["svm__C"], "Gamma": grid.best_params_["svm__gamma"], "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function creates a Multilayer Perceptron classifier and prints the classification report
def multilayer_perceptron(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}4º {BackgroundColors.CYAN}Artificial Neural Network/Multilayer Perceptron Classifier{BackgroundColors.GREEN}.{Style.RESET_ALL}")
   start_time = time.time() # Start the timer
   scaler = StandardScaler() # Instantiate the standard scaler
   train_features_values = scaler.fit_transform(train_features_values) # Scale the training features
   test_features_values = scaler.fit_transform(test_features_values) # Scale the test features
   clf = MLPClassifier(solver="adam", alpha=1e-5, hidden_layer_sizes=(500, 500, 500, 500), random_state=1) # Instantiate the classifier
   clf.fit(train_features_values, train_label) # Train the classifier
   y_pred = clf.predict(test_features_values) # Predict the test set
   accuracy = clf.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"Solver": "Adam", "Alpha": 1e-5, "Hidden Layer Sizes": (500, 500, 500, 500), "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function creates a Random Forest classifier and prints the classification report
def random_forest(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}5º {BackgroundColors.CYAN}Random Forest Classifier{BackgroundColors.GREEN}.{Style.RESET_ALL}")
   start_time = time.time() # Start the timer
   clf = RandomForestClassifier(n_estimators=10000, max_depth=30, random_state=1) # Instantiate the classifier
   clf.fit(train_features_values, train_label) # Train the classifier
   y_pred = clf.predict(test_features_values) # Predict the test set
   accuracy = clf.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"N Estimators": 10000, "Max Depth": 30, "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function trains the Naive Bayes classifier and prints the classification report
def naive_bayes_with_grid_search(train_features_values, train_label, test_features_values, test_label):
   print(f"{BackgroundColors.GREEN}6º {BackgroundColors.CYAN}Naive Bayes Classifier with Grid Search{BackgroundColors.GREEN}.{Style.RESET_ALL}")

   start_time = time.time() # Start the timer
   # Define the parameters for the grid search
   param_grid = {"var_smoothing": [1e-9, 1e-8, 1e-7, 1e-6, 1e-5]}

   # Instantiate Naive Bayes classifier
   nb = GaussianNB()

   # Instantiate GridSearchCV
   grid = GridSearchCV(nb, param_grid, cv=5, scoring="accuracy", verbose=0, n_jobs=-1)

   grid.fit(train_features_values, train_label) # Train the classifier
   y_pred = grid.predict(test_features_values) # Predict the test set
   accuracy = grid.score(test_features_values, test_label) # Calculate the accuracy
   execution_time = time.time() - start_time # Calculate the execution time

   return accuracy, {"Var Smoothing": grid.best_params_["var_smoothing"], "Execution Time": f"{execution_time:.5f} Seconds"} # Return the Accuracy and the Parameters

# This function sort the classifiers by accuracy
def sort_classifiers_execution(classifiers_execution):
   # Sort the classifiers by accuracy and return the sorted dictionary
   return dict(sorted(classifiers_execution.items(), key=lambda item: item[1][0], reverse=True))

# This function prints the execution time of the classifiers
def print_classifiers_execution(sorted_classifiers_execution):
   print(f"\n{BackgroundColors.GREEN}Classifiers Results:{BackgroundColors.CYAN}") # Print the classifiers results

   # loop through the classifiers name, accuracy and parameters
   for classifier, accuracy in sorted_classifiers_execution.items():
      print(f"{BackgroundColors.GREEN}{classifier}: {BackgroundColors.CYAN}{accuracy[0]*100:.2f}%{Style.RESET_ALL}")
      for parameter, value in accuracy[1].items():
         print(f"{BackgroundColors.GREEN}{parameter}: {BackgroundColors.CYAN}{value}{Style.RESET_ALL}")
      print(f"{Style.RESET_ALL}")

# This is the Main function
def main():
   print(f"{BackgroundColors.CLEAR_TERMINAL}{BackgroundColors.BOLD}{BackgroundColors.GREEN}Hello, World!{Style.RESET_ALL}") # Output the Welcome message

   train_features_values, train_label, test_features_values, test_label = load_data() # Load the data
   classifiers_execution = {} # Dictionary to store the classifiers execution time

   classifiers_execution["K-NN"] = knn(train_features_values, train_label, test_features_values, test_label) # Train the K-NN classifier
   classifiers_execution["Decision Tree"] = decision_tree(train_features_values, train_label, test_features_values, test_label) # Train the Decision Tree classifier
   classifiers_execution["Support Vector Machine"] = svm_with_grid_search(train_features_values, train_label, test_features_values, test_label) # Train the SVM classifier
   classifiers_execution["Multilayer Perceptron Classifier"] = multilayer_perceptron(train_features_values, train_label, test_features_values, test_label) # Train the ANN/MLP classifier
   classifiers_execution["Random Forest"] = random_forest(train_features_values, train_label, test_features_values, test_label) # Train the Random Forest classifier
   classifiers_execution["Naive Bayes"] = naive_bayes_with_grid_search(train_features_values, train_label, test_features_values, test_label) # Train the Naive Bayes classifier

   # Sort the classifiers by execution time
   classifiers_execution = sort_classifiers_execution(classifiers_execution)

   # Print the execution time
   print_classifiers_execution(classifiers_execution)

   print(f"{BackgroundColors.BOLD}{BackgroundColors.GREEN}Program finished.{Style.RESET_ALL}") # Output the end of the program message

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
	main() # Call the main function
