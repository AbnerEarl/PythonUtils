import math


def print_tree1(array, unit_width=2):
    length = len(array)
    depth = math.ceil(math.log2(length + 1))
    index = 0
    width = 2 ** depth - 1
    for i in range(depth):
        for j in range(2 ** i):
            print("{:^{}}".format(array[index], width * unit_width), end=" " * unit_width)
            index += 1
            if index >= length:
                return
        width //= 2
        print()


def print_tree2(array, unit_width=2):
    length = len(array)
    depth = math.ceil(math.log2(length + 1))
    index = 0
    count = 0
    for i in range(depth - 1, -1, -1):
        pre = 2 ** i - 1
        print(" " * pre * unit_width, end="")
        step = 2 ** count
        count += 1
        values = array[index:index + step]
        interval = " " * (2 * pre + 1) * unit_width
        print(interval.join(map(lambda x: "{:^{}}".format(x, unit_width), values)))
        index += step


def big_heap(array):
    def heap_adjust(n, i, arr):
        while n > 2 * i:
            max_child_index = 2 * i
            right_child_index = max_child_index + 1
            if right_child_index < n and arr[right_child_index] > arr[max_child_index]:
                max_child_index = right_child_index
            if arr[max_child_index] > arr[i]:
                arr[i], arr[max_child_index] = arr[max_child_index], arr[i]
                i = max_child_index
            else:
                break
        return arr

    length = len(array)
    start = length // 2
    for index in range(start, -1, -1):
        heap_adjust(length, index, array)

    return array


def sort_by_big_heap(array, reverse=False):
    length = len(array)
    result = []
    while length > 0:
        array = big_heap(array)
        result.append(array[0])
        array = array[1:]
        length = len(array)
    result = result.reverse() if reverse else result
    return result


print_tree1(range(50))
print("\n\n")
print_tree2(range(50))
print("\n\n")
tree_list = [10, 20, 30, 40, 50, 60, 70, 80, 90]
print_tree1(tree_list)
print("\n\n")
print_tree1(big_heap(tree_list))
print("\n\n")
print(sort_by_big_heap(tree_list))
