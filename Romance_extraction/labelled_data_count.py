import ast
with open('label_sanguo.txt','r') as f:
    lines = f.readlines()
    count = 0

    for line in lines:
        dict = ast.literal_eval(line)
        print(dict['speaker'])
        if not dict['speaker'] == None:
            count += 1

    print(count)
