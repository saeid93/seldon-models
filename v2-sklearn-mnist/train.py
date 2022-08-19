# Original source code and more details can be found in:
# https://scikit-learn.org/stable/auto_examples/classification/plot_digits_classification.html

# Import datasets, classifiers and performance metrics
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn import datasets, svm
from sklearn.model_selection import train_test_split
import joblib


from functools import partial
import numpy as np

# The digits dataset
digits = datasets.load_digits()

# Create a classifier: a support vector classifier
reshape = partial(np.reshape, newshape=(-1, 64))
classifier = svm.SVC(gamma=0.001)
pipe = Pipeline([("reshape", FunctionTransformer(reshape)), ("classifier", classifier)])

# Split data into train and test subsets
X_train, X_test, y_train, y_test = train_test_split(
    digits.images, digits.target, test_size=0.5, shuffle=False
)

# We learn the digits on the first half of the digits
pipe.fit(X_train, y_train)

# Save model
model_file_name = "mnist-svm.joblib"
print(f"Saving model: {model_file_name}")
joblib.dump(pipe, model_file_name)
