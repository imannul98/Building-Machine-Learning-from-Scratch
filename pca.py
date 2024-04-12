import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
rndr_type = 'jupyterlab+png'
pio.renderers.default = rndr_type


class PCA(object):

    def __init__(self):
        self.U = None
        self.S = None
        self.V = None

    def fit(self, X: np.ndarray) ->None:
        """		
		Decompose dataset into principal components by finding the singular value decomposition of the centered dataset X
		You may use the numpy.linalg.svd function
		Don't return anything. You can directly set self.U, self.S and self.V declared in __init__ with
		corresponding values from PCA. See the docstrings below for the expected shapes of U, S, and V transpose
		
		Hint: np.linalg.svd by default returns the transpose of V
		      Make sure you remember to first center your data by subtracting the mean of each feature.
		
		Args:
		    X: (N,D) numpy array corresponding to a dataset
		
		Return:
		    None
		
		Set:
		    self.U: (N, min(N,D)) numpy array
		    self.S: (min(N,D), ) numpy array
		    self.V: (min(N,D), D) numpy array
		"""
        X_centered = X - np.mean(X, axis=0)
        
        U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
        self.U = U 
        self.S = S 
        self.V = Vt

    def transform(self, data: np.ndarray, K: int=2) ->np.ndarray:
        """		
		Transform data to reduce the number of features such that final data (X_new) has K features (columns)
		Utilize self.U, self.S and self.V that were set in fit() method.
		
		Args:
		    data: (N,D) numpy array corresponding to a dataset
		    K: int value for number of columns to be kept
		
		Return:
		    X_new: (N,K) numpy array corresponding to data obtained by applying PCA on data
		
		Hint: Make sure you remember to first center your data by subtracting the mean of each feature.
		"""
        data=data-np.mean(data,axis=0)
        V=self.V[:K, :]
        X_new=np.dot(data,V.T)
        return X_new
        

    def transform_rv(self, data: np.ndarray, retained_variance: float=0.99
        ) ->np.ndarray:
        """		
		Transform data to reduce the number of features such that the retained variance given by retained_variance is kept
		in X_new with K features
		Utilize self.U, self.S and self.V that were set in fit() method.
		
		Args:
		    data: (N,D) numpy array corresponding to a dataset
		    retained_variance: float value for amount of variance to be retained
		
		Return:
		    X_new: (N,K) numpy array corresponding to data obtained by applying PCA on data, where K is the number of columns
		           to be kept to ensure retained variance value is retained_variance
		
		Hint: Make sure you remember to first center your data by subtracting the mean of each feature.
		"""
        data=data-np.mean(data,axis=0)
        cumulative_variance = np.cumsum(self.S**2) / np.sum(self.S**2)
        K = np.where(cumulative_variance >= retained_variance)[0][0] + 1
        return np.dot(data,self.V[:K,:].T)

    def get_V(self) ->np.ndarray:
        """		
		Getter function for value of V
		"""
        return self.V

    def visualize(self, X: np.ndarray, y: np.ndarray, fig_title) ->None:
        """		
		You have to plot three different scatterplots (2d and 3d for strongest 2 features and 2d for weakest 2 features)
        for this function. For plotting the 2d scatterplots, use your PCA implementation to reduce the dataset to 
        only 2 (strongest and later weakest) features. You'll need to run PCA on the dataset and then transform it 
        so that the new dataset only has 2 features.
		Create a scatter plot of the reduced data set and differentiate points that have different true labels using color using plotly.
		Hint: Refer to https://plotly.com/python/line-and-scatter/ for making scatter plots with plotly.
		Hint: We recommend converting the data into a pandas dataframe before plotting it. Refer to https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html for more details.
		Hint: To extract weakest features, consider the order of components returned in PCA.
		
		Args:
		    xtrain: (N,D) numpy array, where N is number of instances and D is the dimensionality of each instance
		    ytrain: (N,) numpy array, the true labels
		
		Return: None
		"""
        self.fit(X)
        X_strongest = self.transform(X, K=2)
        X_weakest = np.dot(X - np.mean(X, axis=0), self.V[-2:, :].T)
        
        df_strongest = pd.DataFrame(X_strongest, columns=['z1', 'z2'])
        df_strongest['Label'] = y
        
        df_weakest = pd.DataFrame(X_weakest, columns=['z1', 'z2'])
        df_weakest['Label'] = y
        
        fig_strongest = px.scatter(df_strongest, x='z1', y='z2', color='Label', title=f"{fig_title} - Strongest Features")
        fig_strongest.show()
        fig_weakest = px.scatter(df_weakest, x='z1', y='z2', color='Label', title=f"{fig_title} - Weakest Features")
        fig_weakest.show()
