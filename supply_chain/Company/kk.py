import heapq

lis = []
heapq.heappush(lis, 2)
heapq.heappush(lis, 5)
heapq.heappush(lis, 1)
heapq.heappush(lis, 7)
print(len(lis))
print(lis)
to_remove = heapq.heappop(lis)
print(to_remove)
print(len(lis))
print(lis)

a = list(filter(lambda x: x == 20, lis))
print(a)
