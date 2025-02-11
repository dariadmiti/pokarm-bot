import dramatiq

@dramatiq.actor
def count(n):
    for i in range(n):
        if i % 2 == 0:
            print(i)

