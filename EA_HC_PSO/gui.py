import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication,  QLineEdit
import threading
from HC.HC_class import Hill_Climbing
from EA.EA_class import EA
from PSO.PSO_class import PSO
import matplotlib.pyplot as plotter
import statistics


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(450, 300, 580, 300)
        self.initUI()
        self.ea_thread = None
        self.hc_thread = None
        self.pso_thread = None
        self.pso_stats_thread = None
        self.ea_stats_thread = None
        self.average_ea = []
        self.average_pso = []

    def initUI(self):
        self.main_thread = threading.Thread()
        self.main_thread.start()
        '''Buttons:'''
        self.EA_button = QPushButton('Start EA', self)
        self.EA_button.move(90, 150)
        self.EA_button.clicked[bool].connect(self.start_EA)
        #
        self.stop_button = QPushButton('Stop process', self)
        self.stop_button.move(260, 250)
        self.stop_button.clicked[bool].connect(self.stop_execution)
        #
        self.HC_button = QPushButton('Start HC', self)
        self.HC_button.move(260, 150)
        self.HC_button.clicked[bool].connect(self.start_HC)
        #
        self.PSO_button = QPushButton('Start PSO', self)
        self.PSO_button.move(420, 150)
        self.PSO_button.clicked[bool].connect(self.start_PSO)
        #
        self.plot_EA_button = QPushButton('Plot EA', self)
        self.plot_EA_button.move(90, 250)
        self.plot_EA_button.clicked[bool].connect(self.ea_stats)
        #
        self.plot_PSO_button = QPushButton('Plot PSO', self)
        self.plot_PSO_button.move(420, 250)
        self.plot_PSO_button.clicked[bool].connect(self.pso_stats)

        '''Line edits"'''
        self.le_indiv_size = QLineEdit(self)
        self.le_pop_size = QLineEdit(self)
        self.le_mutation_probability = QLineEdit(self)
        self.le_iteration_count = QLineEdit(self)
        self.le_neigh_size = QLineEdit(self)

        self.le_indiv_size.move(230, 20)
        self.le_iteration_count.move(230, 50)
        self.le_pop_size.move(90, 120)
        self.le_mutation_probability.move(90, 90)
        self.le_neigh_size.move(390, 120)

        '''Labels:'''
        label1 = QtWidgets.QLabel(self)
        label2 = QtWidgets.QLabel(self)
        label3 = QtWidgets.QLabel(self)
        label4 = QtWidgets.QLabel(self)
        label5 = QtWidgets.QLabel(self)
        label1.setText("Population size:")
        label1.move(10, 120)
        label2.setText("Individual size:")
        label2.move(150, 20)
        label3.setText("Mutation prob.:")
        label3.move(10, 90)
        label4.setText("Iteration count:")
        label4.move(150, 50)
        label5.setText("Neighbourhood size:")
        label5.move(390, 90)

        self.show()

    def start_EA(self):
        def EA_thread(p_size, i_size, m_prob, i_count):
            ea = EA(p_size, i_size, m_prob, i_count)
            ea.run_EA()

        pop_size = int(self.le_pop_size.text())
        indiv_size = int(self.le_indiv_size.text())
        mutation_prob = int(self.le_mutation_probability.text())
        iteration_count = int(self.le_iteration_count.text())

        self.ea_thread = threading.Thread(target=EA_thread, args=(pop_size, indiv_size, mutation_prob, iteration_count))
        self.ea_thread.start()

    def stop_execution(self):
        # app.quit()
        if self.ea_thread != None:
            self.ea_thread.exit()
        if self.hc_thread != None:
            self.hc_thread.exit()
        if self.pso_thread != None:
            self.pso_thread.exit()
        app.quit()

    def start_HC(self):
        def HC_thread(i_size, it_count):
            hc = Hill_Climbing(i_size, it_count)
            hc.run_hc()

        indiv_size = int(self.le_indiv_size.text())
        iteration_count = int(self.le_iteration_count.text())
        self.hc_thread = threading.Thread(target=HC_thread, args=(indiv_size, iteration_count))
        self.hc_thread.start()

    def start_PSO(self):
        def PSO_thread(i_size, p_size, n_size, it_count):
            pso = PSO(i_size, p_size, n_size, it_count)
            pso.run_pso()

        indiv_size = int(self.le_indiv_size.text())
        pop_size = int(self.le_pop_size.text())
        neighb_size = int(self.le_neigh_size.text())
        iterations = int(self.le_iteration_count.text())
        self.pso_thread = threading.Thread(target=PSO_thread, args=(indiv_size, pop_size, neighb_size, iterations))
        self.pso_thread.start()

    def ea_stats(self):
        '''Go through 30 generation using the ea algorithm
        For each generation, plot the average fitness resulted
        '''
        '''dimension = 30, individual_size = 3, mutation probability = 60%, iteration count = 1000'''

        def thread_stats():
            y_axis = []
            for i in range(30):
                ea = EA(40, 3, 60)
                for j in range(1000):
                    ea.next_generation()
                    ea.set_average_fitness()

                avr = 0
                for run_fitness in ea.get_average_fitness():
                    avr += run_fitness
                avg = avr / len(ea.get_average_fitness())
                y_axis.append(avg)
                self.average_ea.append(avg)
            x_axis = [i for i in range(len(y_axis))]

            plotter.cla()
            plotter.ylabel("Average fitness value")
            plotter.xlabel("Generation no.")
            plotter.plot(x_axis, y_axis, 'g^-')
            plotter.show()

            global_average = 0
            for a in self.average_ea:
                global_average += a
            global_average /= len(self.average_ea)

            print("Global average fitness is: ")
            print(global_average)

            deviation = statistics.stdev(self.average_ea)
            print("Standard deviation is:")
            print(deviation)

        self.ea_stats_thread = threading.Thread(target=thread_stats, args=())
        self.ea_stats_thread.start()

    def pso_stats(self):
        def thread_stats():
            fitness_list = []
            for i in range(30):
                pso = PSO(3, 40, 10, 1000)
                pso.run_pso()
                fitness_list.append(pso.get_highest_fitness())
            avg = 0
            for fit in fitness_list:
                avg += fit
            avg = avg / 30

            plotter.cla()
            x_axis = [i for i in range(len(fitness_list))]
            plotter.plot(x_axis, fitness_list, 'r--')
            plotter.show()

            print("Global average fitness is: ")
            print(avg)

            deviation = statistics.stdev(fitness_list)
            print("Standard deviation is:")
            print(deviation)

        self.pso_stats_thread = threading.Thread(target=thread_stats, args=())
        self.pso_stats_thread.start()


app = QApplication(sys.argv)
GUI = Window()
sys.exit(app.exec())
