import matplotlib.pyplot as plt
import pandas as pd
import os, pathlib, shutil

def render(path_to_dataset, path_to_pngstore, dataset_name, username):
    df = pd.read_csv(path_to_dataset)
    cols = df.columns
    columns = []
    for i in cols:
        columns.append(i)
    columns.remove('Date')
    columns.remove('Time')
    os.mkdir(os.path.join(path_to_pngstore, username, dataset_name))
    i = 0
    labels = ['voltage', 'current', 'power', 'tempurature', 'pressure', 'humidity', 'gas', 'altitude', 'pm_greater_0-3', 'pm_greater_0-5', 'pm_greater_1-0', 'pm_greater_2-5', 'pm_greater_5-0', 'pm_greater_10-0', 'pm_1-0', 'pm_2-5', 'pm_10-0', 'AQI_2-5', 'AQI_10-0']
    try:
        for col in columns:
            plt.figure()
            plt.title(col)
            plt.plot(df['Time'], df[col])
            plt.savefig(pathlib.Path(os.path.join(path_to_pngstore, username, dataset_name, '{}.png'.format(labels[i]))))
            i+=1
    except FileExistsError:
        shutil.rmtree(os.path.join(path_to_pngstore, username, dataset_name))
        render(path_to_dataset, path_to_pngstore, dataset_name, username)
    except:
        raise ValueError()
