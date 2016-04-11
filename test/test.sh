echo "1) Number of json messages = Number of template files. Test: OK"
python ../src/checkjson.py -t ./template1.json -j ./stream1.json

echo "2) Number of json messages > Number of template files. Test Failed"
python ../src/checkjson.py -t ./template2.json -j ./stream2.json

echo "3) Number of json messages < Number of template files. Test failed"
python ../src/checkjson.py -t ./template3.json -j ./stream3.json

echo "4) Number of json messages < Number of template files. Test failed"
python ../src/checkjson.py -t ./template4.json -j ./stream4.json

