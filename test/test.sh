echo "1) Number of json messages = Number of template files. Test: OK"
python ../src/checkjson.py ./template1.json ./stream1.json 

echo "2) Number of json messages > Number of template files. Test Failed"
python ../src/checkjson.py ./template2.json ./stream2.json

echo "3) Number of json messages < Number of template files. Test failed"
python ../src/checkjson.py ./template3.json ./stream3.json

echo "4) Number of json messages < Number of template files. Test failed"
python ../src/checkjson.py ./template4.json ./stream4.json

