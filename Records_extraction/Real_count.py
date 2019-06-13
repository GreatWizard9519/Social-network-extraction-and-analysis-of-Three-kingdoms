with open('sanguozhi1.txt','r',encoding='UTF-8') as f:
    count = 0
    for line in f.readlines():
        if "Ma Chao" in line:
            count += 1

    print(count)