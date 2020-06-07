# import os
# import setting
from mainapp.models import ProductCategory, Product


category_new = ProductCategory(name='new cat')

# print(BASE_DIR)

# data_path = os.path.join(os.getcwd(), 'names')
#
#
# def count_top3(list_years):
#     cols = ['Name', 'Gender', 'Count']
#     i = 0
#     for year in list_years:
#         names_frame = pd.read_csv(
#             os.path.join(data_path, 'yob' + str(year) + '.txt'),
#             names=cols
#         )
#         i += 1
#         if i == 1:
#             names = names_frame
#         else:
#             names = names.append(names_frame)
#
#     if len(list_years) > 0:
#         names.sort_values(by='Count', ascending=False)
#         return [a for a in names.Name.head(3)]