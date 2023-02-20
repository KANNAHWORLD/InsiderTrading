import data_pipeline
import os

# Define Test cases below!
# Checks if the defalt saveFilings gets filings and is able to save it to
# the file tree
def Test1(holder="holder"):
    data_pipeline.SaveFilings("AMD")
    return True


# Add testing thing here I guess
if __name__ == "__main__":
    # Change this variable as test cases increase
    total_tests = 1
    test_counter = 1
    tests_passed = 0

    # test 1
    Test1()
    if os.path.exists("filings/AMD/4"):
        tests_passed += 1
        print(f'Test {test_counter}/{total_tests},'
              f' passed {tests_passed} tests')
    else:
        print(f'Test {test_counter}/{total_tests},'
              f' Failed current test, '
              f' passed {tests_passed} tests')

    test_counter += 1
    print()

