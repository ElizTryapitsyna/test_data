import pandas as pd

# Загрузка данных из файла data.xlsx
df = pd.read_excel('data.xlsx')

# Выбор нужных столбцов
selected_columns = df[['client_id', 'sum', 'status', 'sale', 'new/current', 'document','receiving_date']]

# Преобразование столбца receiving_date в формат datetime
date_format = '%d.%m.%Y'
#selected_columns.loc[:, 'receiving_date'] = pd.to_datetime(selected_columns['receiving_date'], format=date_format, errors='coerce')
selected_columns['receiving_date'] = pd.to_datetime(selected_columns['receiving_date'], format=date_format, errors='coerce')

#Сделкт до Июля 2021
index = selected_columns.index[selected_columns['status'] == 'Июль 2021'].tolist()[0]
jul_deals = selected_columns.iloc[:index]
jul_deals = jul_deals[
    (jul_deals['receiving_date'].dt.month >= 7) & 
    (jul_deals['receiving_date'].dt.day >= 1)
    ]
#Будем считать бонус каждой сделки
def bon_fu(filtered_data):
    bonus = []
    for i in range(filtered_data.shape[0]):
        if filtered_data['new/current'].iloc[i] == 'новая':
            bonus.append(filtered_data['sum'].iloc[i] * 0.07)
        elif filtered_data['status'].iloc[i] != 'ПРОСРОЧЕНО':
            if filtered_data['sum'].iloc[i] > 10000:
                bonus.append(filtered_data['sum'].iloc[i] * 0.05)
            else:
                bonus.append(filtered_data['sum'].iloc[i] * 0.03)
        else:
            bonus.append(0)
    return bonus

jul_deals['bonus'] = bon_fu(jul_deals)
print(jul_deals.groupby(['sale'])['bonus'].sum())