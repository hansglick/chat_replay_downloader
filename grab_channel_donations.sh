channel_url=$1
final_results_filename=$2


echo "recuperation de la channel"
bash app_grab_channel.sh $channel_url "data/temp_channel_data"

echo "parsing des urls"
bash app_parser.sh "data/temp_channel_data" "data/temp_channel_urls"

echo "récupération des dons"
python app_grab_money.py -u "data/temp_channel_urls" -s $final_results_filename

rm "data/temp_channel_data"
rm "data/temp_channel_urls"