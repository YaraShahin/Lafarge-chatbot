import pandas as pd
import matplotlib.pyplot as plt

class ChatbotEngine:
    
    def __init__(self):
        self.reply = "Hi there! How can I help you today?"
        self.responses = ["info center", "data lab"]
        self.clr = False

        self.get_data()

    def get_data(self):
        SHEET_ID = '1YRw1mIFsu7fDctWjcim3TGFm8LGJc3jWGRO3_b7xYfQ'
        info_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=info'
        data_url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=data'
        self.df_info = pd.read_csv(info_url)
        self.df_data = pd.read_csv(data_url)

    def get_response(self, user_input):
        if not user_input:
            self.reply = "Hi there! How can I help you today?"
            self.responses = ["info center", "data lab"]
            self.clr = False
        else:
            #info center
            if (user_input[0]==0):
                #info center
                if (len(user_input)==1):
                    self.reply = "Welcome to Lafarge Information Center! What topic would you like to know more about?"
                    self.responses = self.df_info['Category'].tolist()
                    self.clr = False
                #info center -> category
                else:
                    self.reply = self.df_info.iloc[user_input[1],1] +  "\n\nLafarge Assistant: Hi there! How can I help you today?"
                    self.responses = ["info center", "data lab"]
                    self.clr = True
            #data center
            else:
                #data center
                if(len(user_input)==1):
                    self.reply = "Welcome to Lafarge data lab! Here you can enhance your decision-making using data-driven analysis.\nHow can I help you?"
                    self.responses = ["aggregation", "lookup", "filter", "graph"]
                    self.clr = False
                #data center -> tool
                else:
                    #data center -> aggregation
                    if (user_input[1]==0):
                        #data center -> aggregation
                        if (len(user_input)==2):
                            self.reply = "Which column would you like to see statistical summary of?"
                            self.responses = self.df_data.columns.tolist()
                            self.clr = False
                        #data center -> aggregation -> column
                        elif (len(user_input)==3):
                            self.reply = "Which statistical summary do you want?"
                            self.responses = ["min", "max", "avg", "median"]
                            self.clr = False
                        #data center -> aggregation -> column -> aggregation type
                        else:
                            #data center -> aggregation -> column -> min
                            if (user_input[3]==0):
                                self.reply = "The minimum value of the " + self.df_data.columns.tolist()[2] + " column is: "+ str(self.df_data.iloc[:, user_input[2]].min())
                            #data center -> aggregation -> column -> max
                            elif (user_input[3]==1):
                                self.reply = "The maximum value of the " + self.df_data.columns.tolist()[2] + " column is: "+ str(self.df_data.iloc[:, user_input[2]].max())
                            #data center -> aggregation -> column -> avg
                            elif (user_input[3]==2):
                                self.reply = "The mean value of the " + self.df_data.columns.tolist()[2] + " column is: "+ str(self.df_data.iloc[:, user_input[2]].mean())
                            #data center -> aggregation -> column -> median
                            else:
                                self.reply = "The median value of the " + self.df_data.columns.tolist()[2] + " column is: "+ str(self.df_data.iloc[:, user_input[2]].median())

                            self.reply = self.reply + "\n\nLafarge Assistant: Hi there! How can I help you today?"
                            self.responses = ["info center", "data lab"]
                            self.clr = True
                    #data center -> lookup
                    elif  (user_input[1]==1):
                        pass
                    #data center -> filter
                    elif  (user_input[1]==2):
                        pass
                    #data center -> graph
                    else:
                        #data center -> graph
                        if (len(user_input)==2):
                            self.reply = "What graph would you like me to plot?"
                            self.responses = ["historgam", "scatter plot"]
                            self.clr = False
                        #data center -> graph -> type of graph
                        else:
                            #data center -> graph -> histogram
                            if (user_input[2]==0):
                                #data center -> graph -> histogram
                                if (len(user_input)==3):
                                    self.reply = "Sure! Which column would you like a frequency histogram of?\nPlease choose a categorical column."
                                    self.responses = self.df_data.columns.tolist()
                                    self.clr = False
                                #data center -> graph -> histogram -> column
                                else:
                                    self.df_data.iloc[:,user_input[3]].value_counts().plot(kind='bar')
                                    self.reply = "Here is your histogram!\n\nLafarge Assistant: Hi there! How can I help you today?"
                                    self.responses = ["info center", "data lab"]
                                    self.clr = True
                                    plt.show()
                            #data center -> graph -> scatter plot
                            else:
                                #data center -> graph -> scatter plot
                                if (len(user_input)==3):
                                    self.reply = "Sure! Which column would you like to use for the x-axis?\nPlease choose a numerical column."
                                    self.responses = self.df_data.columns.tolist()
                                    self.clr = False
                                #data center -> graph -> scatter plot -> x-axis col
                                elif (len(user_input)==4):
                                    self.reply = "Great! Now, which column would you like to use for the y-axis?\nPlease choose a numerical column."
                                    self.responses = self.df_data.columns.tolist()
                                    self.clr = False
                                #data center -> graph -> scatter plot -> x-axis col -> y-axis col
                                else:
                                    plt.scatter(self.df_data.iloc[:,user_input[3]], self.df_data.iloc[:,user_input[4]])
                                    self.reply = "Here is your scatter plot!\n\nLafarge Assistant: Hi there! How can I help you today?"
                                    self.responses = ["info center", "data lab"]
                                    self.clr = True
                                    plt.show()

        return [self.reply, self.responses, self.clr]
