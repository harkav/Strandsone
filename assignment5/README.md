# IN3110 strømpris

A webapp that displays the prices of electricity in the different parts of Norway over time. 
Data is collected from the hvakosterstrømmen.no api. 

installation: 
    on envs: 
        I've used Anaconda, and if you want the same env as I've used, you can run: 
        pip install -r requirements2.txt
        This will include a buttload of unecessary stuff, and hopefully 
        pip intsall -r requirements should suffice. 


    from root dir: 
    

    python3 -m pip install -e 
    
    
    run: 
    python3 app.py 

    open 127.0.0.1:5000/ 

Docs: 
Docs are available at 127.0.0.1:5000/help or can be built by runing 
    make html in the ./docs dir. 

Tests: 
    run pytest 
                ./tests/test_app.py 
                ./tests/test_strompris.py
                ./tests/conftest.py
                ./test_files.py

        test_app.py fails on some of the tests, but those tests seems to be for the bonus/in4110 assignments. 


I have not implemented the task for in4110, nor any of the bonus tasks 

#TODO: 
    still a bug when you de-select all checkboxes on the graph. displays all graphs, should throw some sort of error. 
