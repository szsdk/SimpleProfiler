cmake .. -DCMAKE_INSTALL_PREFIX:PATH=.. -DCMAKE_BUILD_TYPE=Release 
cmake .. -DCMAKE_INSTALL_PREFIX:PATH=.. -DCMAKE_BUILD_TYPE=Release -DPYTHON_LIBRARY=$(python3-config --prefix)/lib/libpython3.so -DPYTHON_INCLUDE_DIR=$(python3-config --prefix)/include/python3.9 -DPYTHON_EXECUTABLE:FILEPATH=$(which python3)
