# utilisation : app_parser.sh urlsdata.txt urls
filename=$1
files_array=()

while read line

do

arrIN=(${line//;/ })
myurl="https://www.youtube.com/watch?v=${arrIN[1]}"
files_array+=($myurl)

done < $filename

sorted_unique_ids=($(echo "${files_array[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))


for i in "${sorted_unique_ids[@]}"
do
	echo $i >> $2
done




#while read line; do

#arrIN=(${line//;/ })
#myurl="https://www.youtube.com/watch?v=${arrIN[1]}"
#echo $myurl >> $2

#done < $filename