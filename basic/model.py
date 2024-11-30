

class CivDataDict(dict):
    def __init__(self,keys:list or tuple,values:list or tuple):
        if len(keys) != len(values):
            raise Exception
        for i in range(len(keys)):
            self[keys[i]] = values[i]

    def set_query_script(self,sql:str,params:tuple):
        if sql and params:
            for i in params:
                if "?" in sql:
                    if type(i) == str:
                        sql = sql.replace("?",f"'{i}'",__count=1)
                    elif type(i) in (tuple,int,float):
                        sql = sql.replace("?",f"'{i}'",__count=1)
                    else:
                        i = str(i)
                        sql = sql.replace("?", i)
                else:
                    raise ValueError("Too many params to fill in basic query script")
            if "?" in sql:
                raise ValueError("Too many placeholders in basic query script")
        self.query_script = sql
