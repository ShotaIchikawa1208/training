import csv 


def insert_from_csv():
    print('start')
    with open('C:\\Users\\市川翔大\\Desktop\\task\\make_sql\\sample.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)

        insert_sqls = []

        for row in csv_reader:
            post_code = row[0]
            ken_kana = row[1]
            shiku_kana = row[2]
            mati_kana = row[3]
            ken = row[4]
            shiku = row[5]
            mati = row[6]

            sql = f"""INSERT INTO post_code_list (post_code,ken_kana,shiku_kana,mati_kana,ken,shiku,mati) 
                VALUES('{post_code}', '{ken_kana}','{shiku_kana}','{mati_kana}','{ken}','{shiku}','{mati}');
                """
            
            insert_sqls.append(sql)

    with open('insert_yubin.txt', 'w', encoding='utf-8') as f:
        print('wstart')
        for sql in insert_sqls:
            f.write(sql + '\n')
        

if __name__ == '__main__':
    insert_from_csv()