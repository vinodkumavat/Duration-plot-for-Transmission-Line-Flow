# for all extracting and plotting
from calendar import month
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


# for creating GUI
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg



# importing data frame from sheet name MainData
df_sheet = pd.read_excel("Lines_Plot.xlsx")
# importing data frame used for naming
station_name_id = pd.read_excel("Station_Name_Id.xlsx")



class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # add title to application
        self.setWindowTitle("Vinod's App")

        # set layout
        self.setLayout(qtw.QVBoxLayout())

        # Create label1
        my_label_1 = qtw.QLabel("Select transmission line")
        # change font size
        my_label_1.setFont(qtg.QFont('Cosmic Sans', 18))
        # Display label on screen
        self.layout().addWidget(my_label_1)


        # extracting the column names from Line_Plot.xlsx
        column_names = df_sheet.columns[1:]


        #Create Drop Down (combo) box for selecting transmission line
        my_combo = qtw.QComboBox()
        # add items to combo box
        my_combo.addItems(column_names)
        # put on the screen
        self.layout().addWidget(my_combo)


        # Create label2
        my_label_2 = qtw.QLabel("Enter The reference voltage")
        # change font size
        my_label_2.setFont(qtg.QFont('Cosmic Sans', 16))
        # Display label on screen
        self.layout().addWidget(my_label_2)


        # creating entry box for reference voltage
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("Reference Voltage")
        # Display entrybox on screen
        self.layout().addWidget(my_entry) 


        # Create button
        my_button = qtw.QPushButton("Show me plot!", clicked = lambda: press_it())
        # Display button on screen
        self.layout().addWidget(my_button) 


        # creating image label widget
        my_label_img = qtw.QLabel(self)
        # loading image
        pixmap = qtg.QPixmap('vinod_fig.png')
        # Addign image to label
        my_label_img.setPixmap(pixmap)
        # resizing label to image size
        my_label_img.resize(pixmap.width(), pixmap.height())
        self.layout().addWidget(my_label_img)
        

        # to show the app i.e. to pop up the window
        self.show()


        # Creating counter function to get the x_axis values
        def counter_(unique_sample, total_sample):
            # defining the counter array size = size(unique_Sample)
            counter_temp = []

            for i in range(len(unique_sample)):
                # counting the number of times total sample have value greater than unique
                temp_c = (total_sample[:] >= unique_sample[i]).sum()

                # Finding the percentage of counter_temp over total sample
                temp_per = (temp_c/len(total_sample))*100

                # appending to the counter variable
                counter_temp.append(temp_per)

            return counter_temp
        
        
        
        # Creating month decider i.e. April, May, June
        def month_decider(i, month_number):
            row_indexing = [2880, 5856]
            if (month_number == 0):
                temp_sample = df_sheet.iloc[0:2880, i]
                return temp_sample
            elif (month_number == 1):
                temp_sample = df_sheet.iloc[2880:5856, i]
                return temp_sample
            else:
                temp_sample = df_sheet.iloc[5856:, i]
                return temp_sample



        # Creating function to decide the title
        def title_decider(col_num):
            # get the array of station id and name from Station_Name_Id.xlsx
            station_id = station_name_id["Station ICT ID"]
            station_name = station_name_id["Station Name"]

            # getting selected id i.e. actual id
            actual_id = df_sheet.columns[col_num]

            # checking codition for actual id == station_id[col_num]
            for i in range(len(station_id)):
                if (station_id[i] == actual_id):
                    s_name = station_name[i]
                    return s_name
            s_name = actual_id
            return s_name



        # Creating x and y axis value decider
        def x_y_values(i, reference_vol):
            # Clearing previous figure saved to solve over writting issue
            plt.clf()
            
            # intersection point
            int_point = []

            # color decider
            color_grph = ['r', 'b', 'g']
            label_grph = ['April', 'May', 'June']

            # plotting for 3 months
            for month_number in range(3):
                # Taking ith column
                total_sample = month_decider(i, month_number)

                # unique value by using "unique()" method
                max_value_us = max(total_sample)+20
                unique_sample = np.arange(0, max_value_us, 20)

                # Calling counter function
                counter_values = counter_(unique_sample, total_sample)

                # Defining the axis values for plotting
                x_axis_values = counter_values
                y_axis_values = unique_sample

                # getting the intersection point
                int_point.append(0)
                for i in range(len(unique_sample)):
                    difference = unique_sample[len(unique_sample) - i-1] - reference_vol
                    if(difference<0):
                        difference = -difference
                    if(difference <= 10):
                        int_point[month_number] = x_axis_values[len(unique_sample) - i-1]
                        break

                # plotting the graph
                plt.plot(x_axis_values, y_axis_values, color = color_grph[month_number], label = label_grph[month_number])

            # adding text inside the plot
            plt.text(-5, 60, f'April = {round(int_point[0], 2)}\nMay = {round(int_point[1], 2)}\nJune = {round(int_point[2], 2)}', fontsize = 10)
            
            # Graphing the reference line
            plt.plot(np.arange(0, 100, 1), np.repeat(reference_vol, 100), color = "black", label = f"Ref Volt = {reference_vol} MW")
            # Naming the x-axis, y-axis and the whole graph
            plt.xlabel("% Time Duration")
            plt.ylabel("Load (Mega Watt)")
            title_name = title_decider(i)
            plt.title(title_name)

            # Adding legend, which helps us recognize the curve according to it's color
            plt.legend()

            # To load the display window
            # plt.show()

            # save the figure
            plt.savefig('vinod_fig.png')



        # image adder function to add the plot to the toolbox
        def image_adder():
            # loading image
            pixmap = qtg.QPixmap('vinod_fig.png')
            
            # Addign image to label
            my_label_img.setPixmap(pixmap)

            # resizing label to image size
            my_label_img.resize(pixmap.width(), pixmap.height())
        
        
        
        # define the function to perform when button is pressed
        def press_it():
            # getting column number from drop down menu
            i = my_combo.currentIndex() + 1

            # getting reference voltage from entry box
            ref_vol = float(my_entry.text())

            # calling x_value function to do the rest of work
            x_y_values(i, ref_vol)

            # adding figure to the tool box by caling the image_adder function to do so
            image_adder()

            # print
            print("Executed the code........")
    

app = qtw.QApplication([])
mw = MainWindow()

# run the app
app.exec_()