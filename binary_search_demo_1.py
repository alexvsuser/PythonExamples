
def binary_search(lst, need_item, startindex, stopindex):

        """ Returns the index of the required item or -1. Example of recursion"""

        if startindex > stopindex:
            return -1
    
        mid = (startindex + stopindex) // 2
    
        if lst[mid] == need_item:
            return mid
        elif lst[mid] > need_item:
            return binary_search(lst, need_item, startindex, mid -1)
        else:
            return binary_search(lst, need_item, mid + 1, stopindex)

if __name__ == '__main__':

        lst_1 = [5, 10, 12, 15, 18, 19, 21, 24, 26, 27, 30, 32, 34, 35, 37, 40, 42, 44, 45, 46, 49, 70, 80, 120] # 24

        print(binary_search(lst_1, 5, 0, len(lst_1)-1))
        print(binary_search(lst_1, 21, 0, len(lst_1)-1))
        print(binary_search(lst_1, 22, 0, len(lst_1) -1))
        print(binary_search(lst_1, 120, 0, len(lst_1)-1))
    
      
      
