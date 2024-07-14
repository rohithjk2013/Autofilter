# Autofilter
The Data Processor App is a user-friendly tool for efficient data processing and filtering, utilizing a graphical user interface built with Tkinter. It allows users to upload CSV or Excel files, select specific columns for processing, apply various filtering techniques, and visualize the results.
Key Features:

    File Upload:
        Users can upload CSV or Excel files containing the data to be processed.

    Column Selection:
        Select multiple columns from the uploaded data for processing via a listbox.

    Filter Selection:
        Choose from a variety of filters:
            Moving Average
            Savitzky-Golay
            Low-pass Filter
            High-pass Filter
            Band-pass Filter
            Band-stop Filter
            Exponential Moving Average
            Median Filter
            Butterworth Filter
            Chebyshev Filter

    Window Size Input:
        Specify the window size for the chosen filter.

    Data Processing:
        Process the selected columns with the chosen filter and window size.
        Processed data columns are named with a suffix _Filtered.

    Data Visualization:
        Plots of the original and filtered data are generated and displayed using Matplotlib within the Tkinter window.

    Save Processed Data:
        Save the processed data to a new Excel file.

    User-Friendly Interface:
        Clear instructions and labels guide the user.
        Progress messages indicate the status of data processing.

    Author Information:
        The app includes author information: Rohith Jayaraman Krishnamurthy from CRN Lab UBC.

Usage:

    Start the Application:
        Run the script to open the Tkinter window.

    Upload a File:
        Click "Upload File" to select and upload a CSV or Excel file.

    Select Columns:
        Use the listbox to select columns from the uploaded data.

    Choose a Filter:
        Select a filter from the dropdown menu.

    Enter Window Size:
        Specify the window size for the filter.

    Process the Data:
        Click "Process Data" to apply the filter to the selected columns.

    View Results:
        The original and filtered data are plotted and displayed within the app.

    Save Processed Data:
        Click "Save Processed Data" to save the results to an Excel file.

Benefits:

    Ease of Use: Intuitive graphical interface suitable for users with minimal programming experience.
    Multiple Filtering Options: Diverse filters to meet various data processing needs.
    Visualization: Immediate visual feedback through plots.
    Data Export: Ability to save processed data for further analysis or sharing.

The Data Processor App streamlines data filtering and visualization, providing an effective solution for data processing needs.
