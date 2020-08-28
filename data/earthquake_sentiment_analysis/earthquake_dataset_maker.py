import pandas as pd
if __name__ == "__main__":
    data = pd.read_csv("Cresci-SWDM15.csv", usecols=['text', 'disaster', 'class'])
    earthquake = data.loc[data['disaster'].isin([1, 2])]
    earthquake = earthquake[['text', 'class']].to_numpy()
    for entry in earthquake:
        if entry[1] == "no damage":
            entry[1] = "pos"
        else:
            entry[1] = "neg"
    earthquake = pd.DataFrame(data=earthquake)
    earthquake.columns = ['Content', 'Label']
    earthquake.to_csv("./earthquake_dataset_SA.csv", index=False)