def trap(height):
    """
    :type height: List[int]
    :rtype: int
    """
    area = 0
    i=0
    while i < len(height):
        if (height[i] == 0):
            i += 1
            continue

        temp_height = height[i]
        found = 0
        max_height = 0
        max_height_pos = 0
        for j in range(i + 1, len(height)):
            if (height[j] >= temp_height):
                found = j
                break
            elif (height[j]>max_height):
                max_height = height[j]
                max_height_pos = j
        if (found):
            temp = 0
            for k in range(i+1, found):
                temp = temp_height - height[k]
                area += temp
            i = found
        elif (max_height):
            for h in range(i+1  ,max_height_pos):
                temp = max_height - height[h]
                area += temp
            i = max_height_pos
        else:
            i+=1

    return area


print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))