import random
import time

RANDOM_MIN = 1
RANDOM_MAX = 10 ** 9

def time_travel_test():
    # predict the random number before it is shown to you!

    x = random.randrange(RANDOM_MIN, RANDOM_MAX + 1)
    guess = input(f"Which number between {RANDOM_MIN} and {RANDOM_MAX} will I print? ")

    print(f"The number is {x}")
    return str(x) == guess

def control_electricity_test():
    # if you can control electricity, you can change the value in the computer
    # memory to return True, right?
    return False

def super_speed_test():
    # here you must type the challenge within 1 nano second
    # oh, and you need to make the print function take less than a nano seond
    challenge = "I am super fast!"

    time_before = time.perf_counter_ns()
    typed = input(f"Write \"{challenge}\" as fast as you can :)")
    time_after = time.perf_counter_ns()

    return challenge == typed and time_before == time_after

def test_super_powers():
    print("time travel = t\ncontrol electricity = e\nsuper speed = s")

    super_powers = input("what are your superpowers? ")

    if "t" in super_powers and not time_travel_test():
        return False
    if "e" in super_powers and not control_electricity_test():
        return False
    if "s" in super_powers and not super_speed_test():
        return False

    letters = super_powers.lower()

    # success if didn't fail any test, and one of the test letters was found
    return any(("t" in letters, "e" in letters, "s" in letters))

if __name__ == '__main__':
    if test_super_powers():
        print("you win!")
    else:
        print("you failed :(")
