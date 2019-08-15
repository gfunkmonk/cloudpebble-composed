import numpy as n, pylab as p
from scipy import stats

class NetworkPCA:
    """PCA cases of interest  for observing stability in interaction networks.


        1) Primacy of centrality measures for dispersion; and
        2) precedence of symmetry over clustering;
        3) average of all basic centrality measures for first compoment
    """
    def __init__(self,network_measures,network_partitioning=None,tdir=".",tname="sample.png", measures="all"):
        # enable selection of measures input as string
        # through measures variable and exec() or eval() methods.
        self.M1=n.array(( network_measures.weighted_clusterings_,
                    network_measures.degrees_,
                    network_measures.weighted_directed_betweenness_
                    ))
        self.pca1=PCA(self.M1)
        self.M2=n.array(( network_measures.weighted_clusterings_,
                    network_measures.strengths_,
                    network_measures.in_strengths_,
                    network_measures.out_strengths_,
                    network_measures.degrees_,
                    network_measures.in_degrees_,
                    network_measures.out_degrees_,
                    network_measures.weighted_directed_betweenness_
                    ))
        self.pca2=PCA(self.M2)

        self.M3=n.array(( network_measures.weighted_clusterings_,
                    network_measures.strengths_,
                    network_measures.in_strengths_,
                    network_measures.out_strengths_,
                    network_measures.degrees_,
                    network_measures.in_degrees_,
                    network_measures.out_degrees_,
                    network_measures.weighted_directed_betweenness_,
                    network_measures.asymmetries,
                    network_measures.asymmetries_edge_mean,
                    network_measures.asymmetries_edge_std,
                    network_measures.disequilibrium,
                    network_measures.disequilibrium_edge_mean,
                    network_measures.disequilibrium_edge_std,
                    ))
        self.pca3=PCA(self.M3)
        if network_partitioning:
            self.pca1.plot(tname.replace(".","_1."),network_partitioning,tdir=tdir)
            self.pca2.plot(tname.replace(".","_2."),network_partitioning,tdir=tdir)
            self.pca3.plot(tname.replace(".","_3."),network_partitioning,tdir=tdir)

class PCA:
    """Apply PCA to incoming datatable M (metrics x observations)

    Usage
    =====

    Initialize with a n x m matrix of n metrics each with m observations
    >>> foo=n.random(100)
    >>> p1=n.vstack((foo,foo))
    >>> p2=n.vstack((-foo,foo))
    >>> p3=n.vstack((foo,-foo))
    >>> M=n.hstack((p1,p2,p3))
    >>> pca=g.PCA(M)

    See attributes for information about data:
    >>> pca.eig_values # for eigen values from greatest down
    >>> pca.eig_values_ # for a normalized eig_values
    >>> pca.eig_vectors # for eigen vectors of the eig_values
    >>> pca.eig_vectors_ # for a normalized eig_vectors
    >>> pca.C # for covariance matrix
    >>> pca.M # for initial data 
    >>> pca.x # final positions in the principal component
    >>> pca.y # final positions in second principal component
    >>> pca.plot() # to plot observations in initial and final spaces
    

    """
#    def __init__(self,*metrics,final_dimensions=2,draw=False):
    def __init__(self,final_dimensions=2,draw=False,*meterics):
        M=n.vstack(metrics)
        # zscore: # USE NUMPY.stats.zscore(M, axis=1, ddof=1)
        self.M_=M
        for i in range(M.shape[0]):
            if M[i].std():
                M[i]=(M[i]-M[i].mean())/M[i].std()
            else:
                M[i]=0.
        # convariance matrix:
        self.C=n.cov(M)
        self.M=M

        eig_values, eig_vectors = n.linalg.eig(self.C)
        # Ordering eigenvalues and eigenvectors
        args=n.argsort(eig_values)[::-1]
        self.eig_values=eig_values[args]
        self.eig_values_=100*self.eig_values/n.sum(n.abs(self.eig_values))
        self.eig_vectors=eig_vectors[:,args]
        self.eig_vectors_=n.array([100*self.eig_vectors[:,i]/n.abs(self.eig_vectors[:,i]).sum() for i in range(self.eig_vectors.shape[1])]).T
        # retaining only some eigenvectors
        self.feature_vec=self.eig_vectors[:,:final_dimensions]
        self.feature_vec_=n.array([100*self.feature_vec[:,i]/n.abs(self.feature_vec[:,i]).sum() for i in range(self.feature_vec.shape[1])]).T

        self.final_data=n.dot(M.T,self.feature_vec)
        self.x=self.final_data[:,0]
        self.y=self.final_data[:,1]


    def plot(self, tname="sample.png", network_partitioning=False,labels="full", tdir="."):
        p.clf()
        label1="PC1"
        label2="PC2"
        title="Vertex position in principal components (PCA)"
        if labels=="full":
            #foo=self.feature_vec[:,0]
            #foo_=("%.2f, "*len(foo)) % tuple(foo)
            foo=self.feature_vec_[:,0]
            foo__=("%.2f, "*len(foo)) % tuple(foo)
            label1+=" " + foo__

            #foo=self.feature_vec[:,1]
            #foo_=("%.2f, "*len(foo)) % tuple(foo)
            foo=self.feature_vec_[:,1]
            foo__=("%.2f, "*len(foo)) % tuple(foo)
            label2+=" " +foo__

            #foo=(self.eig_values[:4]/self.eig_values.sum())*100
            #foo_=r"$\lambda = $"+("%.2f, "*len(foo) % tuple(foo))
            foo=(self.eig_values_[:4])
            foo__=r"$\lambda = $"+("%.2f, "*len(foo) % tuple(foo))
            title+=" "+foo__

        p.xlabel(label1, fontsize=10)
        p.ylabel(label2, fontsize=10)
        #p.title(foo_)
        p.title(title)

        p.ylim(min(self.y)-1,max(self.y)+1)
        p.xlim(min(self.x)-1,max(self.x)+1)
        if not network_partitioning:
            p.plot(self.x,self.y,"go", ms=3.9,label="intermediary")
        else:
            n_periphery=   len(network_partitioning.sectorialized_agents__[0])
            n_intermediary=len(network_partitioning.sectorialized_agents__[1])
            n_hubs=        len(network_partitioning.sectorialized_agents__[2])
            p.plot(self.x[:n_periphery],self.y[:n_periphery],"bo", ms=3.9,label="perihpery")
            p.plot(self.x[n_periphery:n_periphery+n_intermediary],self.y[n_periphery:n_periphery+n_intermediary],"go", ms=3.9,label="intermediary")
            p.plot(self.x[-n_hubs:],self.y[-n_hubs:],"ro", ms=3.9,label="hubs")
        #p.legend()
        p.savefig("{}/{}".format(tdir,tname))
        x=self.M[0]
        y=self.M[1]
        p.clf()
        p.plot(x,y,"go", ms=3.9,label="intermediary")
        p.savefig("{}/Initial{}.png".format(tdir,tname))
