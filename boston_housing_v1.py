
# Load libraries
import numpy as np
import pylab as pl
import scipy.stats as stats
from sklearn import datasets,grid_search
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, make_scorer, mean_absolute_error
from sklearn.grid_search import GridSearchCV

def load_data():
    boston = datasets.load_boston()
         
    #global city_data
    city_data = boston
    return boston
    
#load_data()

def explore_city_data(city_data):
    """Calculate the Boston housing statistics."""

    # Get the labels and features from the housing data
    housing_prices = city_data.target
    housing_features = city_data.data
    #print (housing_prices)
    #print (housing_features)
    ###################################
    ### Step 1. YOUR CODE GOES HERE ###
    ###################################

    # Please calculate the following values using the Numpy library
    # Size of data (number of houses)?
    houses = np.shape(housing_features)
    print "number of houses = " + str(houses[0])
    # Number of features?
    print "number of features = " + str(houses[1])
    # Minimum price?
    print "Minimum price = " + str(np.min(housing_prices))
    
    # Maximum price?
    print "Maximum price = " + str(np.max(housing_prices))
    # Calculate mean price?
    print "Mean price of population= " + str(np.mean(housing_prices))
    # Calculate median price?
    print "Median price of population = " + str(np.median(housing_prices))
    # Calculate standard deviation?
    print "Standard deviation of population = " + str(np.std(housing_prices))
    
#explore_city_data(city_data)

def split_data(city_data):
    """Randomly shuffle the sample set. Divide it into 70 percent training and 30 percent testing data."""

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target
    global X_train
    global X_test
    global y_train
    global y_test
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30,     _state=42)
    ###################################
    ### Step 2. YOUR CODE GOES HERE ###
    ###################################
    
    print X_train.shape
    print X_test.shape
    print y_train.shape
    print y_test.shape
    return X_train, y_train, X_test, y_test

    
#split_data(city_data)

def performance_metric(label, prediction):
    """Calculate and return the appropriate error performance metric."""

    ###################################
    ### Step 3. YOUR CODE GOES HERE ###
    ###################################

    return mean_squared_error(label, prediction)
    #return mean_absolute_error(label, prediction)

    # The following page has a table of scoring functions in sklearn:
    # http://scikit-learn.org/stable/modules/classes.html#sklearn-metrics-metrics
    pass

def learning_curve(depth, X_train, y_train, X_test, y_test):
    """Calculate the performance of the model after a set of training data."""

    # We will vary the training set size so that we have 50 different sizes
    sizes = np.round(np.linspace(1, len(X_train), 50))
    train_err = np.zeros(len(sizes))
    test_err = np.zeros(len(sizes))


    print "Decision Tree with Max Depth: "
    print depth

    for i, s in enumerate(sizes):
        
        # Create and fit the decision tree regressor model
        regressor = DecisionTreeRegressor(max_depth=depth)
        regressor.fit(X_train[:s], y_train[:s])

        # Find the performance on the training and testing set
        train_err[i] = performance_metric(y_train[:s], regressor.predict(X_train[:s]))
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))
        

    # Plot learning curve graph
    learning_curve_graph(sizes, train_err, test_err)
    
def learning_curve_graph(sizes, train_err, test_err):
    """Plot training and test error as a function of the training size."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Training Size')
    pl.plot(sizes, test_err, lw=2, label = 'test error')
    pl.plot(sizes, train_err, lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Training Size')
    pl.ylabel('Error')
    pl.show()
    

def model_complexity(X_train, y_train, X_test, y_test):
    """Calculate the performance of the model as model complexity increases."""

    print "Model Complexity: "

    # We will vary the depth of decision trees from 2 to 25
    max_depth = np.arange(1, 25)
    train_err = np.zeros(len(max_depth))
    test_err = np.zeros(len(max_depth))

    for i, d in enumerate(max_depth):
        # Setup a Decision Tree Regressor so that it learns a tree with depth d
        regressor = DecisionTreeRegressor(max_depth=d)

        # Fit the learner to the training data
        regressor.fit(X_train, y_train)

        # Find the performance on the training set
        train_err[i] = performance_metric(y_train, regressor.predict(X_train))

        # Find the performance on the testing set
        test_err[i] = performance_metric(y_test, regressor.predict(X_test))

    # Plot the model complexity graph
    model_complexity_graph(max_depth, train_err, test_err)
    
def model_complexity_graph(max_depth, train_err, test_err):
    """Plot training and test error as a function of the depth of the decision tree learn."""

    pl.figure()
    pl.title('Decision Trees: Performance vs Max Depth')
    pl.plot(max_depth, test_err, lw=2, label = 'test error')
    pl.plot(max_depth, train_err, lw=2, label = 'training error')
    pl.legend()
    pl.xlabel('Max Depth')
    pl.ylabel('Error')
    pl.show()
    
def fit_predict_model(city_data):
    """Find and tune the optimal model. Make a prediction on housing data."""

    # Get the features and labels from the Boston housing data
    X, y = city_data.data, city_data.target

    # Setup a Decision Tree Regressor
    regressor = DecisionTreeRegressor()

    parameters = {'max_depth':(1,2,3,4,5,6,7,8,9,10)}

    ###################################
    ### Step 4. YOUR CODE GOES HERE ###
    ###################################

    # 1. Find an appropriate performance metric. This should be the same as the
    # one used in your performance_metric procedure above:
    # http://scikit-learn.org/stable/modules/generated/sklearn.metrics.make_scorer.html
    scoring_func = make_scorer(performance_metric,greater_is_better=False)
    
    # 2. We will use grid search to fine tune the Decision Tree Regressor and
    # obtain the parameters that generate the best training performance. Set up
    # the grid search object here.
    # http://scikit-learn.org/stable/modules/generated/sklearn.grid_search.GridSearchCV.html#sklearn.grid_search.GridSearchCV
    bestparameterlist = []   
    for num in range (1,10):
        reg = grid_search.GridSearchCV(regressor, parameters,scoring = scoring_func)
    # Fit the learner to the training data to obtain the best parameter set
        #print "Final Model: "
        print reg.fit(X, y)
        print "Best fit parameter = " + str(reg.best_params_)
        #best = reg.best_params_['max_depth']
        bestparameterlist.append(reg.best_params_['max_depth'])
    counts = np.bincount(bestparameterlist)
    bestparameter = np.argmax(counts)
    print (type(bestparameter))
    print "best parameterlist " + str(bestparameterlist)
    print "best parameter from above list is " + str(bestparameter)
    
    reg_new=DecisionTreeRegressor(max_depth = bestparameter)
    reg_new.fit(X, y)
   # y_predicted = reg_new.predict(X_test)    
   # mse_test = performance_metric(y_test, y_predicted)
    
    # Use the model to predict the output of a particular sample
    x = [11.95, 0.00, 18.100, 0, 0.6590, 5.6090, 90.00, 1.385, 24, 680.0, 20.20, 332.09, 12.13]
    y = reg_new.predict(x)
    print "House: " + str(x)
    print "Prediction: " + str(y)

#In the case of the documentation page for GridSearchCV, it might be the case that the example is just a demonstration of syntax for use of the function, rather than a statement about 
def main():
    """Analyze the Boston housing data. Evaluate and validate the
    performanance of a Decision Tree regressor on the housing data.
    Fine tune the model to make prediction on unseen data."""
    global city_data
    # Load data
    city_data = load_data()

    # Explore the data
    explore_city_data(city_data)

    # Training/Test dataset split
    X_train, y_train, X_test, y_test = split_data(city_data)

    # Learning Curve Graphs
    max_depths = [1,2,3,4,5,6,7,8,9,10]
    for max_depth in max_depths:
        learning_curve(max_depth, X_train, y_train, X_test, y_test)

    # Model Complexity Graph
    model_complexity(X_train, y_train, X_test, y_test)

    # Tune and predict Model
    fit_predict_model(city_data)


if __name__ == "__main__":
    main()