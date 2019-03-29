class Counter:
    def __init__(self):
        self.count = 1

    def __call__(self, expected_count, return_value=None):
        assert self.count == expected_count, (
                "Count doesn't match: you are expecting {}, but my "
                "count is {}").format(expected_count, self.count)
        self.count += 1
        return return_value

    def reset(self):
        self.count = 1

c = Counter()
