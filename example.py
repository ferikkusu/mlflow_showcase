import os
import mlflow

from sklearn import tree
from sklearn.metrics import confusion_matrix

# dummy train data
x_train = [[0, 0], [1, 1]]
y_train = [0, 1]

x_test = [[0, 1], [1, 0], [0, 0], [1, 1]]
y_test = [0, 1, 0, 1]

# set dummy parameters
max_depth = 2
random_state = 42

# setup mlflow
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://localhost:9000"
os.environ["MLFLOW_S3_IGNORE_TLS"] = 'true'
os.environ["AWS_ACCESS_KEY_ID"] = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minioadmin"
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test_experiment")

# run experiment
with mlflow.start_run(run_name="test_run"):
    # log hyperparameters
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_param("random_state", random_state)

    # train classifier
    classifier = tree.DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    classifier = classifier.fit(x_train, y_train)

    # log classifier
    mlflow.sklearn.log_model(classifier, "example_model")

    # evaluate model
    y_pred = classifier.predict(x_test)
    metrics = confusion_matrix(y_test, y_pred)
    mlflow.log_metric(key="true_negatives", value=metrics[0, 0])
    mlflow.log_metric(key="false_positives", value=metrics[0, 1])
    mlflow.log_metric(key="false_negatives", value=metrics[1, 0])
    mlflow.log_metric(key="true_positives", value=metrics[1, 1])
