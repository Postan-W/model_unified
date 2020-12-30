
def analysis_list(data_dict) -> []:
    key_list = []
    for data in data_dict:
        for key in data.keys():
            key_list.append(key)
    return key_list
