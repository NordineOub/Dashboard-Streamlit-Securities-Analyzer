# Dashboard Streamlit Securities Analyzer

This program studies requests for land values in France between 2016 and 2020 and allows any user to view the information as close as possible to the field.

Several study layers are available:

## Departmental level:
- Allows you to see the distribution of sales in a department
- Visualize the nature of changes and types of sales
- Has a raw and graphic shape


## City level:
- Allows you to see the distribution of sales in a city
- Visualize the nature of the transfers, the types of sales and the exact location (address ...)
- Has a raw and graphic shape


## National level :
- Allows you to see the distribution of sales throughout France
- Visualize the nature of changes and types of sales
- Has a raw and graphic shape

# Pre process & logs

To import the data properly, they are stored and retrieved by a .gz compression system, a program will import and parsing.

The logs contain the name, launch date and duration of different programs. It is possible to see the logs in the logs.txt file

You can also change the sample taken by the dashboard by writing the chosen value in this function : 
```s
def importData(wt): 
    
    val= pd.read_csv(wt,  compression='gzip')
    return val.sample(500000) # Here you choose the number of sample you want

```
Note that the more sample you choose, the longer loading will be.

# Streamlit Share

The streamlit share link was produced but it does not work for the following reasons:
- CSV file is much too large, the virtual machine does not accept to retrieve and study so much information
- The RAM allocated by the streamlit team is not sufficient to display all the code with such large csv files, despite the fact that the import only uses a sample of 500,000 lines

The link is as follows: 
## https://share.streamlit.io/nordineoub/dashboard_lab4/main/DashBoard_Lab4.py
