import pandas as pd
raw_data = {
        'subject_id': ['1', '2', '3', '4', '5'],
        'first_name': ['Alex', 'Amy', 'Allen', 'Alice', 'Ayoung'],
        'last_name': ['Anderson', 'Ackerman', 'Ali', 'Aoni', 'Atiches']}
df = pd.DataFrame(raw_data, columns = ['subject_id', 'first_name', 'last_name'])

print(len(df.loc[df['first_name']=='amy']))

print(int(True))
print(int(False))
# r = df.loc[df['first_name'] == 'Amy'].iloc[0]['f']
#
# print(r)
import os
root_path = os.path.dirname(__file__)
print(root_path)