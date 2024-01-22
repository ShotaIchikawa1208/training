import psycopg

with psycopg.connect("dbname=study user=study password=study host=localhost port= 5432") as conn:
    with conn.cursor() as cur:
        # cur.execute("""
        #             CREATE TABLE test (
        #             id serial PRIMARY KEY,
        #             num integer,
        #             data text 
        #             )
        #             """
        #             )
        

        # INSERT文
        cur.execute(
            "INSERT INTO test (num, data) VALUES (%s, %s)",
            (300, "ABC'DEF")
        )

        cur.execute('SELECT * FROM test')
        recodes = cur.fetchall()

        # print(recodes)

        for record in recodes:
            
            # print(record)
            pass

        print(recodes)
        # UPDATE文
        cur.execute('UPDATE test SET data = %s WHERE id = %s',('XXX',1))
        cur.execute('SELECT * FROM test')
        update_recodes = cur.fetchall()
        print(update_recodes)

        # DELETE文
        # cur.execute('DELETE FROM test WHERE num = %s',(200,))
        # cur.execute('SELECT * FROM test')
        # delete_after_recodes = cur.fetchall()
        # print(delete_after_recodes)
        # print(cur.execute('SELECT * FROM test').fetchone()[0])

        # cur.execute('INSERT INTO test (num, data) VALUES(%s, %s)',(200,'ABC' ))
        conn.commit()
        
