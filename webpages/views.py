import io
from django.shortcuts import render
from django.http import HttpResponse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from io import BytesIO
import base64


def home(request):
    return render(request, 'index.html')


def report(request):
    global df
    if request.method == 'POST':
        file = request.FILES['csvfile']

        if file.content_type == 'application/vnd.ms-excel':

            df = pd.read_csv(file)
            print("DF --->>>", type(df))

            global numerical
            global categorical
            numerical = df.select_dtypes(include=['int64']).columns.tolist()+df.select_dtypes(include=['float64']).columns.tolist(
            )+df.select_dtypes(include=['int32']).columns.tolist()+df.select_dtypes(include=['float32']).columns.tolist()
            categorical_temp = df.select_dtypes(
                include=['object']).columns.tolist()
            dict_check = {}
            categorical = []

            for i in categorical_temp:
                for j in range(0, 10):
                    if(type(df[i][j]) != np.float):
                        dict_check[i] = df[i][j][0].isdigit()
                        break

            for col in dict_check:
                if(dict_check[col] == False):
                    categorical.append(col)
                else:
                    # convertinng string type to float
                    # take of 55.6 ... and remove space from beginning
                    for j in range(0, df.count()[0]+df.isnull().sum()[0]):
                        if(type(df[col][j]) == np.float):
                            print("", end="")
                        else:
                            df[col][j] = df[col][j].lstrip()
                            for i in range(0, len(df[col][j])):
                                if((df[col][j][i].isdigit() == False)):
                                    if(df[col][j][i] == "."):
                                        print("", end="")
                                    else:
                                        df[col][j] = df[col][j][0:i]
                                        break

                            if(df[col][j] == ''):
                                df[col][j] = np.NaN

                            else:
                                df[col][j] = float(df[col][j])
                    numerical.append(col)

            numericalValues = []
            categoricalValues = []

            for i in numerical:
                single = {
                    'name': (i),
                    'count': (df[i].count()),
                    'missNo': (df[i].isnull().sum()),
                    'missPer': (df[i].isnull().sum()*100 /
                                (df[i].count()+df[i].isnull().sum())),
                    'mean': (df[i].mean()),
                    'median': (df[i].median()),
                    'mode': (df[i].mode()[0]),
                    'var': (df[i].std()*df[i].std()),
                    'std': (df[i].std()),
                    'min': (df[i].min()),
                    'max': (df[i].max()),
                    'q1': (df[i].quantile(0.25)),
                    'q2': (df[i].quantile(0.5)),
                    'q3': (df[i].quantile(0.75)),
                    'iqr': (df[i].quantile(0.75)-df[i].quantile(0.25)),
                    'kurtosis': (df[i].kurtosis())
                }
                numericalValues.append(single)
                single = {}

            for i in categorical:
                single = {
                    'name': (i),
                    'count': (df[i].count()),
                    'missNo': (df[i].isnull().sum()),
                    'missPer': (df[i].isnull().sum()*100 /
                                (df[i].count()+df[i].isnull().sum())),
                    'mode': (df[i].mode()[0])
                }
                categoricalValues.append(single)
                single = {}

            data = {
                'variables': len(df.columns.tolist()),
                'observations': df.count()[0]+df.isnull().sum()[0],
                'rows': df[df.duplicated()].count()[0],
                'numCols': len(df.select_dtypes(include=['int64']).columns.tolist())+len(df.select_dtypes(include=['float64']).columns.tolist()),
                'catCols': len(df.select_dtypes(include=['object']).columns.tolist()),
                'numericalValues': numericalValues,
                'categoricalValues': categoricalValues,
                'numerical': numerical,
                'df': df,
            }

        else:
            return HttpResponse("Please upload a csv file")

    return render(request, 'report.html', data)


def midpair(request):
    return render(request, 'loaders/pairload.html')


def midheat(request):
    return render(request, 'loaders/midheat.html')


def midscatter(request):
    return render(request, 'loaders/midscatter.html')


def midline(request):
    return render(request, 'loaders/midline.html')


def midhistogram(request):
    return render(request, 'loaders/midhistogram.html')


def midboxplot(request):
    return render(request, 'loaders/midboxplot.html')


def middensity(request):
    return render(request, 'loaders/middensity.html')


def midcount(request):
    return render(request, 'loaders/midcount.html')


def midpie(request):
    return render(request, 'loaders/midpie.html')


def sample(request):
    data = {
        'head': df.head()
    }
    return render(request, 'sample.html', data)


def pairplot(request):
    try:
        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 6))
        sns.pairplot(df)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_png = buffer.getvalue()
        pair = base64.b64encode(img_png)
        pair = pair.decode('utf-8')
        buffer.close()
        data = {
            'pairplot': pair
        }
        return render(request, 'graphs/multivariate/pairplot.html', data)
    except:
        return HttpResponse("Not possible to plot Pairplot")


def heatmap(request):
    try:
        plt.switch_backend('AGG')
        plt.figure(figsize=(10, 6))
        sns.heatmap(data=df.corr(), annot=True)
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img_png = buffer.getvalue()
        heat = base64.b64encode(img_png)
        heat = heat.decode('utf-8')
        buffer.close()
        data = {
            'heatmap': heat
        }
        return render(request, 'graphs/multivariate/correlation_heatmap.html', data)
    except:
        return HttpResponse("Not possible to plot Pairplot")


def scatterplot(request):
    scatterplots = []
    for i in numerical:
        for j in numerical:
            try:
                plt.switch_backend('AGG')
                plt.figure(figsize=(10, 5))
                sns.scatterplot(data=df, x=i, y=j)
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_png = buffer.getvalue()
                heat = base64.b64encode(img_png)
                heat = heat.decode('utf-8')
                buffer.close()
                scatterplots.append(heat)
            except:
                continue
    data = {
        'scatterplots': scatterplots
    }
    return render(request, 'graphs/bivariate/scatterplot.html', data)


def lineplot(request):
    lineplots = []
    for i in numerical:
        for j in numerical:
            try:
                plt.switch_backend('AGG')
                plt.figure(figsize=(10, 5))
                sns.lineplot(data=df, x=i, y=j)
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_png = buffer.getvalue()
                heat = base64.b64encode(img_png)
                heat = heat.decode('utf-8')
                buffer.close()
                lineplots.append(heat)
            except:
                continue
    data = {
        'lineplots': lineplots
    }
    return render(request, 'graphs/bivariate/lineplots.html', data)


def histogram(request):
    # plt.figure(figsize=(10, 5))
    histograms = []
    for i in numerical:
        try:
            plt.switch_backend('AGG')
            sns.histplot(data=df, x=i)
            plt.xlabel(i)
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_png = buffer.getvalue()
            heat = base64.b64encode(img_png)
            heat = heat.decode('utf-8')
            buffer.close()
            histograms.append(heat)
        except:
            continue
    data = {
        'histograms': histograms
    }
    return render(request, 'graphs/univariate/histogram.html', data)


def boxplot(request):
    boxplots = []
    for i in numerical:
        try:
            plt.switch_backend('AGG')
            plt.figure(figsize=(10, 5))
            sns.boxplot(df[i])
            plt.xlabel(i)
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_png = buffer.getvalue()
            heat = base64.b64encode(img_png)
            heat = heat.decode('utf-8')
            buffer.close()
            boxplots.append(heat)
        except:
            continue
    data = {
        'boxplots': boxplots
    }
    return render(request, 'graphs/univariate/boxplot.html', data)


def density(request):
    densitys = []
    for i in numerical:
        try:
            plt.switch_backend('AGG')
            plt.figure(figsize=(10, 5))
            sns.distplot(df[i])
            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_png = buffer.getvalue()
            heat = base64.b64encode(img_png)
            heat = heat.decode('utf-8')
            buffer.close()
            densitys.append(heat)
        except:
            continue
    data = {
        'densitys': densitys
    }
    return render(request, 'graphs/univariate/density.html', data)


def count(request):
    counts = []
    for i in categorical:
        try:
            if df[i].value_counts().count() < 12:
                plt.switch_backend('AGG')
                plt.figure(figsize=(10, 5))
                sns.countplot(y=df[i])
                plt.legend()
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_png = buffer.getvalue()
                heat = base64.b64encode(img_png)
                heat = heat.decode('utf-8')
                buffer.close()
                counts.append(heat)
        except:
            continue
    data = {
        'counts': counts
    }
    return render(request, 'graphs/univariate/count.html', data)


def pie(request):
    count_pie = []
    count = []
    pies = []
    for i in categorical:
        try:
            count_pie = df[i].value_counts()
            index_col = list(df[i].value_counts().index)
            for j in count_pie:
                count.append(j)
            if (df[i].value_counts().count() < 10):
                plt.switch_backend('AGG')
                plt.figure(figsize=(10, 5))
                plt.pie(count, labels=index_col)
                plt.legend()
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                img_png = buffer.getvalue()
                heat = base64.b64encode(img_png)
                heat = heat.decode('utf-8')
                buffer.close()
                pies.append(heat)
            count.clear()
            index_col.clear()
        except:
            continue
    data = {
        'pies': pies
    }
    return render(request, 'graphs/univariate/pie.html', data)
