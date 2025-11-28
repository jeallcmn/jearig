
def outer_join(list1, list2, leftJoin:bool = True):
    joined = []
    last1 = list1[-1]
    last2 = list2[-1]
    for i in range(max(len(list1), len(list2))):
        # get left element
        left = last1
        if i < len(list1):
            left = list1[i]
        right = last2
        if(leftJoin):
            right = None
        if i < len(list2):
            right = list2[i]
        if left and right:
            joined.append((left, right))
    return joined