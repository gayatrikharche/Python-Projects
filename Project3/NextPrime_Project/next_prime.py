def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def next_prime_generator():
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


# Main loop
if __name__ == "__main__":
    primes = next_prime_generator()
    
    while True:
        print("Next prime:", next(primes))
        cont = input("Do you want the next one? (y/n): ").strip().lower()
        if cont != "y":
            print("Exiting... Goodbye!")
            break

