It only compares 2 files if they have same name and are in different folders — one file in the "Input1" folder and the other in the "Input2" folder.

## How to Use

1. Put all your `.xml` files of set 1 in the `Input1` folder.  
2. Put all your `.xml` files of set 2 in the `Input2` folder.  
3. Run the script `compare_script.py`.  
4. Your results will be saved in a folder named like `Result_<date_time>`, with each result having the same name as the compared `.xml` file.

> 💡 Press `Shift + Alt + F` in VS Code to beautify (format) XML files.

## Folder Structure

```
project_folder/
├── compare_script.py
├── Input1/
│   ├── file1.xml
│   ├── file2.xml
├── Input2/
│   ├── file1.xml
│   ├── file2.xml
└── Results/
    ├── file1.txt
    ├── file2.txt
```
