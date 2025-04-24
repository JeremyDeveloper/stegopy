import unittest, time

class TestResult(unittest.TextTestResult):
    def startTest(self, test):
        self._start_time = time.time()
        super().startTest(test)

    def stopTest(self, test):
        elapsed = time.time() - self._start_time
        self.stream.writeln(f"Test {test} took {elapsed:.3f} seconds")
        super().stopTest(test)
    
class TestRunner(unittest.TextTestRunner):
    resultclass = TestResult

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = TestRunner(verbosity=2)
    runner.run(suite)