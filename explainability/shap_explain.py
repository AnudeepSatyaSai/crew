import shap
import matplotlib.pyplot as plt

def explain_with_shap(model, X):
    """
    Explain model predictions using SHAP values.
    Returns SHAP values and summary plot.
    """
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    shap.summary_plot(shap_values, X)
    return shap_values

def partial_dependence_plot(model, X, feature):
    """
    Plot partial dependence of a feature.
    """
    shap.dependence_plot(feature, shap.Explainer(model, X)(X), X)
    plt.show() 