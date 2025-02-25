# def simple_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @simple_decorator
# def say_hello():
#     print("Hello!")

# say_hello()


def simple_decorator(func):
    print("before")
    func()
    print("after")

@simple_decorator
def say_hello():
    print("Hello!")