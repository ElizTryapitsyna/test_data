import pandas as pd
import matplotlib.pyplot as plt

# Загрузка данных из файла data.xlsx
df = pd.read_excel('data.xlsx')

# Выбор нужных столбцов
selected_columns = df[['client_id', 'sum', 'status', 'sale','new/current', 'document','receiving_date']]

# Преобразование столбца receiving_date в формат datetime
date_format = '%d.%m.%Y'
#selected_columns.loc[:, 'receiving_date'] = pd.to_datetime(selected_columns['receiving_date'], format=date_format, errors='coerce')
selected_columns['receiving_date'] = pd.to_datetime(selected_columns['receiving_date'], format=date_format, errors='coerce')

def draw_graph(filtered_data):
    july_data = filtered_data.sort_values(by='receiving_date')
    revenue = [july_data['sum'].iloc[0]]
    for i in range(july_data.shape[0] - 1):
        revenue.append(july_data['sum'].iloc[i + 1] + revenue[i])
    # Построение графика изменения выручки за июль
    plt.figure(figsize=(10, 6))
    plt.plot(july_data['receiving_date'], revenue, marker='o')
    plt.title('Изменение выручки за июль')
    plt.xlabel('Дата')
    plt.ylabel('Выручка')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#Поиск самого эффективного менеджера
def most_ef_men(filtered_data):
    sales = filtered_data.groupby(['sale'])['sum'].sum().reset_index()
    sales = sales.sort_values(by='sum', ascending=False, ignore_index=True)
    return sales['sale'][0]
#Поиск преобладающего типа сделок
def most_frequent_type(filtered_data):
    most_common_type = filtered_data['new/current'].value_counts().idxmax()
    #most_common_count = filtered_data['new/current'].value_counts().max()
    return most_common_type
#Поиск количества оригиналов
def orig(filtered_data):
    orig_contract = filtered_data[filtered_data['document'] == 'оригинал'].shape[0]
    return orig_contract

# Фильтрация строк по месяцу и статусу (июль)
filtered_data = selected_columns[
    (selected_columns['receiving_date'].dt.month == 7) &
    (selected_columns['status'] != 'ПРОСРОЧЕНО')
]
# Подсчет суммы по столбцу sum
sum_total = filtered_data['sum'].sum()

#Сентябрьские сделки
sept_deals = selected_columns[selected_columns['receiving_date'].dt.month == 9]

#Октябрьские сделки
oct_deals = selected_columns[selected_columns['receiving_date'].dt.month == 10]

#Майские сделки
index = selected_columns.index[selected_columns['status'] == 'Июнь 2021'].tolist()[0]
may_deals = selected_columns.iloc[:index]
may_deals = may_deals[may_deals['receiving_date'].dt.month == 6]


print(sum_total)
draw_graph(filtered_data)
print(most_ef_men(sept_deals))
print(most_frequent_type(oct_deals))
print(orig(may_deals))