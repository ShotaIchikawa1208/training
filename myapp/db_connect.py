import psycopg
from psycopg.rows import dict_row

class DBconnect():

    # アカウント登録(usersテーブルへ)
    def account_register(self,new_user, new_user_info, user_sikaku_list):
        print('アカウント登録スタート')
        
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:

            # 次のid番号取得
            with conn.cursor() as cur:
                cur.execute("SELECT nextval('user_id_seq') as user_id")
                user_id_seq = cur.fetchone() 
                

            with conn.cursor() as cur:
                self.user_id = user_id_seq[0]
                self.name = new_user['name']
                self.email = new_user['mail']
                self.password = new_user['password']
                sql = """
                    INSERT 
                    INTO users (user_id,name, mail, password, status) 
                    VALUES (%s,%s, %s, %s, %s)
                    """
                
               
                cur.execute(
                    sql,
                    [self.user_id,self.name,self.email,self.password,0]
                )

                
                print('users表へのアカウント登録完了')

                # user_infoへの補足情報登録
                self.user_info_register(self.user_id, new_user_info)
                print('user_info表への登録完了')

                # user_shikakuテーブルへの登録
                self.user_shikaku_register(self.user_id, user_sikaku_list)

                print('user_shikaku表への登録完了')
                conn.commit()
                message = '新規登録完了'
                return message
            
    # # 登録可能なメールアドレスかチェックする
    # def check_mail(salf,mail):
    #     with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
    #         with conn.cursor() as cur:

    #             sql = """
    #                 SELECT
    #                     count(*) 
    #                 FROM
    #                     users 
    #                 WHERE
    #                     mail = %s
    #                 """
    #             cur.execute(sql, [mail])
    #             judg = cur.fetchone()
                
    #             if judg == 0:
    #                 return True
    #             else:
    #                 return False

    # アカウント登録(user_infoテーブルへ)
    def user_info_register(self, user_id, user_info):
        print('user_info表への登録開始')
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            
            with conn.cursor(row_factory=dict_row) as cur:
                
                sql = """
                        INSERT 
                        INTO user_info( 
                            user_id
                            , name_kana
                            , gender
                            , yubin
                            , ken_code
                            , shiku
                            , jyusyo
                            , tel
                            , status
                        ) 
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    """
                
                cur.execute(sql,
                            [user_id,
                             user_info['name_kana'],
                             user_info['gender'],
                             user_info['yubin'],
                             user_info['ken_code'],
                             user_info['shiku'],
                             user_info['jyusyo'],
                             user_info['tel'],
                             0])
                
                print('user_info表への登録完了')

    # アカウント登録(user_shikakuテーブルへ)
    def user_shikaku_register(self, user_id, user_shikaku_list):
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor(row_factory=dict_row) as cur:

                sql = """
                    INSERT 
                    INTO user_shikaku(user_id, shikaku_code) 
                    VALUES (%s, %s)
                    """
                
                for shikaku_code in user_shikaku_list:
                    # print(shikaku_code)
                    cur.execute(sql,[user_id, shikaku_code])

                
    # ログイン判定
    def login_check(self, email, password):
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = """
                    SELECT
                        user_id
                    FROM
                        users
                    WHERE
                        mail = %s
                        AND password = %s
                    """
                cur.execute(sql, [email, password])
                user_id = cur.fetchone() 
                
                if user_id == None:
                    return False
                else:
                    id = user_id['user_id']
                    
                    return id
                
            
    # アカウント更新
    
    def update_user(self, user_id, new_user_info,  new_user_subinfo, user_shikaku_list):
        print('アカウント更新開始')
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor() as cur:
                sql = """
                    UPDATE users 
                    SET
                        name = %s
                        ,mail = %s 
                        ,password = %s
                    WHERE
                        user_id = %s
                    """
                
                user_id = str(user_id)
                cur.execute(sql,[new_user_info['name'], new_user_info['mail'], new_user_info['password'], user_id])
                print('usersへの更新完了')

                sql = """
                    UPDATE user_info 
                    SET
                        name_kana = %s
                        , gender = %s
                        , yubin = %s
                        , ken_code = %s
                        , shiku = %s
                        , jyusyo = %s
                        , tel = %s
                    WHERE
                        user_id = %s

                    """
                cur.execute(sql, 
                            [
                                new_user_subinfo['name_kana']
                                ,new_user_subinfo['gender']
                                ,new_user_subinfo['yubin']
                                ,new_user_subinfo['ken_code']
                                ,new_user_subinfo['shiku']
                                ,new_user_subinfo['jyusyo']
                                ,new_user_subinfo['tel']
                                ,user_id
                            ])
                print('user_infoへの更新完了')

                # まず既存のuser_shikaku表のデータ削除
                sql = """
                    SELECT
                        count(*) 
                    FROM
                        user_shikaku 
                    WHERE
                        user_id = %s
                    """
                
                # 指定のidがshikaku表にあるか判定
                cur.execute(sql, [user_id])
                recode = cur.fetchone()[0]
                

                if recode >= 1:
                    sql = """
                        DELETE 
                        FROM
                            user_shikaku 
                        WHERE
                            user_id = %s
                    """

                cur.execute(sql,[user_id])

                # 更新資格の登録
                sql = """
                    INSERT 
                    INTO user_shikaku(user_id, shikaku_code) 
                    VALUES (%s, %s)
                    """
                
                for shikaku_code in user_shikaku_list:
                    # print(shikaku_code)
                    cur.execute(sql,[user_id, shikaku_code])

                conn.commit()
                message = 'アカウント更新完了'
                return message  
                
    # アカウント削除
    def delete_user(self,id):
        print('アカウント削除開始')
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor() as cur:
                # users表のデータ削除
                sql = """
                    DELETE 
                    FROM
                        users 
                    WHERE
                        user_id = %s
                    """
                id = str(id)
                cur.execute(sql,[id])

                # user_info表のデータ削除
                sql = """
                    DELETE 
                    FROM
                        user_info 
                    WHERE
                        user_id = %s
                    """
                cur.execute(sql,[id])

                # user_shikaku表のデータ削除
                sql = """
                    SELECT
                        count(*) 
                    FROM
                        user_shikaku 
                    WHERE
                        user_id = %s
                    """
                
                # 指定のidがshikaku表にあるか判定
                cur.execute(sql, [id])
                recode = cur.fetchone()[0]
                

                if recode >= 1:
                    sql = """
                        DELETE 
                        FROM
                            user_shikaku 
                        WHERE
                            user_id = %s
                    """

                cur.execute(sql,[id])

                conn.commit()
                message = 'アカウント削除完了'
                return message
    
    # ユーザー一覧取得
    def get_users(self):
        print('users取得開始')
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                sql = """
                    SELECT
                        user_id
                    FROM
                        users    
                    """
                cur.execute(sql)
                user_id_list = cur.fetchall()
                # print(user_id_list)
                # print(type(user_id_list))
                
                # ユーザー全員分の情報をまとめるリスト
                users_info_list = []
                users_shikaku_list = []

                for user_id in user_id_list:
                    id = user_id['user_id']
                    user, user_shikakus = self.search_user(id)


                    # user_shikakusはタプルの入ったリストになるので、それを一つのリストにする
                    tmp = []
                    for shikaku_tapl in user_shikakus:
                        for shikaku in shikaku_tapl:
                            tmp.append(shikaku)
                    
                    users_info_list.append(user)
                    # users_shikaku_list.append(user_shikakus)
                    users_shikaku_list.append(tmp)

                
                print('users取得完了')
                return users_info_list, users_shikaku_list
            
    # ユーザー一人の基本情報取得
    def search_user(self,id):
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                print('user_info取得開始')
                # user_id,名前,性別を取得するSQL
                get_info_sql = """
                    SELECT
                        users.user_id
                        , users.name
                        , user_info.gender 
                    FROM
                        users 
                        INNER JOIN user_info 
                            ON users.user_id = user_info.user_id
                    where 
                        users.user_id = %s
                    """
                
                id = str(id)
                cur.execute(get_info_sql,[id])
                user = cur.fetchone()

                # gender_code変換
                if user['gender'] == '1':
                    user['gender'] = '男性'
                else:
                    user['gender'] = '女性'

                    
                user_shikaku_list = self.get_user_shiksku(id)

                
                
                return user,user_shikaku_list

    # ユーザー一人の資格情報取得
    def get_user_shiksku(self, id):
        with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
            with conn.cursor() as cur:
                # userの資格を取得するSQL
                print('user_shikaku取得開始')
                get_shikaku_sql = """
                                SELECT
                                    shikaku_name 
                                FROM
                                    shikaku 
                                WHERE
                                    shikaku_code IN ( 
                                        SELECT
                                            shikaku_code 
                                        FROM
                                            user_shikaku 
                                        WHERE
                                            user_id = %s
                                    ) 
                                ORDER BY
                                    shikaku_code

                               """
                cur.execute(get_shikaku_sql,[id])
                user_shikaku_list = cur.fetchall()

                return user_shikaku_list