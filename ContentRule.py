import psycopg2
import itertools
import random

conn = psycopg2.connect(
    database='huwebshop',
    host='localhost',
    port='5432',
    password='Eigen Wachtwoord',
    user='postgres'
)

cursor = conn.cursor()

profile_id = input('ProfileID invullen: ')

cursor.execute(f'''
SELECT pr.id,pr.category,pr.sub_category,pr.sub_sub_category
FROM product AS pr
GROUP BY pr.id,pr.category,pr.sub_category,pr.sub_sub_category
ORDER BY pr.category,pr.sub_category,pr.sub_sub_category ''')

producten = cursor.fetchall()
aanbeveling = {}
for product in producten:
    categorie = None
    if product[3]:
        categorie = product[3]
    elif product[2]:
        categorie = product[2]
    elif product[1]:
        categorie = product[1]

    if categorie and product[0]:
        if categorie not in aanbeveling:
            aanbeveling[categorie] = []
        aanbeveling[categorie].append(str(product[0]))

cursor.execute(f'''SELECT session.id from session 
WHERE session.profileid = '{profile_id}' 
and session.has_sale = True ''')

sessie_id = cursor.fetchall()

recommend = []
for sessie in sessie_id:
    id = ''.join(sessie)
    cursor.execute(f'''SELECT productid from "order"
    WHERE "order".sessionid = '{id}' ''')
    products = cursor.fetchall()

    recommend.append(products)

flat_ls = []
for i in recommend:
    for j in i:
        id = ''.join(j)
        flat_ls.append(id)

recommendations = []

for i in flat_ls:
    for categorie, product in aanbeveling.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if i in product:
            pr = product
            recommendations.append(pr)


lijst_recommendation = []
for i in recommendations:
    for j in i:
        lijst_recommendation.append(j)

new_list = random.sample(lijst_recommendation, 5)


