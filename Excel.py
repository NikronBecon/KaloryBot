import openpyxl
from config import PATH_TO_EXCEL_FILE, MAX_ROWS, LETTER_COLUMN_KCAL, LETTER_COLUMN_PRODUCT


def check(key, value):
    key = sorted(key.split(" "))
    value = sorted(value.split(" "))
    for word1 in key:
        if len(word1) > 4:
            word1 = word1[:4].capitalize()
        elif 2 < len(word1) <= 4:
            word1 = word1[:-1].capitalize()
        for word2 in value:
            mark = False
            word2 = word2.capitalize()
            if word1 == word2[:len(word1)]:
                mark = True
                break
        if not mark:
            return False
    return True


def ProductSearch(key, with_sim=False):
    wb = openpyxl.open(filename=PATH_TO_EXCEL_FILE, read_only=True)
    wb.active = 0
    sheet = wb.active
    res = []
    res_sim = ""
    for i in range(1, MAX_ROWS + 1):
        if check(key, sheet[LETTER_COLUMN_PRODUCT + str(i)].value):
            #res += str(sheet["A" + str(i)].value) + ' - ' + str(sheet["F" + str(i)].value) + ' ккал \n'
            res.append([str(sheet[LETTER_COLUMN_PRODUCT + str(i)].value), int(sheet[LETTER_COLUMN_KCAL + str(i)].value)])
        if with_sim:
            word1ls = sorted(key.split(" "))
            word2ls = sheet["A" + str(i)].value
            word2ls = sorted(word2ls.split(" "))
            for word1 in word1ls:
                mark = False
                if len(word1) > 5:
                    word1 = word1[:5].capitalize()
                elif 2 < len(word1) <= 5:
                    word1 = word1[:-1].capitalize()
                for word2 in word2ls:
                    word2 = word2.capitalize()
                    if word1 == word2[:len(word1)]:
                        res_sim += str(sheet[LETTER_COLUMN_PRODUCT + str(i)].value) + ' - ' + str(sheet[LETTER_COLUMN_KCAL + str(i)].value) + ' ккал \n'
                        mark = True
                        break
                if mark:
                    break
    if with_sim:
        if res:
            return res, res_sim
        else:
            return "Ничего похожего не нашлось("
    else:
        if res:
            return res
        else:
            return "Ничего похожего не нашлось("

