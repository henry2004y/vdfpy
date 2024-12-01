import vdfpy as vd
from vdfpy import cluster
import numpy as np
import pyvlasiator.plot
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

import pyvlasiator as vlasiator

filename = "D:/Research/Vlasiator/VDF_Classification/bulk.0000015.vlsv"

df = vd.collect_moments(filename)

cluster(df)

ds = vd.load_vlasiator(filename)

#ds.plot("proton/vg_v")

#ds.meshes["proton"]
#ncellswithVDF = int(ds.nodecellwithVDF[0].attrib["arraysize"])
#ds.read_vcells(1)
ds.init_cellswithVDF("proton")
cVDF = ds.meshes["proton"].cellwithVDF
ncellswithVDF = cVDF.size

range = np.linspace(ds.coordmin[0]+1, ds.coordmax[0]-1, 4)


# # Create a figure with two subfigures
# fig = plt.figure(figsize=(12, 4))
# subfigs = fig.subfigures(2, 1, wspace=0.07)

# axsTop = subfigs[0].subplots(1, 1, sharey=True)
# ds.plot("proton/vg_rho", axsTop)
# axsTop.set_xlabel("x [km]", fontsize=14)
# subfigs[0].suptitle("Line plot", fontsize=14)

# axsBot = subfigs[1].subplots(1, 4, sharex=True)
# for index, ax in enumerate(axsBot):
#     loc = (range[index], 0, 0)
#     ds.vdfslice(loc, ax, addcolorbar=False)
#     cidReq = ds.getcell(loc)
#     cidNearest = ds.getnearestcellwithvdf(cidReq)
#     l = ds.getcellcoordinates(cidNearest)
#     ax.set_title(f"x={l[0]:.1e}")

# # subfigs[1].suptitle("VDFs", fontsize=14)

# plt.show()


# fig, axs = plt.subplots(1, 4, figsize=(10, 2), constrained_layout=True)

# for index, ax in enumerate(axs):
#     loc = (range[index], 0, 0)
#     ds.vdfslice(loc, ax)

# plt.show()

## Clustering

data = []

for i, cid in enumerate(cVDF):
    feature = {}
    feature["n"] = ds.read_variable("proton/vg_rho", cid)
    v = ds.read_variable("proton/vg_v", cid)
    feature["v"] = np.linalg.norm(np.asarray(v), axis=-1)
    v = ds.read_variable("proton/vg_ptensor_diagonal", cid)
    feature["p"] = np.average(v)

    data.append(feature)
    
df = pd.DataFrame(data)

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

(n_samples, n_features) = df.shape
n_clusters = 4

print(f"# clusters: {n_clusters}; # samples: {n_samples}; # features {n_features}\n")


# from sklearn.pipeline import make_pipeline
# estimator = make_pipeline(StandardScaler(), kmeans).fit(df)
# estimator.fit_transform(df)

scaler = StandardScaler()
# scaler.fit(df)
# scaler.transform(df)
data_scaled = scaler.fit_transform(df)
df_scaled = pd.DataFrame(data_scaled)

kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=4, random_state=0)
kmeans.fit(df_scaled)

fig, ax = plt.subplots(figsize=(7, 5))

xrange = np.linspace(ds.coordmin[0]+1, ds.coordmax[0]-1, 48)
ylocs = np.zeros(48)
cdict = {0: 'darkgoldenrod', 1: 'slateblue', 2: 'limegreen', 3: 'darkgreen'}

for g in np.unique(kmeans.labels_):
    ix = np.where(kmeans.labels_ == g)
    ax.scatter(xrange[ix], ylocs[ix], c=cdict[g], label=g, s=30)
ax.legend(loc='upper center', fancybox=True, shadow=True, ncol=4)
ax.set_title('1D Shocktube, 4-class k-means')

plt.show()


# reduced_data = PCA(n_components=2).fit_transform(df_scaled)
# kmeans = KMeans(init="k-means++", n_clusters=n_clusters, n_init=4, random_state=0)
# kmeans.fit(reduced_data)

# # Step size of the mesh. Decrease to increase the quality of the VQ.
# h = 0.02  # point in the mesh [x_min, x_max]x[y_min, y_max].

# # Plot the decision boundary. For that, we will assign a color to each
# x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
# y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
# xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# # Obtain labels for each point in mesh. Use last trained model.
# Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# # Put the result into a color plot
# Z = Z.reshape(xx.shape)
# plt.figure(1)
# plt.clf()
# plt.imshow(
#     Z,
#     interpolation="nearest",
#     extent=(xx.min(), xx.max(), yy.min(), yy.max()),
#     cmap=plt.cm.Paired,
#     aspect="auto",
#     origin="lower",
# )

# plt.plot(reduced_data[:, 0], reduced_data[:, 1], "k.", markersize=2)
# # Plot the centroids as a white X
# centroids = kmeans.cluster_centers_
# plt.scatter(
#     centroids[:, 0],
#     centroids[:, 1],
#     marker="x",
#     s=169,
#     linewidths=3,
#     color="w",
#     zorder=10,
# )
# plt.title(
#     "K-means clustering on the digits dataset (PCA-reduced data)\n"
#     "Centroids are marked with white cross"
# )
# plt.xlim(x_min, x_max)
# plt.ylim(y_min, y_max)
# plt.xticks(())
# plt.yticks(())
# plt.show()