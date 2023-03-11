from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from authentification.models import Utilisateur, ContentTypeRestrictedFileField
from datetime import datetime
from plotly.offline import plot
import plotly.graph_objs as go
import plotly.express as px
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
import pandas as pd

# Mes graphiques
fig = go.Figure()
scatter = go.Scatter(x=[0,1,2,3], y=[0,1,2,3],
                     mode='lines', name='test',
                     opacity=0.8, marker_color='green')
fig.add_trace(scatter)
plt_div = plot(fig, output_type='div')

df2 = px.data.iris() # iris is a pandas DataFrame
fig2 = px.scatter(df2, x="sepal_width", y="sepal_length", title="Scatter plot")
graph2 = plot(fig2, output_type='div')


df3 = px.data.tips()
fig3 = px.box(df3, x="time", y="total_bill", title="Boîte à moustache")
graph3 = plot(fig3, output_type='div')

z = [[.1, .3, .5, .7, .9],
     [1, .8, .6, .4, .2],
     [.2, 0, .5, .7, .9],
     [.9, .8, .4, .2, 0],
     [.3, .4, .5, .7, 1]]

fig4 = px.imshow(z, text_auto=True)
graph4 = plot(fig4, output_type='div')

# Clustering
# DBScan

dfPenguins = pd.read_csv(fichier)
X = dfPenguins[dfPenguins.describe().columns].dropna().values

X = StandardScaler().fit_transform(X)

db = DBSCAN().fit(X)
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise_ = list(labels).count(-1)
#Homogeneity = metrics.homogeneity_score(labels_true, labels)



def inscription(request):
    message = ""
    if request.method == "POST":
        if request.POST["motdepasse1"] == request.POST["motdepasse2"]:
            modelUtilisaleur = get_user_model()
            identifiant = request.POST["identifiant"]
            motdepasse = request.POST["motdepasse1"]
            utilisateur = modelUtilisaleur.objects.create_user(username=identifiant,
                                                       password=motdepasse)
            return redirect("connexion")
        else:
            message = "⚠️ Les deux mots de passe ne concordent pas ⚠️"
    return render(request, "inscription.html", {"message" : message})

def connexion(request):
    # La méthode POSt est utilisé quand des infos
    # sont envoyées au back-end
    # Autrement dit, on a appuyé sur le bouton
    # submit
    message = ""
    if request.method == "POST":
        identifiant = request.POST["identifiant"]
        motdepasse = request.POST["motdepasse"]
        utilisateur = authenticate(username = identifiant,
                                   password = motdepasse)
        if utilisateur is not None:
            login(request, utilisateur)
            return redirect("index")
        else:
            message = "Identifiant ou mot de passe incorrect"
            return render(request, "connexion.html", {"message": message})
    # Notre else signifie qu'on vient d'arriver
    # sur la page, on a pas encore appuyé sur le
    # bouton submit
    else:
        return render(request, "connexion.html")

def deconnexion(request):
    logout(request)
    return redirect("connexion")

def suppression(request, id):
    utilisateur = Utilisateur.objects.get(id=id)
    logout(request)
    utilisateur.delete()
    return redirect("connexion")

@login_required
def index(request):
    if request.method == 'POST':
        form = ContentTypeRestrictedFileField(request.POST, request.FILES)
        file=request.FILES['file']
        user = Utilisateur()
        return HttpResponse(str(form) + 'est télérchagé')
    context = {"n_clusters_" : n_clusters_,
               "n_noise_" : n_noise_,
               "graphique": plt_div,
               "graph2": graph2,
               "graph3": graph3,
               "graph4": graph4
               }
    return render(request, "index.html", context)
