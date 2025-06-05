def func_9_9_table():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print("{}*{}={:<2}".format(j, i, i * j), end='\t')
        print()


def bubble_sort(arr):
    
    return arr


if __name__ == '__main__':
    func_9_9_table()
    # Test bubble sort
    test_list = [64, 34, 25, 12, 22, 11, 90]
    print("Original list:", test_list)
    bubble_sort(test_list)
    print("Sorted list:", test_list)
