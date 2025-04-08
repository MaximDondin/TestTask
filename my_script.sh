#!/bin/bash

UNIT_PATTERN="foobar-*.service"

units=$(systemctl list-unit-files "$UNIT_PATTERN" --no-legend | awk '{print $1}')

if [ -z "$units" ]; then
	echo "Не найдено юнитов, соответствующих шаблону ${UNIT_PATTERN}"
	exit 1
fi

for unit in $units; do
	echo "Обработка юнита: $unit"
	service_name=${unit#foobar-}

	if ! systemctl stop "$unit"; then
        	echo "Ошибка при остановке $unit"
        	exit 2
	fi

	old_dir="/opt/misc/$service_name"
	new_dir="/srv/data/$service_name"
	unit_file="/etc/systemd/system/$unit"

	if [ ! -d "$old_dir" ]; then
        	echo "Исходная директория $old_dir не существует"
        	exit 3
	fi

	if ! mkdir -p "$new_dir"; then
		echo "Ошибка при создании директории"
		exit 4
	fi

	if ! mv "$old_dir"/* "$new_dir"/; then
        	echo "Ошибка переноса файлов из $old_dir в $new_dir"
        	exit 5
    	fi

	sed -i -e "s#WorkingDirectory=/opt/misc/$service_name#WorkingDirectory=/srv/data/$service_name#" \
	 -e "s#/opt/misc/$service_name#/srv/data/$service_name#g" \
    	"$unit_file" || { echo "Ошибка изменения $unit"; exit 6 }

	systemctl daemon-reload

	systemctl start "$unit" || echo "Ошибка при запуске $unit"
done
