import math
import random


class Node:
    def __init__(self, data, index, value, left_branch, right_branch):
        self.data = data
        self.index = index
        self.value = value
        self.left_branch = left_branch
        self.right_branch = right_branch


class Leaf_Node:
    def __init__(self, data):
        self.result = None
        self.data = data
        self.compute_result()

    def compute_result(self):
        labels = [row[0] for row in self.data]
        num = 0

        for cls in ['L', 'B', 'R']:
            n = labels.count(cls)
            if n > num:
                num = n
                self.result = cls


class DecisionTree:
    def __init__(self, input_file):
        self.input_file = input_file

    '''Build a tree using the information gain method'''

    def get_data_set(self):
        f = open(self.input_file, 'r')
        line = f.readline()
        data_set = []

        while line:
            row = line.split(',')
            row = [row[0]] + [int(values) for values in row[1:5]]
            data_set.append(row)
            line = f.readline()
        random.shuffle(data_set)

        train_size = int(len(data_set) * 0.8)
        training_data = []
        testing_data = []
        for i in range(train_size):
            training_data.append(data_set[i])
        for i in range(train_size, len(data_set)):
            testing_data.append(data_set[i])

        return training_data, testing_data

    def run_tree(self, data):
        '''Run the algorithm
        If a new branch has an information gain of 0, it means is a Leaf Node'''
        information_gain, best_index, best_value = self.get_split_point(data)
        left_set, right_set = self.partition(best_index, best_value, data)

        if information_gain == 0 or len(left_set) == 0 or len(right_set) == 0:
            left_node = right_node = Leaf_Node(data)
        else:
            #At this point, there are still available rows to split on
            '''Do the recursive call for both branches'''
            left_node = self.run_tree(left_set)
            right_node = self.run_tree(right_set)

        return Node(data, best_index, best_value, left_node, right_node)

    def partition(self, index, value, data):
        left_side = []
        right_side = []
        for row in data:
            if row[index] <= value:
                left_side.append(row)
            else:
                right_side.append(row)

        return left_side, right_side

    def get_split_point(self, data):
        '''Go through the data set and find the split point that gives us the highest
        information gain'''
        highest_gain = 0
        best_index = 1
        best_value = 1
        set_size = len(data)
        all_set_entropy = self.get_entropy(data)

        for index in range(1, 5):
            for value in range(1, 6):
                left_branch, right_branch = self.partition(index, value, data)
                if len(left_branch) == 0 or len(right_branch) == 0:
                    continue

                left_entropy = self.get_entropy(left_branch)
                right_entropy = self.get_entropy(right_branch)

                current_gain = all_set_entropy - (
                            len(left_branch) / set_size * left_entropy + len(right_branch) / set_size * right_entropy)
                if current_gain > highest_gain:
                    highest_gain = current_gain
                    best_index = index
                    best_value = value

        return highest_gain, best_index, best_value

    def get_entropy(self, data):
        '''Compute the entropy of the current dataset by the formula from the course:
        Entr(S) = ∑ i=1..n -prob(i) * log⒉ prob(i) '''

        class_list = [row[0] for row in data]
        size = len(data)
        entropy = 0

        for base_class in ['L', 'B', 'R']:
            prob = int(class_list.count(base_class)*100 / size)/100.00
            if prob > 0:
                entropy += -prob * math.log2(prob)

        return entropy

    def get_result(self, node, row):
        if isinstance(node, Leaf_Node):
            return node.result
        else:
            if node.value < row[node.index]:
                if isinstance(node.right_branch, Leaf_Node):
                    return node.right_branch.result
                else:
                    return self.get_result(node.right_branch, row)
            else:
                if isinstance(node.left_branch, Leaf_Node):
                    return node.left_branch.result
                else:
                    return self.get_result(node.left_branch, row)

    def get_accuracy(self):
        train_data, test_data = self.get_data_set()
        decision_tree = self.run_tree(train_data)

        correct_results = 0
        for i in range(len(test_data)):
            predicted_result = self.get_result(decision_tree, test_data[i])
            if predicted_result == test_data[i][0]:
                correct_results += 1
        accuracy = int(correct_results*100 / len(test_data))
        return accuracy

def main():
    runs = 400
    input_file = 'balance-scale.data'

    highest_accuracy = 0
    medium_accuracy = 0

    for run in range(1, runs + 1):
        decision_tree = DecisionTree(input_file)
        current_accuracy = decision_tree.get_accuracy()

        medium_accuracy += current_accuracy
        highest_accuracy = max(highest_accuracy, current_accuracy)

        if run % 30 == 0:
            print("Medium accuracy: ", (medium_accuracy*100 / run) / 100.00, "%")
            print("Highest accuracy: ", highest_accuracy*100 / 100.00, "%")
if __name__ == '__main__':
    main()