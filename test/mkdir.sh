echo "dir1" > dirs.txt
echo "dir2" >> dirs.txt
echo "dir3" >> dirs.txt

../combobreaker.py -v mkdir -p -[ dirs.txt ]
../combobreaker.py -v touch [ -[ dirs.txt ] / [ file1 file2 file3 ] ]
