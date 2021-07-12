def longest_common_substring1(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    if len1 > len2:
        str1, str2 = str2, str1

    for i in range(len1, 0, -1):
        for j in range(0, len1 - i + 1):
            substr = str1[j: j + i]
            if str2.find(substr) >= 0:
                return substr
    return ""


def longest_common_substring2(str1, str2):
    len1 = len(str1)
    len2 = len(str2)
    matrix = [[0] * len1 for _ in range(len2)]
    count = 0
    index = 0
    for i, x in enumerate(str2):
        for j, y in enumerate(str1):
            if x == y:
                if i == 0 or j == 0:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] = matrix[i - 1][j - 1] + 1
                if matrix[i][j] > count:
                    count = matrix[i][j]
                    index = j
    return str1[index - count + 1:index + 1]


import datetime

start = datetime.datetime.now()
print(longest_common_substring1("xdabdasdfsdsasdfserjtelrjtlerjterterwewe", "absxabdvsasdfasdfsdfsudofhwqeowpwiepwer"))
end = datetime.datetime.now()
print(longest_common_substring2("xdabdasdfsdsasdfserjtelrjtlerjterterwewe", "absxabdvsasdfasdfsdfsudofhwqeowpwiepwer"))
end2 = datetime.datetime.now()
print(end - start)
print(end2 - end)
