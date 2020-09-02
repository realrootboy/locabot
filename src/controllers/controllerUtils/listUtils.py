def searchAndUpdate(gen_list, pkey1, pkey2, field, newValue):
    # setattr(x, 'y', v) is equivalent to x.y = v
    for item in gen_list:
        if(item.username == pkey1):
            if(item.chat_id == pkey2):
                setattr(item, field, newValue)


def searchAndGetItem(gen_list, pkey1, pkey2):
    for item in gen_list:
        if(item.username == pkey1):
            if(item.chat_id == pkey2):
                return item

def listItens(gen_list):
    for item in gen_list:
        print(item.username + ' ' + str(item.chat_id) + ' ' + str(item.media_dir) + ' \n')