import copy

from Controller import Controller


def main():
    controller = Controller('input_file.txt')
    print('1.Run program')
    print('0.Exit')
    choice = int(input("choice: "))
    if choice == 0:
        return
    elif choice == 1:
        current_best_path = []

        for i in range(controller.get_iter_count()):
            controller.new_colony()
            best_ant = controller.get_best_ant()
            path = best_ant.get_path()
            if len(path) > len(current_best_path):
                current_best_path = copy.deepcopy(path)
            print("the current best path is:\n", current_best_path)
            print("The current best ant is:\n", best_ant)
main()