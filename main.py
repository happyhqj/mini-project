from pathlib import Path
import sys
import pandas as pd
import re
from datetime import datetime as dtt
from tabulate import tabulate as tbl

filename = 'data.csv'

def get_type(inp):
    patterns = {
        'add': r'^add "(.*?)"$',
        'update': r'^update (\d+) "(.*?)"$',
        'delete': r'^delete (\d+)$',
        'mark-in-progress': r'^mark-in-progress (\d+)$',
        'mark-done': r'^mark-done (\d+)$',
        'list': r'^list$',
        'list done': r'^list done$',
        'list todo': r'^list todo$',
        'list in-progress': r'^list in-progress$',
        'quit': r'^2$'
    }
    for command, pattern in patterns.items():
        match =  re.match(pattern, inp)
        if match:
            groups = match.groups()
            res = {'command': command, 'id': '', 'content': ''}
            if command == 'add':
                res['content'] = groups[0]
            elif command == 'update':
                res['id'] = groups[0]
                res['content'] = groups[1]
            elif command in ['delete', 'mark-in-progress', 'mark-done']:
                res['id'] = groups[0]
            return res
    return None

def get_time():
    now = dtt.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def print_(df):
    print(tbl(df, headers='keys', tablefmt='fancy_grid', stralign='center'))

def upd_csv(df):
    df.to_csv(filename, index=False, encoding='utf-8-sig')

def add(content):
    df = pd.read_csv(filename)
    now = get_time()
    df.loc[len(df)] = ['todo', content, now, now]
    upd_csv(df)
    print_(df)

def update(id, content):
    id = int(id)
    df = pd.read_csv(filename)
    if id < 0 or id > len(df): return print("Wrong operation")
    df.loc[id, 'Content'] = content
    df.loc[id, 'UpdatedAt'] = get_time()
    upd_csv(df)
    print_(df)

def delete(id):
    id = int(id)
    df = pd.read_csv(filename)
    if id < 0 or id > len(df): return print("Wrong operation")
    df = df.drop(index=id)
    upd_csv(df)
    print_(df)
    
def mark(id, statu):
    id = int(id)
    df = pd.read_csv(filename)
    if id < 0 or id > len(df): return print("Wrong operation")
    df.loc[id, 'Status'] = statu
    df.loc[id, 'UpdatedAt'] = get_time()
    upd_csv(df)
    print_(df)

def list_(statu):
    df = pd.read_csv(filename)
    condition = df['Status'] == statu
    df2 = df[condition]
    print_(df2)

def main():
    
    file_path = Path(filename)
    if not file_path.exists():
        print(1)
        df = pd.DataFrame(columns=['Status', 'Content', 'CreatedAt','UpdatedAt'])
        df.to_csv(filename, index=False, encoding='utf-8-sig')

    print("""
    rules:
        add "xxx"
        update [id] "xxx"
        delete [id]
        mark-in-progress [id]
        mark-done [id]
        list
        list done
        list todo
        list in-progress
    """)

    print("start: 1\nquit: 2")
    while True:
        x = input()
        if x == "1": break
        if x == "2": sys.exit()
    print("start!")

    while True:
        op = get_type(input())
        if op == None: continue
        tp = op['command']
        id = op['id']
        content = op['content']
        if tp == 'add':
            add(content)
        elif tp == 'update':
            update(id, content)
        elif tp == 'delete':
            delete(id)
        elif tp == 'mark-in-progress':
            mark(id, 'in-progress')
        elif tp == 'mark-done':
            mark(id, 'done')
        elif tp == 'list':
            print_(pd.read_csv(filename))
        elif tp == 'list done':
            list_('done')
        elif tp == 'list todo':
            list_('todo')
        elif tp == 'list in-progress':
            list_('in-progress')
            
if __name__ == "__main__":
    main()