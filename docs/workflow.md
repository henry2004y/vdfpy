# Workflow

`vdfpy` takes velocity distribution functions (VDFs) from observation and simulation data, and clusters the distributions using unsupervised machine learning algorithms from `sklearn` and other population packages. We provide uniform interfaces for data from different sources, and standard methods for training and evaluating the clustering performance. On the top level, the task is divided into several steps:

* Data preparation
  * Data collection
  * Data cleaning
  * Feature engineering
  * Data splitting
* Modeling
  * Hyperparameter tuning
  * Training
  * Predicting
  * Assessing performance
* Deployment
  * Deploy model
  * Monitor model performance
  * Improve model

## Data Preparation

Currently, we support VDF collection from MMS, Vlasiator, and FLEKS.

### Normalizing the data

When working with distance-based algorithms, like k-Means Clustering, we must normalize the data. If we do not normalize the data, variables with different scaling will be weighted differently in the distance formula that is being optimized during training. For example, if we were to include velocity [km/s] in the cluster, in addition to density [amu/cc] and pressure [nPa], density would have an outsized impact on the optimizations because its scale is significantly larger and wider than the bounded location variables.

We first set up training and test splits using `train_test_split` from `sklearn`.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(home_data[['latitude', 'longitude']], home_data[['median_house_value']], test_size=0.33, random_state=0)
```

Next, we normalize the training and test data using the `preprocessing.normalize` method from `sklearn`.

```python
from sklearn import preprocessing

X_train_norm = preprocessing.normalize(X_train)
X_test_norm = preprocessing.normalize(X_test)
```

`sklearn` provides several methods for data normalization.

## Modeling

### Fitting the model

For the first iteration, we will arbitrarily choose a number of clusters (referred to as k) of 3. Building and fitting models in `sklearn` is very simple. We will create an instance of `KMeans`, define the number of clusters using the `n_clusters` attribute, set `n_init`, which defines the number of iterations the algorithm will run with different centroid seeds, to "auto", and we will set the `random_state` to 0 so we get the same result each time we run the code.  We can then fit the model to the normalized training data using the `fit()` method.

```python
from sklearn import KMeans

kmeans = KMeans(n_clusters = 3, random_state = 0, n_init="auto")
kmeans.fit(X_train_norm)
```

Once the data are fit, we can access labels from the `labels_` attribute.

### Evaluating the model

Below, we visualize the data we just fit.

```python
sns.scatterplot(data = X_train, x = 'longitude', y = 'latitude', hue = kmeans.labels_)
```

We can evaluate performance of the clustering algorithm using a Silhouette score which is a part of `sklearn.metrics` where a lower score represents a better fit.???

```python
from sklearn.metrics import silhouette_score

silhouette_score(X_train_norm, kmeans.labels_, metric='euclidean')
```

### Choosing the best number of clusters

The weakness of k-means clustering is that we don’t know how many clusters we need by just running the model. We need to test ranges of values and make a decision on the best value of k. We typically make a decision using the Elbow method to determine the optimal number of clusters where we are both not overfitting the data with too many clusters, and also not underfitting with too few.

We create the below loop to test and store different model results so that we can make a decision on the best number of clusters.

```python
K = range(2, 8)
fits = []
score = []


for k in K:
    # train the model for current value of k on training data
    model = KMeans(n_clusters = k, random_state = 0, n_init='auto').fit(X_train_norm)
    
    # append the model to fits
    fits.append(model)
    
    # Append the silhouette score to scores
    score.append(silhouette_score(X_train_norm, model.labels_, metric='euclidean'))
```

Typically, as we increase the value of K, we see improvements in clusters and what they represent until a certain point. We then start to see diminishing returns or even worse performance. We can visually see this to help make a decision on the value of k by using an elbow plot where the y-axis is a measure of goodness of fit and the x-axis is the value of k.

```python
sns.lineplot(x = K, y = score)
```

We typically choose the point where the improvements in performance start to flatten or get worse.

### When will k-means cluster analysis fail?

K-means clustering performs best on data that are spherical. Spherical data are data that group in space in close proximity to each other either. This can be visualized in 2 or 3 dimensional space more easily. Data that aren’t spherical or should not be spherical do not work well with k-means clustering. For example, k-means clustering would not do well on the below data as we would not be able to find distinct centroids to cluster the two circles or arcs differently, despite them clearly visually being two distinct circles and arcs that should be labeled as such.
