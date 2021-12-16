# def superfunc():
#     i = 0
#
#     def wrapper():
#         nonlocal i
#         i += 1
#         return i
#
#     return wrapper
#
#
# A = superfunc()
# print(A(), A(), A())

import datetime
tx = datetime.datetime.now().strftime("%Y-%m-%d")
print(tx)