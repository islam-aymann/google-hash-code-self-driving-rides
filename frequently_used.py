def manipulate(filename, split_count=None, shaped=False, start_line=0, end_line=None, new_line=False, **enumerations):
    """
    :param filename: name of the file to be handled
    :type filename: string
    :param split_count: split line for certain no. of chars if it's one string
    :type split_count: int
    :param shaped:  if True, return the whole list at once instead of yielding each element
    :type shaped: bool
    :param start_line: the line you want to start manipulation with
    :type start_line: int
    :param end_line: the line you want to end manipulation with
    :type end_line: int
    :param new_line: yields new line if exists in line contents
    :type new_line: bool
    :param enumerations: the key is the chars you want to replace with the value
    :return: elements at each iterations or whole list regarding start and end
    """
    final_shape = list()
    global el
    el = '\n'
    with open(filename) as file:
        for line_no, line in enumerate(file.readlines()):
            line_contents = list()
            if line_no < start_line:
                continue
            elif line_no == end_line:
                break
            else:
                line_elements = line.split()
                if line_elements:
                    for element in line_elements:
                        try:
                            if shaped:
                                line_contents.append(int(element))
                            else:
                                yield int(element)
                        except ValueError:
                            if split_count:
                                for step in range(len(element)):
                                    chars_slice = element[step: step+split_count]
                                    if enumerations:
                                        for target, replacer in enumerations.items():
                                            if chars_slice == target:
                                                chars_slice = replacer
                                    if shaped:
                                        line_contents.append(chars_slice)
                                    else:
                                        yield chars_slice
                            else:
                                if shaped:
                                    line_contents.append(element)
                                else:
                                    yield element
            if shaped:
                final_shape.append(line_contents)
            else:
                if new_line:
                    yield el
    if shaped:
        yield final_shape


class sumRange:
    def __init__(self, A=list()):
        self.A = A
        self.s = []
        self.x = []
        self.t = []

    def cumSum(self):
        if type(self.A[0]) == list:
            self.s = []
            self.t = []
            self.z = [0] * len(self.A[0])
            # turn into zero based
            self.A.insert(0, self.z)
            for i in range(len(self.A)):
                self.A[i].insert(0, 0)
            for i in range(len(self.A)):
                for j in range(len(self.A[i])):
                    if j == 0:
                        self.t.append(self.A[i][j])
                    else:
                        self.t.append(self.A[i][j] + self.t[j - 1])
                self.s.append(self.t)
                self.t = []

            self.s = list(map(list, zip(*self.s)))
            self.x = self.s
            self.s = []

            for i in range(len(self.x)):
                for j in range(len(self.x[i])):
                    if j == 0:
                        self.t.append(self.x[i][j])
                    else:
                        self.t.append(self.x[i][j] + self.t[j - 1])
                self.s.append(self.t)
                self.t = []
            self.s = list(map(list, zip(*self.s)))
            return self.s

        else:
            self.s = []
            for i in range(len(self.A)):
                if i == 0:
                    self.s.append(self.A[i])
                else:
                    self.s.append(self.s[i - 1] + self.A[i])
            return self.s

    def getS(self):
        return self.s

    def sr(self, i, j, k=0, l=0):
        if type(self.A[0]) == list:
            i += 1
            j += 1
            k += 1
            l += 1

            A = self.s[i - 1][j - 1]
            B = self.s[i - 1][l]
            D = self.s[k][j - 1]
            C = self.s[k][l]
            return C - B - D + A
        else:
            if i == 0:
                return self.s[i]
            else:
                return self.s[j] - self.s[i - 1]


