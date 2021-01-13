youtube-dl --ignore-errors --get-filename --skip-download -o "%(upload_date)s;%(id)s;%(duration)s;%(title)s" $1 >> $2
