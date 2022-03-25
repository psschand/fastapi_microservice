
def Convert(lst):
    res_dct = { lst[i + 1].strip():lst[i] for i in range(0, len(lst), 2)}
    return res_dct