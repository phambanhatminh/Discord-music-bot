nums = [1,1,2,2,3,4,5,5]
j = 0
for i in range(1, len(nums)):
    if nums[i] != nums[i - 1]:
        nums[j] = nums[i]
        j += 1
        print(nums)
                


