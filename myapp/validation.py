import psycopg

# 登録可能なメールアドレスかチェックする
def check_mail(mail):
    with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
        with conn.cursor() as cur:

            sql = """
                SELECT
                    count(*) 
                FROM
                    users 
                WHERE
                    mail = %s
                """
            print(type(mail))
            cur.execute(sql, [mail])
            judg = cur.fetchone()
            
            # countが１以上（すでにメールアドレスが登録されていれば）Falseを返す
            if judg[0] == 0:
                return True
            else:
                return False
            
def search_address(yubin):
     with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
        with conn.cursor() as cur:

            sql = """
                SELECT
                    * 
                FROM
                    post_code_list 
                WHERE
                    post_code = %s

                """
            
        
            yubin = str(yubin)
            print(yubin)
            cur.execute(sql, [yubin])

            result = cur.fetchone()
        
            # 入力された郵便番号がない場合
            if result == None:
                print('none')
                result_dict = {'yubin': 'None'}
                return result_dict
            else:
                ken_code = search_ken_code(result[4])[0]
               
                result_dict = {'yubin': result[0],
                               'ken_code': ken_code,
                               'ken': result[4],
                               'shiku': result[5],
                               'mati': result[6]}
                return result_dict

def search_ken_code(ken):
    sql = """
        SELECT
            ken_code
        FROM
            todoufuken
        WHERE
            ken_name = %s
        """
    with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
        with conn.cursor() as cur:
            cur.execute(sql, [ken])
            ken_code = cur.fetchone()

            return ken_code

if __name__ == '__main__':
    search_address(9300261)